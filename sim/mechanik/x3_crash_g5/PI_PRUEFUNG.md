# PI-PRÜFUNG X3 – Crash G5 (KI-generiert, 2026-11-23)
Vergleich: nummerierte Erwartungspunkte 1–4 aus ERWARTUNG.md (Basis 2026-11-20) gegen ergebnis.json.

## Erwartungspunkt 1: Energiebilanz-Fehler < 5 % (Pflicht)
| Fall | Ist (energiefehler_proz_max, ergebnis.json/<Fall>) | Urteil |
|---|---|---|
| LFP_a | 0.182 % | erfüllt |
| LFP_a2 | 0.230 % | erfüllt |
| LFP_a_s10 | 0.182 % | erfüllt |
| LFP_a_s40 | 0.184 % | erfüllt |
| NMC_a | 0.077 % | erfüllt |
| LFP_b, NMC_b, LFP_b_p2, LFP_b_t | null/NaN (ergebnis.json, Nachtrag 2: gilt für b nicht) | n. a. |

## Erwartungspunkt 2 (a): Pfahl 40–70 mm, erste Zellreihe 10–40 mm
| Fall | Pfahl (pfahl_eindringung_max_mm) | Zelle (zellreihe_eindringung_mm_Tiefste) | Urteil |
|---|---|---|---|
| LFP_a | 13.57 mm | 6.73 mm | verfehlt, verfehlt |
| LFP_a2 | 38.24 mm | 16.09 mm | verfehlt, erfüllt |
| LFP_a_s10 | 13.58 mm | 6.69 mm | verfehlt, verfehlt |
| LFP_a_s40 | 13.57 mm | 6.74 mm | verfehlt, verfehlt |
| NMC_a | 13.88 mm | 8.28 mm | verfehlt, verfehlt |
(Hinweis: Nachträge 1/3 ersetzen das Band für a durch 25–60 mm bzw. 15–40 mm; erwartet_pruefung in ergebnis.json: LFP_a2 pfahl_eindringung_im_Erwartungsband = false.)

## Erwartungspunkt 3 (b): bei 100 kN Rahmenverformung < 10 mm, Zellen < 2 mm
- LFP_b, ergebnis.json/LFP_b/bei_100kN: weg_platte 1.000001 mm, innenwand_mitte 0.3984485 mm, zellblock_vorderseite 0.0 mm, kraft_kN 284.627, zeit_ms 1.500001. b_rahmen_unter_10mm = true, b_zellen_unter_2mm = true → erfüllt.
- NMC_b, bei_100kN: weg_platte 1.000039 mm, zellblock_vorderseite 0.07405542 mm, b_rahmen_unter_10mm = true, b_zellen_unter_2mm = true → erfüllt.

## Erwartungspunkt 4: Rechenzeit LFP (a) 1–4 h CPU
- LFP_a, ergebnis.json/LFP_a/laufzeit_s_summe: 11548.9 s ≈ 3.2 h → erfüllt. (LFP_a2 11729.4 s ≈ 3.3 h, a_s10 11425.1 s, a_s40 12052.5 s ≈ 3.4 h.)

## Zeilen mit FEHLER/Error/Traceback in den Logs (lauf/, probe25.log)
1. lauf/LFP_b_instabil_N4/engine_2.log:1401352: `** RUN KILLED: ENERGY ERROR LIMIT REACHED`
2. lauf/LFP_b_instabil_N4/engine_3.log:1: `** ERROR: FILE X3_0002_0001.rst NOT FOUND`
3. lauf/LFP_b_instabil_N4/engine_3.log:2: `   ERROR TERMINATION`
4. starter.log jeder gültigen Läufe (LFP_a, LFP_a2, LFP_a_s10, LFP_a_s40, LFP_a_probe25, LFP_a_ungueltig_N3, LFP_b_instabil_N4, NMC_a, NMC_b): `0 ERROR(S)`
- Kein "FEHLER"- oder "Traceback"-Vorkommen in laufen/*.log, *.txt oder probe25.log.

— KI-generiert, Prüfskizze ohne Deutung; Prüfer Mensch (offen).
