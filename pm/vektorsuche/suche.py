# KI-generiert (Claude Sonnet, 2026-11-21), Entwurf
"""suche.py "Frage" [-k 5] [--modell nomic|bge-m3] [--modus vektor|bm25|hybrid|hybrid-dok] [--rag]
Varianten: A = nomic/vektor, B = bge-m3/vektor, C = bge-m3/hybrid (RRF k=60 aus BM25 + Vektor, Chunkebene),
D = bge-m3/hybrid-dok (RRF über Aktenränge, Akte = max-Score ihrer Chunks)."""
import argparse, re, time
from korpus import *

RRF_K = 60
STANDARD = dict(modell="bge-m3", modus="vektor")   # beste Variante B laut bewertung.json (hit@3)
_bm = None

def bm25():
    global _bm
    if _bm is None: _bm = BM25(alle_chunks())
    return _bm

def vektor(frage, k, modell):
    c = collection(modell)
    q = embed([frage], modell, "frage")[0]
    r = c.query(query_embeddings=[q], n_results=k)
    return [dict(score=1 - d, text=t, **m) for d, t, m in zip(r["distances"][0], r["documents"][0], r["metadatas"][0])]

def _dok_max(treffer):
    """Chunk-Treffer -> Akten, Score = max über ihre Chunks (bester Chunk als Vertreter)."""
    out = {}
    for t in treffer:
        if t["id"] not in out or t["score"] > out[t["id"]]["score"]: out[t["id"]] = t
    return sorted(out.values(), key=lambda t: -t["score"])

def _rrf(listen, schluessel):
    s, rep = {}, {}
    for l in listen:
        for r, t in enumerate(l, 1):
            s[schluessel(t)] = s.get(schluessel(t), 0) + 1 / (RRF_K + r); rep.setdefault(schluessel(t), t)
    return [dict(rep[x], score=s[x]) for x in sorted(s, key=lambda x: -s[x])]

def abruf(frage, k=5, modell=None, modus=None):
    modell = modell or STANDARD["modell"]; modus = modus or STANDARD["modus"]
    n = max(k, 50)
    if modus == "bm25": return bm25().suche(frage, n)[:k]
    v = vektor(frage, n, modell)
    if modus == "vektor": return v[:k]
    b = bm25().suche(frage, n)
    if modus == "hybrid": return _rrf([v, b], lambda t: t["cid"] if "cid" in t else t["text"])[:k]
    if modus == "hybrid-dok": return _rrf([_dok_max(v), _dok_max(b)], lambda t: t["id"])[:k]
    raise ValueError(modus)

def dok_rang(treffer):
    out = []
    for t in treffer:
        if t["id"] not in out: out.append(t["id"])
    return out

ID_RE = re.compile(r"\b(ENT-\d{3}|B-BAT-\d{3}|[WPT]\d{2})\b")

def antwort(frage, treffer):
    kontext = "\n\n".join(t["text"] for t in treffer)
    system = ("Antworte auf Deutsch, knapp, AUSSCHLIESSLICH aus den folgenden Textstücken. Jede Aussage endet mit dem Beleg "
              "in eckigen Klammern, z. B. [ENT-152], [B-BAT-030] oder [W20]; die ID steht am Anfang jedes Textstücks. "
              "Steht die Antwort nicht in den Textstücken, schreibe: Nicht in den Akten.")
    r = post("/api/chat", {"model": LLM_MODEL, "stream": False, "think": False, "options": {"temperature": 0.1},
             "messages": [{"role": "system", "content": system}, {"role": "user", "content": f"Textstücke:\n{kontext}\n\nFrage: {frage}"}]})
    return r["message"]["content"].strip()

def grounding(text, treffer):
    """Jede zitierte ID muss in den abgerufenen Chunks vorkommen (analog forschung/pruefe.py)."""
    erlaubt = {t["id"] for t in treffer}
    zitiert = ID_RE.findall(text)
    falsch = sorted({i for i in zitiert if i not in erlaubt})
    saetze = [s for s in re.split(r"(?<=[.!?])\s+|\n", text) if len(s.strip()) > 25]
    ohne = [s for s in saetze if not ID_RE.search(s)]
    if "Nicht in den Akten" in text and not zitiert: status = "OK (keine Antwort)"
    elif not zitiert: status = "BELEG FEHLT (keine ID)"
    elif falsch: status = "BELEG FEHLT (falsche ID: " + ", ".join(falsch) + ")"
    else: status = "OK"
    return dict(status=status, zitiert=sorted(set(zitiert)), falsch=falsch, saetze_ohne_beleg=len(ohne))

if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("frage"); ap.add_argument("-k", type=int, default=5); ap.add_argument("--rag", action="store_true")
    ap.add_argument("--modell", choices=list(MODELLE), default=STANDARD["modell"])
    ap.add_argument("--modus", choices=["vektor", "bm25", "hybrid", "hybrid-dok"], default=STANDARD["modus"])
    a = ap.parse_args()
    t = time.time(); tr = abruf(a.frage, a.k, a.modell, a.modus)
    for i, x in enumerate(tr, 1):
        print(f"{i}. {x['score']:.3f}  {x['id']:<10} {x['quelle']}  | {x['abschnitt']}")
    print(f"(Abruf {time.time()-t:.2f} s; {a.modell}/{a.modus})")
    if a.rag:
        t = time.time(); ans = antwort(a.frage, tr); g = grounding(ans, tr)
        print(f"\n{ans}\n\nGrounding: {g['status']}; Sätze ohne Beleg: {g['saetze_ohne_beleg']} ({time.time()-t:.1f} s)")
