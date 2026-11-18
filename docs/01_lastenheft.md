| Dok.-Nr. | BAT-DOC-01 | Version   | 0.1              | Status | Entwurf          |
| -------- | ---------- | --------- | ---------------- | ------ | ---------------- |
| Titel    | Lastenheft | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

## 1 Auftrag (wörtlich, Rechtschreibung korrigiert)
> „Ein komplettes Batteriesystem soll entwickelt werden. Mit Chemie der Zellen, geometrischer Darstellung der Zellen, Zusammenbau der gesamten Batterie, Auslegung der Elektrik, Kühlung der Batterie ist auch wichtig. Wissensaufbau und Patentrecherche.“ (Autor, 2026-11-11)
> „Das Ganze soll auch so eine Art Testprojekt für den gewerblichen Einsatz sein. Daher auch bitte Dokumentationsunterlagen entsprechend speichern, auch an Anforderungen denken.“ (Autor, 2026-11-11)
> Beispiel: BYD Blade Battery.

## 2 Produktanforderungen
Werte mit „offen“ legt der Autor fest. Bis dahin wird nicht ausgelegt. Ein Vorschlag ist keine Anforderung.

Vorschlagswerte für REQ-P01…P10 aus einem Startsatz: `docs/startparameter.md` (`python3 pm/startwerte.py "<Satz>"`). Freigabe nur durch den Autor.

| ID | Anforderung | Wert | Quelle | Priorität | Status |
|---|---|---|---|---|---|

| REQ-P01 | Anwendung / Fahrzeugklasse | Pkw, Fahrzeugmasse etwa 1500 kg, Anhaltswert (Autor 2026-11-16); Auslegung rechnet Fall A (mit Batterie) und Fall B (ohne Batterie) als Spanne | Autor | Muss | Vorgabe Autor |
| REQ-P02 | nutzbarer Energieinhalt | aus Reichweite 400 km (Vorgabe Autor 2026-11-16) × Verbrauch (Annahme), Vergleich sim/chemie/vergleich_lfp_nmc | Autor | Muss | Reichweite: Vorgabe Autor |
| REQ-P03 | Systemspannung (Nenn, min, max) | 800 V nominal (ENT-006, Autor 2026-11-16); min/max folgen aus Zellfenster | Autor | Muss | teilweise |
| REQ-P04 | Dauer- und Spitzenleistung Entladen | offen (kW, s) | Autor | Muss | offen |
| REQ-P05 | Schnellladen 10 → 80 % | LFP 20 min, NMC-4680 30 min (Autor 2026-11-17 „30 minuten“, nach K1b; Variantenunterschied) | Autor | Muss | festgelegt |
| REQ-P06 | Zellchemie | zwei Varianten gleicher Spezifikation (Autor 2026-11-16): LFP-Blade prismatisch (ENT-005) und NMC811-Rundzelle 4680 (ENT-007…011); Baum ENT-012 | Autor | Muss | entschieden |
| REQ-P07 | Bauraum (L × B × H) und Masse | L = 1950 mm (ENT-013, Autor 2026-11-17); B = 1430 mm (ENT-030, Autor 2026-11-17); H 130 mm Annahme; Masse offen (30 % Gesamtmasse als Annahme) | Autor | Muss | teilweise |
| REQ-P08 | Umgebungstemperatur Betrieb und Laden | offen (°C) | Autor / Norm | Muss | offen |
| REQ-P09 | max. Zelltemperatur und Spreizung | T_max ≤ 45 °C, Spreizung in der Zelle ≤ 5 K (Autor 2026-11-17) | Autor | Muss | festgelegt |
| REQ-P10 | Lebensdauer (Zyklen, Jahre, Restkapazität) | offen | Autor | Soll | offen |
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |
| REQ-P12 | Kühlmittel und Anschlüsse | Vorschlag Wasser-Glykol | Autor | Soll | offen |
| REQ-P13 | Schutzart, Isolation, Berührschutz | nach Norm | Norm | Muss | offen |
| REQ-P14 | Mechanik: Stoß, Schwingung, Crash | nach Norm | Norm | Muss | offen |
| REQ-P15 | Messung und BMS: Zellspannung, Temperatur, Isolationswächter | Umfang offen | Autor | Muss | offen |

## 3 Anforderungen an Entwicklung und Dokumentation (Testprojekt gewerblich)
| ID | Anforderung | Nachweis | Status |
|---|---|---|---|
| REQ-D01 | Jede Zahl ist rückverfolgbar (Rechnung mit Datei oder Quelle mit wörtlichem Beleg) | Prüfskripte, Stichprobe Opus | eingerichtet |
| REQ-D02 | Jedes Dokument hat einen Kopf nach BAT-DOC-00 und ist als KI-generiert gekennzeichnet | Durchsicht (Haiku) | eingerichtet |
| REQ-D03 | Jede Anforderung hat einen Nachweis in BAT-DOC-03 | Nachverfolgung | eingerichtet |
| REQ-D04 | KI-Einsatz protokolliert: Modell, Aufgabe, Prüfung | BAT-DOC-08 | eingerichtet |
| REQ-D05 | Freigabe nur durch den Menschen | Status in BAT-DOC-00 | eingerichtet |
| REQ-D06 | Erwartung vor jeder Rechnung, Vergleich danach | ERWARTUNG.md je Rechenordner | eingerichtet |
| REQ-D07 | Fremde Inhalte und Geheimnisse nicht im Repo, Lizenzen erfasst | .gitignore, BAT-DOC-10 | eingerichtet |
| REQ-D08 | Patentrecherche ohne rechtliche Bewertung; Freedom to Operate nur durch Fachleute | AUFTRAG_PATENTE.md | eingerichtet |
| REQ-D09 | Rechnungen reproduzierbar: Skript, Eingaben, Softwarestand (requirements.txt, Versionen) | SOFTWARE.md, Laufordner | eingerichtet |
| REQ-D11 | Jede Entscheidung als Akte an Bauteil und Merkmal gebunden; CAD-Maße nur aus diesen Akten | pm.py pruefe/parameter | eingerichtet |
| REQ-D12 | Bauteilgespräch: jedes Bauteil begründet seine Form mit Aktenverweisen | pm/gespraech.sh, Aktenprüfung | eingerichtet (Test BT-100) |
| REQ-D13 | Projektdokumentation als Abschlussvideo (Zelle → … → System) | video/STORYBOARD.md | geplant |
| REQ-D14 | Unternehmenspräsentation am Projektende, erzeugt aus den Projektdaten; jeder Vorgang liefert unterwegs seinen Folienbaustein | praesentation/STORYBOARD.md | geplant |
| REQ-D10 | Aufwand messbar: Laufzeiten und Agentenaufrufe je Arbeitspaket | BAT-DOC-08 | eingerichtet |

---
*KI-generiert (Claude Opus, 2026-11-11). Status Entwurf. Freigabe nur durch den Autor.*
