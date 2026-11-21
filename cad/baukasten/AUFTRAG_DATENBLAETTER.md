# AUFTRAG G5.5b (Sonnet): Datenblätter der Kaufteile beschaffen und Maße herausziehen

KI-generiert (Claude Opus, 2026-11-19). Autor 2026-11-19: „besorge dir die datenblätter, schreibe mir ggf eine liste welche ich für dich herunterladen muss“. Anforderungen: REQ-P13, REQ-D12, REQ-P16.

**Ziel:** Für jedes Kaufteil ein öffentlich zugängliches Datenblatt eines realen, passenden Typs (800 V, Ströme laut Akten/E1). Daraus die Maße für die Geometrie der Stufe F und, wo öffentlich, ein Einzelpreis bei einem Distributor.

**Ablage:** PDFs nach `quellen/datenblaetter/<BT>_<hersteller>_<typ>.pdf`. `quellen/` ist in .gitignore, fremde Inhalte kommen nicht ins Repo. Herunterladen mit `curl -L --fail -A "Mozilla/5.0"`, ohne persönliche Angaben. Danach `pdftotext -layout` und die Maßzeichnung lesen. Hat die Zeichnung nur Bilder, die Seite mit dem Read-Werkzeug als Bild ansehen.

| BT | Teil | Anforderung (aus Akten/E1) | Kandidaten (Beispiele, frei wählbar) |
|---|---|---|---|
| BT-711 | Hauptschütz | ≥ 800 V DC, LFP 250 A Dauer (E1), NMC ≈ 190 A | TE Kilovac EVC 250/500-800, Gigavac HX/GX, Hongfa HFZ16V, Panasonic AEV |
| BT-712 | Vorladeschütz + Vorladewiderstand | 800 V, ≈ 10–30 A | TE LEV100, Gigavac GV200; Widerstand Vishay/Arcol HS/RH Alu-Gehäuse |
| BT-713 | Pyrosicherung | 800 V, ≥ 250 A | Autoliv PSS, Mersen Pyrofuse, Littelfuse, Eaton Breaktor/Pyro |
| BT-713 | Schmelzsicherung 40 A | 1000 V DC, 40 A, EV | Eaton Bussmann EVK/EV-Serie, Mersen EV, Littelfuse |
| BT-340 | Shunt | ≥ 300 A, 800 V, mit Messelektronik | Isabellenhütte IVT-S/IVT-Mod, BAS, Vishay WSBE |
| BT-350 | Isolationswächter | 800 V Fahrzeug | Bender ISOMETER iso165C, Sensata |
| BT-720 | Service-Trennstecker (NMC) | 800 V, ≥ 200 A, HVIL | TE AMP+ MSD, Amphenol MSD, Rosenberger |
| BT-730 | HV-Steckverbinder 250 A und 40 A | 800 V, HVIL | TE HVA 280/HVP 800, Amphenol PowerLok/HVSL, Rosenberger HPK |
| BT-740 | NV-Steckverbinder 26-polig | Kfz, abgedichtet | TE MQS/Superseal, Molex MX150 |
| BT-570 | Druckausgleichselement | Batteriegehäuse, IP67 | Gore PolyVent/Automotive Vents, Donaldson |
| BT-750 | Entgasungsventil | Thermal Runaway, Batteriegehäuse | Gore Degassing Unit, Eaton Battery Vent, Freudenberg |
| BT-770 | Gas-/Drucksensor | Thermal-Runaway-Erkennung | Amphenol SGX, Sensata BTRS, Honeywell BES, TE |
| BT-640 | Temperaturfühler Kühlmittel | Wasser-Glykol, NTC, Einschraub- oder Clip | TE, Sensata, Amphenol (NTC Kühlmittel) |
| BT-330 | NTC Zelle | auf FPC | Vishay/TDK NTC SMD 0603/0805 |
| BT-590 | Kabelschuh M8, 50 mm² und 35 mm² | DIN 46235 | Klauke, Cembre |

**Ausgabe:** `forschung/datenblaetter.md` mit Kopf (KI-generiert Sonnet, Entwurf) und je Teil:
| BT | Hersteller, Typ | Quelle (URL des PDF), Abrufdatum | Datei in quellen/ | Hüllmaß L × B × H (mm) | Befestigung (Löcher, Abstand) | Anschlüsse (Bolzen M?, Abstand, Lage) | Masse (g) | Seite im PDF | Preis (EUR/USD, Menge, Distributor, Datum) oder „nicht öffentlich“ |
Jede Zahl mit Seite. Keine Werte aus dem Gedächtnis. Fehlt ein Wert, „fehlt“ eintragen.

**Nicht ladbar** (Login, Formular, Captcha, 403): Lass das Teil aus und trag es in `forschung/datenblaetter_fuer_autor.md` ein: Teil, Typ, Seite des Herstellers mit genauer URL, Grund. Der Autor lädt diese Dateien von Hand nach `quellen/datenblaetter/`.

**Zusätzlich:** Je Datei eine Zeile in docs/10_lizenzen_und_quellen.md (Quelle, Lizenz „Herstellerdatenblatt, nur intern, nicht im Repo“, Ablage).

**Abbruch:** nach höchstens 2 Versuchen je Teil, Gesamtzeit ca. 60 min. Rückgabe ≤ 6 Zeilen: wie viele Teile mit Maßen, wie viele mit Preis, wie viele auf der Liste für den Autor. Nicht deuten, keine Akten, keine Änderung an cad/.
