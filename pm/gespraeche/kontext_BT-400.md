# Kontext für das Bauteilgespräch: BT-400 Verkabelung und Zellverbinder

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Verkabelung und Zellverbinder (BT-400). Aufgabe: leitet den Hochvoltstrom von Zelle zu Zelle und zur Schaltbox. Teil von: BT-000. Meine Teile: BT-410 Zellverbinder, BT-420 Reihenverbinder, BT-430 HV-Hauptleitung, BT-440 Stromschiene, BT-450 Berührschutz.

## Meine Merkmale (Wert und entscheidende Akte)

## Anforderungen an mich (Lastenheft)
| REQ-P04 | Dauer- und Spitzenleistung Entladen | offen (kW, s) | Autor | Muss | offen |
| REQ-P13 | Schutzart, Isolation, Berührschutz | nach Norm | Norm | Muss | offen |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-004 Bauteilbaum bis Stücklistenebene; Schutzteile in Schaltbox unter BT-700 (2026-11-16, entschieden (Mensch), Opus (Vorschlag) / Autor (Freigabe 2026-11-16); Variante: alle)
Merkmal: - = None ; Anforderungen: REQ-D11, REQ-D12, REQ-D13; Belege: B-BAT-004
## Frage
Wie fein wird der Bauteilbaum, damit jedes Teil der Batterie eine Akte und damit ein Maß fürs CAD bekommen kann? Und wohin gehören Schütze, Sicherung, Vorladung, Stecker und Entgasung, die bisher in BT-700 (struktur.json) und in BT-400/BT-500 (Stückliste) standen?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| Baum bleibt bei 8 Baugruppen, Merkmale direkt an der Baugruppe (z. B. `quertraeger_breite_mm` an BT-500) | kein Umbau | sehr lange Merkmallisten; Bauteilgespräch und Video können einzelne Teile nicht zeigen; Stückliste und Baum bleiben getrennt |
| Baum bis Normteilebene (Schrauben, Dichtringe) | vollständig | viel Pflegeaufwand ohne Nutzen für Auslegung und Video; Autor: „muss nicht auf eine Schraube runtergebrochen werden“ (stueckliste.py) |
| **Baum bis Stücklistenebene (gewählt)**: je Stücklistenposition ein Bauteil, Zelle zusätzlich mit 4 Detailteilen fürs Video | jede Position hat Merkmale und Akte; `stueckliste.py` prüft die Zuordnung in beide Richtungen | 46 statt 8 Bauteile; Merkmale sind ein Vorschlag und wachsen mit der Auslegung |
| Schutzteile unter BT-400 lassen (wie Stückliste) | keine Umnummerierung | widerspricht der Rolle von BT-700 und Videoszene 7 (video/STORYBOARD.md) |
| **Schutzteile unter BT-700, Schütze, Vorladung und Sicherung in einer Schaltbox BT-710 (gewählt)** | folgt der ursprünglichen Bauteilrolle und dem Storyboard; die Schaltbox ist ein Bauraum, den G4 platzieren muss | Stückliste umnummeriert (400.4–400.9 und 500.7 → 700.2–700.8, alte 700.1–700.3 → 700.9–700.11, 500.8 → 500.7) |
## Entscheidung und Begründung
Vorschlag: `pm/bauteile/struktur.json` mit 46 Bauteilen (BT-000 bis BT-780). Jedes Bauteil der Stückliste trägt das Feld `stueckliste` mit seiner Position. `stueckliste.py` bricht ab, wenn eine Position kein Bauteil hat oder umgekehrt. Merkmale gibt es nur dort, wo CAD (Maße), Elektrik (Strom, Querschnitt), Kühlung oder Mechanik sie brauchen. Alle Werte sind `null`, bis eine eigene Akte entscheidet. Grund: REQ-D11 (CAD-Maße nur aus Akten) ist nur erfüllbar, wenn jedes Teil Merkmale hat (B-BAT-004 Punkt 1). REQ-D12 und REQ-D13 brauchen einzelne Teile zum Zeigen und Begründen.
Vorherige Fassung: Scratchpad-Sicherung `struktur_v1_2026-11-11.json`. Inhalt der 8 alten Bauteile unverändert, nur Merkmale ergänzt.
## Folgen
- Neue Merkmale an bestehenden Bauteilen: BT-000 (Energie, Spannung, Bauraum, Masse), BT-100 (format, nennspannung_V, masse_g), BT-200 (reihen_anzahl), BT-300 (architektur), BT-500 (bauweise), BT-600 (kuehlart).
- Gleiche Größe darf nur an einer Stelle entschieden werden. Zellzahl je Reihe: BT-210 `zellen_je_reihe`. Gesamtzahl: BT-200 `zellen_anzahl`. Querträgeranzahl: BT-530 `anzahl`. Die Folgegrößen rechnet ein Skript, nicht eine zweite Akte.
- Video (Szenen 1–8) und Bauteilgespräch können jetzt jedes Teil einzeln zeigen (`pm.py kontext BT-530`).
- Risiken: keine neuen.

## Befund B-BAT-004
B-BAT-004 (2026-11-16) Analyse: Was fehlt für die komplette Batterie (Struktur gegen Information)
Fundstellen: `pm/bauteile/struktur.json`, `stueckliste.json`, `parameter.json`, `pm/startwerte.json`, `pm/entscheidungen/`, `forschung/ergebnis/*.pruefung.txt`. Erwartung: entfällt (Bestandsaufnahme, keine Rechnung).
1. **Struktur zu flach.** struktur.json hat 8 Bauteile. Merkmale gibt es nur bei BT-100 (5) und BT-200 (2). BT-300 bis BT-700 haben keine. Die Stückliste hat 37 Positionen, aber keine davon ist ein eigenes Bauteil. Folge: Für Gehäuse, Querträger, Kühlplatte, Zellverbinder usw. kann `pm.py pruefe` keine Akte annehmen, also gibt es kein Maß fürs CAD. Das ist der Hauptblocker.
2. **Keine Maßentscheidung.** parameter.json: alle 7 Merkmale `null`. ENT-001…003 betreffen Methoden. ENT-002 (PyBaMM) steht noch auf „vorgeschlagen“.
3. **Widerspruch Energie.** startwerte.json: 73,9 kWh brutto. stueckliste.json: 79,9 kWh (219s1p × 100 Ah × 3,65 V, beide Zellwerte Annahme). Die Zellzahl ist auf ganze Reihen gerundet, die Energie aber nicht zurückgeführt.
4. **Widerspruch Chemie gegen Vorbild.** Die Startwerte wählen NMC, weil die LFP-Packdichte als 180 Wh/L **angenommen** ist (startwerte.py, „Zelle × Füllgrad ~0,6“, unbelegt), nötig wären 214 Wh/L. Die Recherche belegt für Blade-LFP nur Werte je kg (190–210 Wh/kg Zelle, W03), keinen Wert je Liter. Die Stückliste führt deshalb eine „lang prismatische NMC-Zelle“. Für dieses Format gibt es in der Recherche keinen Beleg, das Blade-Fo

