| Dok.-Nr. | ERG-E3d | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E3d: grobe FMEDA der CMU-Platine (ISO 26262-5, Grobentwurf) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf, nicht vom Menschen freigegeben, Prüfung Opus offen. Anforderung: REQ-P18. v0.2 ersetzt v0.1: Die Stückliste ist die überarbeitete (ERW-E3 Nachtrag 7, B-BAT-055, ENT-192/193). Alle FIT-Werte, Ausfallartenanteile und Diagnosedeckungen sind weiter **Annahmen Opus (ERW-E3d)**. Zahlen aus `ergebnis.json` (Ordner `sim/elektrik/e3d_fmeda/`).

## Was geändert wurde gegenüber v0.1
- Eingabe: `sim/elektrik/e3_platine/cmu_<V>_bom.csv` neu, je 110 Teile. Neu: 18 Doppel-N-FET SOT-363 mit zwei Schaltern in Reihe statt Einzel-FET (**M1 ist jetzt Ist-Stand**, in `fmeda.py` automatisch aktiv, sobald die Klasse `Doppel_NMOS_generisch` in der Stückliste steht) und 3 × 6-Zellen-Überspannungsschutz statt 1 × Summenschutz (Klasse `OVP6_generisch`, Einstufung wie bisher „Sekundärschutz“, FIT je Gehäuse 5, also 3 × 5 FIT).
- Der FIT-Ansatz je Gehäuse bleibt (MOSFET klein 1 FIT je Gehäuse, 18 Gehäuse), wie in ERW-E3 N7 („FETs bleiben 18 Gehäuse“). Keine neuen Annahmen. Das Was-wäre-wenn M1/M1+M2 aus v0.1 entfällt (M1 steckt in den Zahlen); M2 bleibt als Was-wäre-wenn.
- Die Einstufungsregeln sind unverändert (siehe v0.1: Zellabgriff, Ausgleichs-FET, AFE, Sekundärschutz, Stecker J1 als gemeinsame Ursache).

## Ergebnis (je CMU, `ergebnis.json` Block `cmu`; LFP = NMC)
| SG | λ_SR | λ_RF | λ_MPF,latent | SPFM | Ziel | LFM | Ziel | PMHF-Beitrag |
|---|---|---|---|---|---|---|---|---|
| SG-01 (ASIL D) | 28,80 FIT | 0,020 FIT | 0,943 FIT | 99,93 % | 99 % ok | 96,72 % | 90 % ok | 0,020 FIT |
| SG-02 (ASIL C) | 33,58 FIT | 0,721 FIT | 0,720 FIT | 97,85 % | 97 % ok | 97,81 % | 80 % ok | 0,721 FIT |

Vorher (v0.1): SG-01 SPFM 99,92 %, LFM 98,14 %; SG-02 SPFM 95,71 %, LFM 100,00 % (Ziel verfehlt). Ziele jetzt: alle erreicht.
Pack (Block `pack`, nur CMU-Platinen): PMHF-Beitrag SG-01 LFP 0,280 FIT (14 CMU), NMC 0,260 FIT (13); SG-02 LFP 10,09 FIT, NMC 9,37 FIT.
Top-5 SG-02 (FIT je CMU, Rest + latent): Ausgleichs-FET Kurzschluss D-S (x18) 0,720; AFE Ausgleich haengt an (x1) 0,400; Ausgleichswiderstand Kurzschluss (x36) 0,108; AFE Messfehler (x1) 0,100; Filterkondensator Zellabgriff Kurzschluss (x18) 0,036.
Top-5 SG-01: Sekundaerschutz loest nicht aus (x3) 0,750; AFE Messfehler (x1) 0,100; Filterkondensator Zellabgriff Kurzschluss (x18) 0,036; Filterwiderstand Zellabgriff offen (x19) 0,034; Filterwiderstand Zellabgriff Drift (x19) 0,017.
Kein Ziel verfehlt, daher kein Was-wäre-wenn (Block `massnahmen` leer).

## Abgleich ERW-E3 Nachtrag 7
| Erwartung | Befund | Urteil |
|---|---|---|
| SG-02 SPFM 97,85 % (Ziel ≥ 97 %) | 97,85 % | ok |
| SG-01 weiter ≥ 99 % / ≥ 90 % | SPFM 99,93 %, LFM 96,72 % | ok; LFM sinkt von 98,14 auf 96,72 %, weil 3 statt 1 Sekundärschutz-IC latent ausfallen können (0,75 statt 0,25 FIT) |

## Offene Fragen an Opus
1. Der Doppel-N-FET wird mit 1 FIT je Gehäuse gerechnet (wie der Einzel-FET). Ein Gehäuse mit zwei FETs könnte höher liegen; keine FIT-Annahme dafür in der ERWARTUNG.
2. Die Einstufung „Kurzschluss eines der beiden FETs = latenter Zweitfehler, DC 90 %“ übernimmt die Annahme aus v0.1 (M1). Gleichzeitiger Kurzschluss beider FETs und gemeinsame Ursache im Gehäuse sind nicht betrachtet.
3. Der zweite Gate-Ausgang je Kanal ist am AFE ein generischer Pin (kein Bauteilbeleg); „AFE Ausgleich hängt an“ bleibt mit vollem IC-Anteil angesetzt (0,40 FIT).
4. Weitere offene Fragen 2 bis 6 aus v0.1 (konservative Einstufungen, Kommunikationsausfall sicher, PMHF nur RF-Term, SG-07 und SG-03 nicht Umfang, Pack nur CMU) gelten unverändert.

## Dateien
`fmeda.py` (neu geschrieben und ersetzt, `e3c` liest nur), `fmeda_bericht.py`, `bild.py`, `fmeda_LFP.csv`, `fmeda_NMC.csv`, `ergebnis.json`, `e3d_fmeda.png`, `lesehilfe.md`, Folienbaustein `praesentation/bausteine/E3d.md`.

*KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.*
