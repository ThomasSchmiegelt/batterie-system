| Dok.-Nr. | LH-E3d | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe Bild E3d (grobe FMEDA CMU-Platine) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.

**Lesehilfe zu e3d_fmeda.png:** Gefragt wird, wie sicher die Überwachungsplatine (CMU) gegen einzelne Bauteilfehler ist. Links stehen zwei Kennzahlen aus der Norm ISO 26262: SPFM sagt, welcher Anteil der gefährlichen Einzelfehler erkannt oder abgefangen wird, LFM sagt dasselbe für versteckte Fehler, die erst zusammen mit einem zweiten Fehler gefährlich werden. Höher ist besser. Die grünen Striche mit grünem Feld darüber sind die Ziele: SG-01 (Zelle nicht überladen, ASIL D) 99 % und 90 %, SG-02 (tiefentladene Zelle nicht laden, ASIL C) 97 % und 80 %. Liegt ein Balken unter dem Strich, ist das Ziel verfehlt (hier SG-02, SPFM). Die Achse beginnt bei 80 %, damit man die Unterschiede sieht. LFP und NMC sind gleich, weil beide Platinen dieselben Bauteilarten mit denselben Annahmen haben. Rechts stehen die fünf größten Beiträge zu den nicht abgefangenen Fehlern in FIT (1 FIT = ein Ausfall in einer Milliarde Betriebsstunden). Alle Ausfallraten und Erkennungsraten sind Annahmen von Opus aus dem Gedächtnis, nicht aus einem Katalog.
