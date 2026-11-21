# KI-generiert (Claude Sonnet, 2026-11-21), Entwurf
"""Gemeinsame Funktionen: Korpus laden, Chunking, Embedding (ollama), Chroma-Zugriff."""
import re, json, glob, os, urllib.request
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DB = os.path.join(os.path.dirname(__file__), "db")
OLLAMA = "http://localhost:11434"
MODELLE = {  # Name -> (ollama-Modell, Präfix Dokument, Präfix Frage, Collection)
    "nomic": ("nomic-embed-text", "search_document: ", "search_query: ", "projektakten"),
    "bge-m3": ("bge-m3", "", "", "projektakten_bge_m3"),
}
LLM_MODEL = "qwen3.5:9b"
CHUNK, OVERLAP = 800, 150

def post(pfad, daten, timeout=600):
    r = urllib.request.Request(OLLAMA + pfad, json.dumps(daten).encode(), {"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=timeout))

def embed(texte, modell="nomic", art="dok"):
    """nomic braucht Präfixe (search_document:/search_query:), bge-m3 nicht."""
    m, pd, pq, _ = MODELLE[modell]; praefix = pd if art == "dok" else pq
    aus = []
    for i in range(0, len(texte), 16):
        r = post("/api/embed", {"model": m, "input": [praefix + t for t in texte[i:i+16]]})
        aus += r["embeddings"]
    return aus

def yaml_kopf(text):
    m = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not m: return {}, text
    kopf = {}
    for z in m.group(1).splitlines():
        if ":" in z:
            k, v = z.split(":", 1); kopf[k.strip()] = v.strip()
    return kopf, m.group(2)

def chunks_von(text, groesse=CHUNK, ueberlapp=OVERLAP):
    """Chunking an Absätzen, ca. groesse Zeichen, Überlappung = letzter Absatz-Rest."""
    absaetze = [a.strip() for a in re.split(r"\n\s*\n", text) if a.strip()]
    out, akt = [], ""
    for a in absaetze:
        while len(a) > groesse * 1.5:      # sehr lange Absätze (Tabellen) hart teilen
            if akt: out.append(akt); akt = ""
            out.append(a[:groesse]); a = a[groesse - ueberlapp:]
        if akt and len(akt) + len(a) > groesse:
            out.append(akt); akt = akt[-ueberlapp:] + "\n\n" + a
        else:
            akt = (akt + "\n\n" + a) if akt else a
    if akt: out.append(akt)
    return out

def pruefung_ok(nr):
    p = os.path.join(ROOT, "forschung", "ergebnis", nr + ".pruefung.txt")
    if not os.path.exists(p): return False
    letzte = open(p, encoding="utf-8").read().strip().splitlines()[-1]
    return bool(re.search(r"\b0 Fehler", letzte))

def dokumente():
    """Liefert (id, quelle, typ, meta, text, abschnitt-aufteilung)."""
    docs = []
    for f in sorted(glob.glob(f"{ROOT}/pm/entscheidungen/ENT-*.md")):
        kopf, rest = yaml_kopf(open(f, encoding="utf-8").read())
        i = kopf.get("id") or os.path.basename(f)[:-3]
        docs.append(dict(id=i, quelle=os.path.relpath(f, ROOT), typ="ENT", text=f"{i} {kopf.get('titel','')}\n\n{rest}",
                         meta=dict(bauteile=kopf.get("bauteile", ""), merkmal=kopf.get("merkmal", ""), status=kopf.get("status", ""))))
    bt = open(f"{ROOT}/BEFUNDE.md", encoding="utf-8").read()
    for teil in re.split(r"(?m)^(?=## B-BAT-\d+)", bt):
        m = re.match(r"## (B-BAT-\d+)", teil)
        if m:
            docs.append(dict(id=m.group(1), quelle="BEFUNDE.md", typ="B-BAT", text=teil.strip(), meta={}))
    for f in sorted(glob.glob(f"{ROOT}/forschung/ergebnis/*.md")):
        nr = os.path.basename(f)[:-3]
        if not pruefung_ok(nr): continue
        docs.append(dict(id=nr, quelle=os.path.relpath(f, ROOT), typ="Recherche", text=open(f, encoding="utf-8").read(), meta={}))
    return docs

def alle_chunks():
    rows = []
    for d in dokumente():
        abschnitt = d["id"]
        for j, c in enumerate(chunks_von(d["text"])):
            h = re.findall(r"(?m)^#+ (.+)$", c)
            if h: abschnitt = h[0][:80]
            rows.append(dict(cid=f"{d['id']}#{j}", id=d["id"], quelle=d["quelle"], abschnitt=abschnitt,
                             typ=d["typ"], meta=d["meta"], text=f"[{d['id']}] " + c))
    return rows

def collection(modell="nomic"):
    import chromadb
    return chromadb.PersistentClient(path=DB).get_or_create_collection(MODELLE[modell][3], metadata={"hnsw:space": "cosine"})

# ---- BM25 (numpy), gleiche Chunks wie der Index ----
import math, numpy as np
def tok(s): return re.findall(r"[a-zäöüß0-9]+", s.lower())

class BM25:
    def __init__(self, rows, k1=1.5, b=0.75):
        self.rows = rows; self.d = [tok(r["text"]) for r in rows]
        self.avg = np.mean([len(x) for x in self.d]); self.k1, self.b = k1, b
        df = {}
        for x in self.d:
            for w in set(x): df[w] = df.get(w, 0) + 1
        n = len(self.d); self.idf = {w: math.log(1 + (n - v + .5) / (v + .5)) for w, v in df.items()}
        self.tf = [{w: x.count(w) for w in set(x)} for x in self.d]
    def suche(self, q, n=50):
        qt = tok(q); s = np.zeros(len(self.d))
        for i, (tf, x) in enumerate(zip(self.tf, self.d)):
            for w in qt:
                if w in tf: s[i] += self.idf[w] * tf[w] * (self.k1 + 1) / (tf[w] + self.k1 * (1 - self.b + self.b * len(x) / self.avg))
        return [dict(score=float(s[i]), **{kk: self.rows[i][kk] for kk in ("cid", "id", "quelle", "abschnitt", "text")}) for i in np.argsort(-s)[:n]]
