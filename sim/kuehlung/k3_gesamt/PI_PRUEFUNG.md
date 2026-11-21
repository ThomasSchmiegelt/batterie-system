# PI-PRUEFUNG K3/K4 — KI-generiert (2026-11-21)
Zu ERWARTUNG.md. Ist-Werte mit Quelle (Datei, Schlüssel); Status = erfüllt/verfehlt. Keine Deutung.
Quellen: `ergebnis.json` (K3), `elmer_*/ergebnis.json` (K4), `ergebnis_film.json` (Nachtrag 3).

## Erwartungspunkte 1–5 (Hauptblock, 2026-11-20)
1. Δp je Platte ± 30 % von K2b — Ist: `dp_abw_prozent` = **231.9 %** (`ergebnis.json`; `dp_platte_bar_fx` 0.715 vs `dp_platte_bar_k2b` 0.215 bar) → **verfehlt**
2. h ± 30 % — Ist: `h_abw_prozent` = **−0.93 %** (`ergebnis.json`, `h_fx` 469.6 vs `h_k2b_Kanal` 474.0 W/m²K) → **erfüllt**.
   Totzonen < 5 % der Kanalfläche — Ist: `totzone_gesamt` = **0.0186** (Re 100), **0.0360** (Re 200) (`ergebnis.json`,`re.100/200`) → **erfüllt**
3. Kühlmittelaufwärmung ± 5 % — keine Temperatur in K3; Bilanz-Ist: `bilanz_abw_prozent` = **83325.9 %** (Re 100), **NaN** (Re 200) (`ergebnis.json`,`re.100/200`) → **verfehlt**
4. LFP Schnellladen T_max 33–37 °C — Ist: `T_max_C` = **42.56** (`elmer_LFP_P0_V0/ergebnis.json`) → **verfehlt**.
   ΔT im Pack 4–7 K — Ist: `dT_Zellblock_K` = **16.44** (`elmer_LFP_P0_V0/ergebnis.json`) → **verfehlt**.
   NMC T_max 35–40 °C — Ist: `T_max_C` = **34.12** (`elmer_NMC_P4_V0/ergebnis.json`) → **verfehlt**
5. T_max ≤ 45 °C — Ist: **42.56** (`elmer_LFP_P0_V0/ergebnis.json`) → **erfüllt**;
   ΔT ≤ 5 K — Ist: **16.44** (ebd.) → **verfehlt**

## Erwartungspunkte Film (Nachtrag 3, 2026-11-21)
1. Rückbahn-Fluss = Einlass ± 5 % — Ist: `punkt1_fluss_rueckbahn_zu_einlass` = **0.4897** (`ergebnis_film.json`) → **verfehlt**
2. Totzonen < 15 % Kammer, < 5 % Gebiet — Ist: `punkt2_totzone_anteil_kammer` = **0.0792**, `punkt2_totzone_anteil_gesamt` = **0.0139** (`ergebnis_film.json`) → **erfüllt**
3. Umlenkgleichverteilung innen +20 % / außen −20 % (Grenzen) — Ist: Min **0.9450**, Max **1.0090** (`ergebnis_film.json`,`punkt3_kanalfluss_rel_in_messebene_z241`) → **erfüllt** (innerhalb der Grenzen)
4. Temperatur qualitativ — kein Zahlenband; Ist: `nan` = **false**, `stationaer_aenderung_rueckbahn_letzte_durchlaufzeit` = **2.3e-4** (`ergebnis_film.json`) → keine Zahlenprüfung

## Logs (FEHLER/Error/Traceback)
Suche `grep -rni 'FEHLER|Error|Traceback' --include='*.log' .` (alle Laufordner inkl. Proben): **keine Treffer**.

KI-generiert (Claude, 2026-11-21). Nur Fakten aus den genannten Dateien, keine Deutung.
