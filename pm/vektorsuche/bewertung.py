# KI-generiert (Claude Sonnet, 2026-11-21), Entwurf
"""12 Testfragen mit Zielakte: hit@1/3/5 (Dokumentebene) Vektor vs. BM25, Antwortzeit, RAG-Grounding."""
import json, math, re, time, numpy as np
from korpus import *
import suche
from suche import abruf, dok_rang, antwort, grounding

# Fragen von der KI selbst gewählt; Zielakten (Menge zulässiger IDs) aus den Akten gelesen.
FRAGEN = [
 ("Warum wird die Kühlplatte aus gelötetem Blech statt aus einem Vollblock gebaut?", ["ENT-152", "ENT-153", "ENT-154"]),
 ("Welche Zellchemie ist die Hauptvariante und warum?", ["ENT-005"]),
 ("Wie werden die Zellen im Pack auf gleiche Spannung gebracht?", ["ENT-114"]),
 ("Wodurch ist der Hochstrompfad gegen Kurzschluss geschützt?", ["ENT-127"]),
 ("Wie breit darf das Pack im Fahrzeug maximal sein?", ["ENT-030"]),
 ("Wie viele Zellen liegen in Reihe, und welche Spannung ergibt das?", ["ENT-006"]),
 ("Warum hat das Pack keinen Aufprallpuffer für den Seitencrash?", ["ENT-151"]),
 ("Womit wird bei Frost der Kühlkreislauf erwärmt?", ["ENT-135"]),
 ("Aus welchem Werkstoff sind die Querträger und was spricht dafür?", ["ENT-086"]),
 ("Wie lange darf das Einschalten des Zwischenkreises dauern?", ["ENT-126"]),
 ("Wie kommt die Wärme von der Oberseite der Zellen in die Kühlplatte?", ["ENT-095"]),
 ("An welcher Stelle am Pack sitzt das Aggregat für den Kühlmittelkreis?", ["ENT-157"]),
]

def hit(rang, ziele, k): return any(i in ziele for i in rang[:k])

VARIANTEN = {  # Name: (Modell, Modus)
 "A nomic Vektor": ("nomic", "vektor"), "B bge-m3 Vektor": ("bge-m3", "vektor"),
 "C bge-m3+BM25 Hybrid (RRF)": ("bge-m3", "hybrid"), "D Hybrid Aktenebene": ("bge-m3", "hybrid-dok"),
 "Basis BM25": ("bge-m3", "bm25")}
rows = alle_chunks(); n = len(FRAGEN)
res = {}
for name, (mod, modus) in VARIANTEN.items():
    erg = []; tv = tr = 0.0
    for f, ziele in FRAGEN:
        t = time.time(); v = abruf(f, 50, mod, modus); dt = time.time() - t
        rv = dok_rang(v)
        t = time.time(); ans = antwort(f, v[:5]); g = grounding(ans, v[:5]); dr = time.time() - t
        tv += dt; tr += dr
        erg.append(dict(frage=f, ziele=ziele, rang=rv[:5], zeit_abruf_s=round(dt, 3), antwort=ans, grounding=g, zeit_rag_s=round(dr, 1),
                        **{f"hit@{k}": hit(rv, ziele, k) for k in (1, 3, 5)}))
    res[name] = dict(modell=mod, modus=modus, fragen=erg,
        **{f"hit@{k}": sum(e[f"hit@{k}"] for e in erg) / n for k in (1, 3, 5)},
        mittel_zeit_abruf_s=round(tv / n, 3), mittel_zeit_rag_s=round(tr / n, 1),
        grounding_beanstandet=sum(e["grounding"]["status"].startswith("BELEG FEHLT") for e in erg),
        antworten_nicht_in_akten=sum("Nicht in den Akten" in e["antwort"] for e in erg))
    print(name, {k: res[name][k] for k in ("hit@1", "hit@3", "hit@5", "grounding_beanstandet", "antworten_nicht_in_akten")}, flush=True)
json.dump(dict(korpus=dict(dokumente=len({r["id"] for r in rows}), chunks=len(rows)), varianten=res,
               hinweis="KI-generiert (Claude Sonnet, 2026-11-21), Entwurf; Fragen identisch zum ersten Lauf"),
          open("bewertung.json", "w"), ensure_ascii=False, indent=1)
