---
typ: dokument
datei: "praesentation/bausteine/E3d.md"
tags: ["dokument", "kopie"]
---
# E3d

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/E3d.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf. Folienbaustein Vorgang E3d.

# Grobe FMEDA der CMU-Platine: Tiefentladeschutz knapp verfehlt
**Kernaussage: Beim Überladeschutz (ASIL D) werden die Ziele erreicht, beim Schutz vor dem Laden tiefentladener Zellen (ASIL C) liegt die Einzelfehlerabdeckung bei 95,7 % statt 97 %; ein zweiter Schalter am Ausgleichs-FET würde sie auf 97,9 % heben.**

**Bild:** sim/elektrik/e3d_fmeda/e3d_fmeda.png (Zielband: SPFM/LFM je SG, ASIL D 99/90 %, ASIL C 97/80 %)

**Zahlen** (Quelle sim/elektrik/e3d_fmeda/ergebnis.json):
- SG-01: SPFM 99,92 %, LFM 98,14 % (Block `cmu`)
- SG-02: SPFM 95,71 %, LFM 100 %; Hauptbeitrag Ausgleichs-FET-Kurzschluss 0,72 FIT und AFE „Ausgleich hängt an“ 0,40 FIT (Block `top`)
- Maßnahme M1 (zweiter Schalter in Reihe): SPFM 97,85 % (Block `massnahmen`)
- Alle FIT- und Diagnosewerte sind Annahmen (ERW-E3d); Abgleich in sim/elektrik/e3d_fmeda/ERGEBNIS.md

*KI-generiert, Entwurf.*

