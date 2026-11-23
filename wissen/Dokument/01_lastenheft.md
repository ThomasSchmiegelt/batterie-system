---
typ: dokument
nr: "BAT-DOC-01"
version: "0.1"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-01 – Lastenheft

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/01_lastenheft`
- Version: 0.1
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-D01|REQ-D01]]
- [[Anforderung/REQ-D02|REQ-D02]]
- [[Anforderung/REQ-D03|REQ-D03]]
- [[Anforderung/REQ-D04|REQ-D04]]
- [[Anforderung/REQ-D05|REQ-D05]]
- [[Anforderung/REQ-D06|REQ-D06]]
- [[Anforderung/REQ-D07|REQ-D07]]
- [[Anforderung/REQ-D08|REQ-D08]]
- [[Anforderung/REQ-D09|REQ-D09]]
- [[Anforderung/REQ-D10|REQ-D10]]
- [[Anforderung/REQ-D11|REQ-D11]]
- [[Anforderung/REQ-D12|REQ-D12]]
- [[Anforderung/REQ-D13|REQ-D13]]
- [[Anforderung/REQ-D14|REQ-D14]]
- [[Anforderung/REQ-P01|REQ-P01]]
- [[Anforderung/REQ-P02|REQ-P02]]
- [[Anforderung/REQ-P03|REQ-P03]]
- [[Anforderung/REQ-P04|REQ-P04]]
- [[Anforderung/REQ-P05|REQ-P05]]
- [[Anforderung/REQ-P06|REQ-P06]]
- [[Anforderung/REQ-P07|REQ-P07]]
- [[Anforderung/REQ-P08|REQ-P08]]
- [[Anforderung/REQ-P09|REQ-P09]]
- [[Anforderung/REQ-P10|REQ-P10]]
- [[Anforderung/REQ-P11|REQ-P11]]
- [[Anforderung/REQ-P12|REQ-P12]]
- [[Anforderung/REQ-P13|REQ-P13]]
- [[Anforderung/REQ-P14|REQ-P14]]
- [[Anforderung/REQ-P15|REQ-P15]]
- [[Anforderung/REQ-P16|REQ-P16]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Bauteil/BT-100|BT-100]]
- [[Entscheidung/ENT-005|ENT-005]]
- [[Entscheidung/ENT-006|ENT-006]]
- [[Entscheidung/ENT-007|ENT-007]]
- [[Entscheidung/ENT-012|ENT-012]]
- [[Entscheidung/ENT-030|ENT-030]]

## Vorgänge, die dieses Dokument nennen
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/V2|V2]] – Freigabe Lastenheft durch Autor

## Inhalt (Kopie aus `docs/01_lastenheft.md`)

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
| REQ-P03 | Systemspannung (Nenn, min, max) | 800 V nominal (ENT-006, Autor 2026-11-16); U_nenn 720–880 V, U_min und U_max ausweisen (Autor, Freigaberunde 2026-11-23) | Autor | Muss | festgelegt |
| REQ-P04 | Dauer- und Spitzenleistung Entladen | P_spitze 10 s nach Startwert, P_dauer ≥ 60 kW (Autor, Freigaberunde 2026-11-23) | Autor | Muss | festgelegt |
| REQ-P05 | Schnellladen 10 → 80 % | LFP 20 min, NMC-4680 30 min (Autor 2026-11-17 „30 minuten“, nach K1b; Variantenunterschied) | Autor | Muss | festgelegt |
| REQ-P06 | Zellchemie | zwei Varianten gleicher Spezifikation (Autor 2026-11-16): LFP-Blade prismatisch (ENT-005) und NMC811-Rundzelle 4680 (ENT-007…011); Baum ENT-012 | Autor | Muss | entschieden |
| REQ-P07 | Bauraum (L × B × H) und Masse | L ≤ 2400 mm; B = 1430 mm (ENT-030, Autor 2026-11-17); H ≤ 130 mm im Zellbereich, Dom Schaltbox ≤ 250 mm; Masse LFP ≤ 528 kg, NMC ≤ 370 kg (Startwerte als Ziel) (Autor, Freigaberunde 2026-11-23) | Autor | Muss | festgelegt |
| REQ-P08 | Umgebungstemperatur Betrieb und Laden | Betrieb −20 … +45 °C, Laden 0 … +45 °C (Vorheizen unter 0 °C) (Autor, Freigaberunde 2026-11-23) | Autor / Norm | Muss | festgelegt |
| REQ-P09 | max. Zelltemperatur und Spreizung | T_max ≤ 45 °C, Spreizung ΔT ≤ 5 K zwischen den Zellen (Autor, Freigaberunde 2026-11-23); Nachweis neu auswerten (Schleife 2) | Autor | Muss | festgelegt |
| REQ-P10 | Lebensdauer (Zyklen, Jahre, Restkapazität) | SOH ≥ 70 % nach 200.000 km (Autor, Freigaberunde 2026-11-23) | Autor | Soll | festgelegt |
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |
| REQ-P12 | Kühlmittel und Anschlüsse | Wasser-Glykol, Δp je Platte ≤ 0,5 bar, Verteilung ±10 % (Autor, Freigaberunde 2026-11-23) | Autor | Soll | festgelegt |
| REQ-P13 | Schutzart, Isolation, Berührschutz | IP67, R_iso ≥ 100 Ω/V (UN R100) (Autor, Freigaberunde 2026-11-23) | Norm | Muss | festgelegt |
| REQ-P14 | Mechanik: Stoß, Schwingung, Crash | Zellverschiebung ≤ 0,5 mm bei Pfahl 5 kJ und Quetschung nach R100 (100–105 kN) (Autor, Freigaberunde 2026-11-23) | Norm | Muss | festgelegt |
| REQ-P15 | Messung und BMS: Zellspannung, Temperatur, Isolationswächter | Messumfang: Zellspannung je Reihe, Temperaturfühler, Isolationswächter (Stücklistenposition) (Autor, Freigaberunde 2026-11-23) | Autor | Muss | festgelegt |
| REQ-P16 | Herstellkosten je Variante ausweisen (€/kWh Pack, Anteile je Baugruppe) | kein Zielwert (Autor 2026-11-18: „lass offen“); Preise als Schätzung oder verifiziert kennzeichnen | Autor (2026-11-18) | Soll | vorgeschlagen |

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

