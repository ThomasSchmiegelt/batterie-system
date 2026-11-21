# AUFTRAG K2b (Sonnet): Blech-Kühlplatte 1/4/1 mm mit Mäander

KI-generiert (Claude Opus, 2026-11-19). Erwartung: ERWARTUNG.md „Nachtrag K2b“. Akte ENT-152. REQ-P05, REQ-P09.
1. kuehlplatte.py um eine Funktion `k2b()` erweitern (die alten Funktionen bleiben unverändert). Sie nutzt `kanal()` usw. mit Hk = 4 mm und Blech 1 mm. Varianten nach Nachtrag K2b: n ∈ {2,4,6,8}, w ∈ {6,8,10,15,20,40}, Führung längs/quer, Varianten LFP/NMC. Teilkanäle je Bahn: m = floor((Bahnbreite + Steg)/(w + Steg)). Bahnbreite = (Plattenmaß quer zur Bahn − (n−1) × Trennsteg 3 mm)/n. Kanallänge je Bahn = Plattenmaß längs der Bahn. Gesamtweg = n × Bahnlänge. Umlenkung ζ = 1,5 je Umlenkung, bezogen auf die Bahngeschwindigkeit.
2. Ausgabe ergebnis_k2b.json: je Variante Re, h_Kanal, h_eff, U_gesamt, Δp (bar), P_hyd (W), ΔT_Kühlmittel, Masse beider Platten (Bleche + Stege, ρ 2700).
3. Bild k2b_U_dp.png: U über Δp, je n eine Farbe, Zielband U ≥ 500 und Δp ≤ 0,5 bar schattiert und beschriftet, Auswahl markiert. Lesehilfe als Abschnitt in k2_lesehilfe.md.
4. ERGEBNIS.md um den Abschnitt K2b ergänzen: Tabelle der 5 besten Varianten je Pack (Kriterium: U ≥ 500, kleinstes Δp), Abgleich mit jedem Punkt der Erwartung (erfüllt/verfehlt).
5. Folienbaustein praesentation/bausteine/K2b.md (Kernaussage 1 Satz, Bild, Zahlen mit Quellpfad).
Abbruch und Rückgabe an Opus: Erwartung verfehlt oder neue Annahme nötig. Nicht entscheiden, welche Variante gebaut wird, sondern nur vorschlagen. Rückgabe ≤ 5 Zeilen.
