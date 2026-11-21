# KI-generiert (Claude Sonnet, 2026-11-21), Entwurf
"""Baut den Index: Korpus -> Chunks -> Embeddings (ollama nomic-embed-text) -> Chroma (pm/vektorsuche/db)."""
import time, shutil, os
import sys
from korpus import *
modell = sys.argv[1] if len(sys.argv) > 1 else "nomic"   # nomic | bge-m3
t = time.time()
rows = alle_chunks()
ids = sorted({r["id"] for r in rows})
print(f"Dokumente {len(ids)}, Chunks {len(rows)}")
import chromadb
cl = chromadb.PersistentClient(path=DB)
try: cl.delete_collection(MODELLE[modell][3])
except Exception: pass
c = collection(modell)
emb = embed([r["text"] for r in rows], modell, "dok")
for i in range(0, len(rows), 200):
    b = rows[i:i+200]
    c.add(ids=[r["cid"] for r in b], embeddings=emb[i:i+200], documents=[r["text"] for r in b],
          metadatas=[dict(quelle=r["quelle"], id=r["id"], abschnitt=r["abschnitt"], typ=r["typ"], **{k: v for k, v in r["meta"].items()}) for r in b])
n = {}
for r in rows: n.setdefault(r["typ"], set()).add(r["id"])
print({k: len(v) for k, v in n.items()}, f"Dauer {time.time()-t:.1f} s")
