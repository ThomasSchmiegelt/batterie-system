| Dok.-Nr. | BAT-DOC-05 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Risiken (FMEA-Vorlage) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

Bewertung B (Bedeutung), A (Auftreten), E (Entdeckung) je 1–10; RPZ = B·A·E. Zahlen erst mit Begründung eintragen.

## Produkt
| Nr | Fehler | Folge | Ursache | Maßnahme / Nachweis | B | A | E | RPZ |
|---|---|---|---|---|---|---|---|---|
| RIS-001 | thermisches Durchgehen einer Zelle | Brand, Ausbreitung | Innenkurzschluss, Überladung, Beschädigung | Barriere (P04), Entgasung (P05), BMS (P07); Nachweis nach Norm | – | – | – | – |
| RIS-002 | ungleiche Kühlung | Alterung, Leistungsgrenze | Verteiler, Wärmeleitpaste | Verteilerauslegung (Lehre 1), Elmer | – | – | – | – |
| RIS-003 | Verbinder überhitzt | Ausfall, Brand | Querschnitt, Schweißnaht | Verlustrechnung, Prüfung | – | – | – | – |

## Prozess (KI-Einsatz)
| Nr | Fehler | Folge | Maßnahme |
|---|---|---|---|
| RIS-K01 | erfundene Zahl oder Quelle | falsche Auslegung | Beleg Pflicht, pruefe.py, Prüfung an Rohdaten (REQ-D01) |
| RIS-K02 | Ergebnis falsch gedeutet (z. B. zu kurze Rechnung) | falsche Entscheidung | Erwartung vorher, Opus prüft (Fusion B-061) |
| RIS-K03 | eingeschleuste Anweisung in fremden Texten | Datenabfluss, Schaden | PI ohne Werkzeuge (ENT-001) |
| RIS-K04 | Absturz der Sitzung bricht Rechnungen ab | Zeitverlust | losgelöst starten, paketweise speichern |
| RIS-K05 | Lizenz- oder Schutzrechtsverstoß | rechtlich | BAT-DOC-10, keine FTO-Aussage durch KI |
| R-PLAT | 2026-11-17 | 4680: Lithium-Ablagerung an der Anode beim Schnellladen 1,5C (Modell: Anodenpotential < 0 V schon bei 1C, generischer Satz Chen2020) | Alterung, Kurzschluss | 4 | 7 | 6 | Ladestrom vom BMS nach Anodenpotential-Beobachter begrenzen; 4680-Messdaten beschaffen (C3); Ladezeit 32–33 min als Rückfall | B-BAT-023 | offen |
| R-4680W | 2026-11-17 | 4680: Wärme beim 30-min-Laden zwischen 7,4 W (Modell) und 11,5 W (I·ΔU); im ungünstigsten Fall Spreizung 6,5 K > 5 K | REQ-P09 verfehlt | 4 | 5 | 5 | Auslegung Modellwärme (Autor 2026-11-17), I·ΔU mitführen; Kalibrierung mit Messdaten | B-BAT-023 | offen |

---
*KI-generiert (Claude Opus, 2026-11-11). Status Entwurf. Freigabe nur durch den Autor.*
