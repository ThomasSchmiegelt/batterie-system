# KI-generiert (Claude Sonnet, 2026-11-21), Entwurf

> **KI-generiert.** Dokument im Entwurfsstatus, nicht geprüft und nicht freigegeben. Ersteller: Claude Sonnet, 2026-11-21. Prüfer: offen (Opus).

# Vektorsuche und RAG über die Projektakten (Prototyp)

## Zweck
Kleiner, nachprüfbarer Nachweis für Vektordatenbanken und Embedding-Retrieval: Fragen in Alltagssprache finden die passende Akte (ENT, B-BAT, Recherche), optional beantwortet ein lokales Modell die Frage ausschließlich aus den Fundstellen und muss jede Aussage belegen.

## Architektur
Frage → Embedding (ollama, lokal: `bge-m3` Standard, `nomic-embed-text` mit Präfix `search_query:`) → Chroma (persistent, `db/`, Kosinus, je Modell eine Collection), optional Hybrid mit BM25 (RRF) → Top-k → LLM `qwen3.5:9b` mit Belegpflicht ([ENT-NNN], [B-BAT-NNN], [Wnn]) → Grounding-Prüfung im Code (jede zitierte ID muss in den abgerufenen Chunks stehen, sonst „BELEG FEHLT“; analog `forschung/pruefe.py`). Nichts geht ins Internet (nur pip und `ollama pull bge-m3` für die Installation).

Korpus: `pm/entscheidungen/ENT-*.md` (YAML-Kopf als Metadaten), je Abschnitt `## B-BAT-NNN` aus `BEFUNDE.md`, und `forschung/ergebnis/*.md` **nur mit bestandener Prüfung** (letzte Zeile von `<Nr>.pruefung.txt` enthält „0 Fehler“; 20 Dateien ohne Prüfdatei oder mit Fehler sind ausgeschlossen). Chunks ca. 800 Zeichen an Absätzen, 150 Zeichen Überlappung; jeder Chunk beginnt mit seiner ID. Metadaten je Chunk: quelle, id, abschnitt, typ (bei ENT zusätzlich bauteile, merkmal, status).

Dateien: `korpus.py` (Laden, Chunking, Embedding), `index.py`, `suche.py`, `bewertung.py`, `bewertung.json`.

## Aufruf
```bash
source umgebung.sh && cd pm/vektorsuche
ollama pull bge-m3
python index.py nomic; python index.py bge-m3     # je 10-25 s
python suche.py "Wo sitzt das Kühlmodul?" -k 5 --rag [--modell nomic|bge-m3] [--modus vektor|bm25|hybrid|hybrid-dok]
python bewertung.py                      # 5 Verfahren x 12 Fragen, ca. 2 min
```

## Ergebnisse (`bewertung.json`, Teil `varianten`)
Korpus: 234 Dokumente, 678 Chunks; Treffer auf Dokumentebene, dieselben 12 Fragen in allen Varianten. Varianten: A = nomic-embed-text (englisch, Präfixe), B = bge-m3 (mehrsprachig, ohne Präfix), C = bge-m3 + BM25 mit Reciprocal Rank Fusion (k=60, Chunkebene), D = wie C, aber Rangliste je Akte (max-Score ihrer Chunks).

| Variante | Modell / Modus | hit@1 | hit@3 | hit@5 | Abruf | RAG | Grounding beanstandet | "Nicht in den Akten" |
|---|---|---|---|---|---|---|---|---|
| A nomic Vektor | nomic / vektor | 8 % | 25 % | 42 % | 0.126 s | 0.8 s | 0 von 12 | 6 |
| B bge-m3 Vektor | bge-m3 / vektor | 33 % | 58 % | 58 % | 0.066 s | 1.0 s | 0 von 12 | 4 |
| C bge-m3+BM25 Hybrid (RRF) | bge-m3 / hybrid | 33 % | 33 % | 58 % | 0.058 s | 1.0 s | 0 von 12 | 5 |
| D Hybrid Aktenebene | bge-m3 / hybrid-dok | 25 % | 42 % | 50 % | 0.093 s | 1.1 s | 0 von 12 | 4 |
| Basis BM25 | - / bm25 | 25 % | 33 % | 33 % | 0.001 s | 0.7 s | 0 von 12 | 8 |

hit@1/3/5 je Frage (ja/nein):

| Nr | Zielakte | A | B | C | D | BM25 |
|---|---|---|---|---|---|---|
| 1 | ENT-152, ENT-153, ENT-154 | nein/nein/ja | ja/ja/ja | ja/ja/ja | ja/ja/ja | ja/ja/ja |
| 2 | ENT-005 | nein/nein/nein | ja/ja/ja | ja/ja/ja | ja/ja/ja | ja/ja/ja |
| 3 | ENT-114 | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein |
| 4 | ENT-127 | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein |
| 5 | ENT-030 | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein |
| 6 | ENT-006 | nein/nein/nein | nein/ja/ja | nein/nein/ja | nein/nein/ja | nein/nein/nein |
| 7 | ENT-151 | nein/ja/ja | ja/ja/ja | ja/ja/ja | nein/ja/ja | nein/ja/ja |
| 8 | ENT-135 | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein |
| 9 | ENT-086 | nein/nein/ja | nein/ja/ja | nein/nein/ja | nein/ja/ja | nein/nein/nein |
| 10 | ENT-126 | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein | nein/nein/nein |
| 11 | ENT-095 | nein/ja/ja | nein/ja/ja | nein/nein/ja | nein/nein/nein | nein/nein/nein |
| 12 | ENT-157 | ja/ja/ja | ja/ja/ja | ja/ja/ja | ja/ja/ja | ja/ja/ja |

Deutung (Opus-Erwartungen: bge-m3 hit@3 ≥ 50 %, Hybrid ≥ BM25 und ≥ Vektor allein):
- Erwartung 1 **erfüllt**: bge-m3 hit@3 58 % (nomic 25 %). Das englische Modell auf deutschem Korpus war also plausibel eine Hauptursache; der Gewinn bleibt bei 12 Fragen (1 Frage = 8,3 Punkte) unsicher.
- Erwartung 2 **verfehlt**: Hybrid C hit@3 33 %, D 42 %, beide unter bge-m3 allein (58 %), über BM25 (33 %). Der Schlüsselwortanteil verdrängt hier gute Vektortreffer; bei hit@5 liegt C gleichauf mit B. Nichts nachgebessert.
- Standard in `suche.py`: Variante B (`--modell bge-m3 --modus vektor`), weil beste hit@3.
- Die RAG-Antworten werden zwischen Läufen nicht identisch (Temperatur 0,1): Variante A hatte im ersten Lauf 1 beanstandete Antwort, im zweiten 0. Die Grounding-Prüfung prüft nur die ID, nicht den Inhalt.

## Grenzen
Einzelplatz, ein kleines Korpus (ca. 234 Dokumente), 12 Testfragen von der KI selbst gewählt (Zielakten ebenfalls von ihr gewählt, mehrere zulässige IDs nur bei der Kühlplatte), keine Wiederholung mit anderen Embedding-Modellen oder Chunkgrößen, ein Lauf bei Temperatur 0,1. Die Zahlen belegen den Prototyp, keine allgemeine Eignung der Verfahren.
