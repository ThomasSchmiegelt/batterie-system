---
typ: dokument
datei: "praesentation/bausteine/E3d.md"
tags: ["dokument", "kopie"]
---
# E3d

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/E3d.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf. Folienbaustein Vorgang E3d (v0.2, neue Stückliste).

# Grobe FMEDA der CMU-Platine: mit zwei Schaltern in Reihe und Zellschutz je Zelle werden beide Ziele erreicht
**Kernaussage: Mit Doppel-FET je Ausgleichskanal und drei 6-Zellen-Überspannungsschützen liegt die Einzelfehlerabdeckung beim Überladeschutz (ASIL D) bei 99,93 % und beim Schutz vor dem Laden tiefentladener Zellen (ASIL C) bei 97,85 % (vorher 95,71 %, Ziel 97 %).**

**Bild:** sim/elektrik/e3d_fmeda/e3d_fmeda.png (Zielband: SPFM/LFM je SG, ASIL D 99/90 %, ASIL C 97/80 %)

**Zahlen** (Quelle sim/elektrik/e3d_fmeda/ergebnis.json, Block `cmu`):
- SG-01: SPFM 99,93 %, LFM 96,72 %
- SG-02: SPFM 97,85 %, LFM 97,81 %; Hauptbeitrag Ausgleichs-FET-Kurzschluss (latent) und AFE „Ausgleich hängt an“ (Block `top`)
- Maßnahme M1 (zweiter Schalter in Reihe) ist Ist-Stand der Stückliste (ENT-192), Sekundärschutz misst je Zelle (ENT-193, B-BAT-055)
- Alle FIT- und Diagnosewerte sind Annahmen (ERW-E3d); Abgleich in sim/elektrik/e3d_fmeda/ERGEBNIS.md

*KI-generiert, Entwurf.*

