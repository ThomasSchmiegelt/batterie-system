| Dok.-Nr. | ERW-E3d | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung E3d: grobe FMEDA der CMU-Platine (ISO 26262-5, Grobentwurf) | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-24). Umfang vom Autor festgelegt (F-S6, Freigaberunde 2026-11-24). ISO 26262 und die Ausfallratenkataloge (SN 29500, IEC 61709) liegen **nicht** vor. Alle FIT-Werte, Ausfallartenanteile und Diagnosedeckungen sind **Annahmen Opus aus dem Gedächtnis (Größenordnung)**, Herkunft „ERW-E3d“.

## Anforderung
REQ-P18

## Eingaben
`sim/elektrik/e3_platine/cmu_<V>_bom.csv` (108 Teile), HARA `docs/24` (SG-01 ASIL D, SG-02 ASIL C), FSR-01/02/06.

## Annahmen Opus (ERW-E3d)
| Bauteil | FIT | Ausfallarten (Anteil) |
|---|---|---|
| Widerstand Chip | 0,3 | offen 60 %, Kurzschluss 10 %, Drift 30 % |
| Kondensator MLCC | 0,5 | Kurzschluss 40 %, offen 30 %, Drift 30 % |
| MOSFET klein | 1 | Kurzschluss D-S 40 %, offen 40 %, Drift 20 % |
| TVS-Diode | 1 | Kurzschluss 60 %, offen 40 % |
| AFE-IC | 20 | „Messfehler“ 50 %, „Ausfall Kommunikation“ 30 %, „Ausgleich hängt an“ 20 % |
| Sekundärschutz-IC | 5 | „löst nicht aus“ 50 %, „löst falsch aus“ 50 % |
| Übertrager | 2 | offen 70 %, Kurzschluss Wicklung 30 % |
| Stecker | 2 | offen 70 %, Kurzschluss benachbarter Pins 30 % |
| NTC-Eingang | 1 | offen 50 %, Kurzschluss 50 % |

Diagnosedeckung (Annahme): AFE-Selbsttest und Plausibilisierung 99 % für Messfehler; Leitungsbruch-Diagnose 99 % (FSR-02); Ausgleichsstrom-Überwachung über die Zellspannung 90 %; Sekundärschutz deckt AFE-Messfehler für SG-01 unabhängig ab (latent, Prüfung beim Start 90 %).

## Methode
Je Bauteil und Ausfallart: verletzt sie SG-01 oder SG-02? Einzelfehler, Restfehler, latenter Mehrfachfehler oder sicher? SPFM = 1 − Σ(SPF+RF)/Σλ_sicherheitsrelevant, LFM = 1 − Σλ_MPF,latent / Σ(λ_sicherheitsrelevant − λ_SPF − λ_RF). Je SG getrennt. Ergebnis je CMU und für das Pack (14 bzw. 13 CMU).

## Erwartung
1. **SG-01 (Überladung):** SPFM ≥ 99 %, weil der Sekundärschutz unabhängig ist. LFM ≈ 90 %, abhängig vom Starttest des Sekundärschutzes. Zielwerte ASIL D: SPFM ≥ 99 %, LFM ≥ 90 %.
2. **SG-02 (Tiefentladung):** Ein Kurzschluss im Ausgleichs-FET oder ein hängender Ausgleich im AFE entlädt die Zelle dauernd. Das ist der **dominierende Restfehler**. Mit 90 % Überwachung ergibt sich SPFM ≈ 95–98 %, unter dem ASIL-C-Ziel von 97 % möglich. Dann folgt eine Maßnahme als Vorschlag, z. B. zweiter Schalter in Reihe = OPT oder bessere Diagnose.
3. PMHF-Beitrag je CMU ≈ 0,1–1 FIT.

## Abbruch → OPUS
Ziel verfehlt (dann Maßnahme vorschlagen, nicht umsetzen); Bauteil ohne Annahme in der Tabelle.
