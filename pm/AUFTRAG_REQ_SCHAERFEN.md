# Auftrag Sonnet: Alle Anforderungen prüfbar machen (keine Bewertung „nicht definiert“)

KI-generiert (Claude Opus, 2026-11-23). Vorgabe des Autors: „"nicht definiert" darf es nicht mehr geben“.
Die Kriterien unten stammen von Opus. Wo der Autor keinen Wert gesetzt hat, sind es **Annahmen von Opus**. Sie werden auch so gekennzeichnet und gehen in die Freigaberunde.

## Regeln für das Werkzeug
1. Neues Feld je Kriterium: `herkunft_kriterium`: `"Autor"`, `"Startwert (Vorschlag)"`, `"Annahme Opus"` oder `"Norm (zu belegen Wxx)"`.
2. `verifikation.py`:
   - Die Stufe „nicht definiert“ fällt weg. Fehlt bei einer REQ ein Pflichtfeld (Messgröße, Ort, Lastfall, Methode, Ebene, Kriterium), bricht das Skript mit rc 1 ab und nennt die REQ. Das ist Tor T0, keine Bewertung.
   - Neuer Operator `"vorhanden"`: Der Schlüssel existiert in der Nachweisdatei und ist nicht leer. Gilt für „ausweisen“-Anforderungen.
   - Neuer Operator `"zwischen"` mit `wert: [min, max]`.
   - Hängt die Bewertung an einem Kriterium ohne Herkunft „Autor“, bekommt sie den Zusatz „(Kriterium Annahme, Autor offen)“.
   - Die Zählung bleibt mit den Stufen nachgewiesen, rechnerisch erfüllt (nicht validiert), verfehlt, offen und blockiert. Zusätzlich gibt es eine zweite Zählung „davon mit vom Autor bestätigtem Kriterium“.
3. Nachweise verknüpfst du nur mit vorhandenen Ergebnisdateien und Schlüsseln. Gibt es keine Rechnung, bleibt die Bewertung „offen“. Nichts rechnen, nichts schätzen.
4. `pm.py freigabe` führt jedes Kriterium ohne Herkunft „Autor“ als eigene Zeile.

## Kriterien je REQ (Opus)
| REQ | Messgröße / Ort / Lastfall | Kriterium | Herkunft | Methode / Ebene |
|---|---|---|---|---|
| P01 | Fahrzeugmasse der Auslegung / Fahrzeug / – | = 1500 kg | Autor | R / System |
| P02 | Energieinhalt brutto / Pack / 25 °C | ≥ Wert aus startwerte.json (Brutto-Vorschlag) je Variante | Startwert (Vorschlag) | A / System |
| P03 | U_nenn; U_min und U_max / Pack / SOC 0 und 100 % | U_nenn zwischen 720 und 880 V (±10 %); U_min und U_max „vorhanden“ | Autor (800 V) / Annahme Opus (Band ±10 %) | A / System |
| P04 | P_dauer, P_spitze 10 s / Pack / 25 °C, SOC 50 % | Werte aus startwerte.json, wenn vorhanden. Sonst P_spitze ≥ 150 kW 10 s und P_dauer ≥ 60 kW | Startwert / Annahme Opus | S / System |
| P05 | t 10→80 % / Pack / Start 25 °C | wie bisher. LFP `blockiert` (Zellparameter), NMC aus der Ergebnisdatei C2/K1 | Autor | S / System |
| P06 | Varianten gebaut / Pack / – | CAD-Ergebnis für LFP und NMC „vorhanden“ | Autor | I / System |
| P07 | L, B, H, Masse / Pack / – | B ≤ 1430; L ≤ 1950 (Lastenheft, Widerspruch B-BAT-045, nicht ändern); H ≤ 130 mm; Masse nach Stückliste im Zielband der Startwerte (Obergrenze) | Autor (L, B) / Annahme (H) / Startwert (Masse) | I / System |
| P08 | Umgebungstemperatur / Fahrzeug / Betrieb und Laden | Betrieb −20 … +45 °C, Laden 0 … +45 °C | Annahme Opus | S / System |
| P09 | wie bisher, Ort „Zelle“ | wie bisher | Autor | S / Subsystem |
| P10 | Restkapazität (SOH) / Pack / Laufleistung | SOH ≥ 70 % nach km_leben aus startwerte.json | Startwert (km) / Annahme Opus (70 %) | S / System |
| P11 | Zeit von der Warnung bis Feuer oder Explosion außerhalb des Packs / Pack / eine Zelle durchgehend | ≥ 5 min | Norm (zu belegen W35) | T / System |
| P12 | Kühlmittel; Δp je Platte; Durchflussverteilung / Kühlplatte / Schnellladen | Wasser-Glykol „vorhanden“; Δp ≤ 0,5 bar; Verteilung ≤ ±10 % (ergebnis_verteiler.json) | Annahme Opus (Δp) / ENT-159 (±10 %) | A / Subsystem |
| P13 | Isolationswiderstand; Schutzart / Pack / Neu, trocken | ≥ 500 Ω/V (DC); IP67 | Norm (zu belegen W35) / Annahme Opus (IP67) | T / System |
| P14 | Zellblockverschiebung / Zellen / Pfahl 5 kJ (X3 a) und Quetschung 100 kN (X3 b) | ≤ 0,5 mm (Kontaktspalt der Auswertung, KONTAKT_B) in beiden Fällen; Schwingung und Stoß: offen | Annahme Opus (Lastfälle zu belegen W35/W36) | S / System |
| P15 | Messumfang BMS / Pack / – | Zellspannung je Reihe, Temperaturfühler, Isolationswächter: als Stücklistenposition „vorhanden“ | Annahme Opus | I / Subsystem |
| P16 | Kosten je Variante und Anteil Schätzung / Pack / – | Summe und Anteil „vorhanden“ (pm/kosten/ergebnis_*.json) | Autor (kein Zielwert) | A / System |
| REQ-D | aus der Spalte „Nachweis“ des Lastenhefts | Prüfskript rc 0 oder Nachweisdatei „vorhanden“ (z. B. D04 docs/08, D13 video/abschluss.mp4, D14 praesentation/unternehmenspraesentation.pptx) | Autor | R / Prozess |
| G01 | Anwendbarkeit / – / – | „nicht anwendbar“ belegt (W37) | Norm (zu belegen W37) | R / System |

## Danach
`verifikation.py` laufen lassen, dann `pm.py freigabe`. `python3 praesentation/erzeuge.py` und PDF wie gehabt, die Folien 3 und 10 ansehen. Zeile in docs/08. Rückmeldung höchstens 5 Zeilen: Zählung je Bewertung, davon bestätigt, Zahl der Lücken T0 (Ziel 0).
