# ERWARTUNG G5 (ERW-G5): Geometrie aus der Stückliste

| Nummer | ERW-G5 | Version 0.1 | Status: Entwurf | Ersteller: Claude Opus (2026-11-19) | Prüfer: offen |
|---|---|---|---|---|---|

Vor der ersten Montage festgelegt. Abweichungen werden begründet, nicht weggerechnet.

| Größe | Erwartung | Begründung | Toleranz |
|---|---|---|---|
| Positionen SL3 je Variante | LFP ≈ 50, NMC ≈ 55 | SL2 39 + 4.2 (≈ 10 neu, NMC +Verguss/Brücke/Berührschutz) | ± 8 |
| Masse LFP (nur Stücklistenregeln §4) | 621 kg (SL2 620 + Verbinder 249 statt 130: +0,9 kg + Normteile ≈ 1 kg − nichts) | Zellverbinder 1,0 kg × 249/130 = 1,9 kg | 615…630 kg |
| Masse NMC | 476 kg (SL2 471 + Verguss 11,4 schon in CAD, Zellabgriff ×2: +0,27 kg, Normteile ≈ 1 kg) | Verguss war in SL2 „fehlend“, im CAD-Wert 483 enthalten | 470…486 kg |
| Kühlplatten 2 Stück, echte Kanäle | LFP ≈ 75 kg statt 47 kg (+28) | Füllgrad aus K2-Geometrie (Blech 2 × 1,5 + Kanal 5 mm mit Steg 3/Teilung 7) = 0,64 statt Annahme 0,4 (A_KUEHLPLATTE_FUELLGRAD war mit 4-mm-Kanälen nicht vereinbar) | ± 5 kg |
| Seitenrahmen 3 Kammern | LFP ≈ 6–7 kg statt 21,8 kg (Vollprofil) | Fläche ≈ 28 % des Vollquerschnitts | ± 2 kg |
| Masse LFP mit G5-Geometrie | ≈ 633 kg (621 + 28 − 15) | Summe der Zeilen oben | 620…645 kg |
| Masse NMC mit G5-Geometrie | ≈ 488 kg (476 + 26 − 14) | gleiche Rechnung, Platte etwas kürzer | 475…500 kg |
| Masse CAD gegen SL3 | ≤ 1 % | gleiche Quelle (Volumen × Dichte) | 3 % → Rückgabe |
| Höhe max. über Deckel | LFP ≤ 130 mm am Pol, Schaltbox-Turm ≤ 210 mm (beide) | M0-Grenze, Autor | hart |
| Schaltbox Innenhöhe | ≤ 90 mm mit liegenden Schützen | Schütz liegend ≈ 60…75 mm hoch (Annahme bis W34) | ± 10 mm |
| Positionen in Stufe H | ≤ 5 % | nur ohne jede Formangabe | – |
| Kollisionen | 0 (Kontaktflächen erlaubt) | | hart |
| Laufzeit Montage | LFP ≈ 2 min, NMC ≈ 10 min (868 Zellen, 1736 Abgriffe) | wie pack_e2d | Faktor 3 |

---
*KI-generiert (Claude Opus, 2026-11-19).*

## Nachtrag 1 (2026-11-19, vor der Gesamtmontage): Blech-Kühlplatte (ENT-152…156) und Kühlkreis
| Größe | Erwartung | Begründung |
|---|---|---|
| Kühlplatten 2 Stück | 46–48 kg (statt 75,5) | K2b 46,6 kg; Teillauf 47,3 kg vor dem Verteilerausschnitt |
| Höhe Packdeckel LFP | 117 mm (−4) | 2 × (8 → 6 mm) |
| Kühlkreis außen (Pumpe, Ventil, Chiller, Behälter, Schläuche, T) | ≈ 3,3 kg ohne Kühlmittel | Annahmen A_g5_*_masse_kg + EPDM |
| Länge mit Kühlmodul | Pack 2050 + 245 mm (LFP) | Stutzen 40 + Abstand 60 + Geräte 120 + Bögen |
| Masse LFP gesamt | ≈ 607 kg (633 − 28 − 1 + 3) | Kühlplatte zurück auf ≈ K2-Niveau, Kühlkreis neu |
