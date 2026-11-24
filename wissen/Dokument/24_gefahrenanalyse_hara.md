---
typ: dokument
nr: "BAT-DOC-24"
version: "0.3"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-24 – Gefahrenanalyse und Risikobewertung (HARA) nach ISO 26262-3, Batteriesystem BT-000

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/24_gefahrenanalyse_hara`
- Version: 0.3
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-P01|REQ-P01]]
- [[Anforderung/REQ-P03|REQ-P03]]
- [[Anforderung/REQ-P11|REQ-P11]]
- [[Anforderung/REQ-P13|REQ-P13]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- [[Befund/B-BAT-055|B-BAT-055]]
- [[Bauteil/BT-000|BT-000]]
- [[Bauteil/BT-300|BT-300]]
- [[Bauteil/BT-310|BT-310]]
- [[Bauteil/BT-322|BT-322]]
- [[Bauteil/BT-325|BT-325]]
- [[Bauteil/BT-330|BT-330]]
- [[Bauteil/BT-340|BT-340]]
- [[Bauteil/BT-350|BT-350]]
- [[Bauteil/BT-360|BT-360]]
- [[Bauteil/BT-710|BT-710]]
- [[Bauteil/BT-711|BT-711]]
- [[Bauteil/BT-713|BT-713]]
- [[Bauteil/BT-715|BT-715]]
- [[Bauteil/BT-720|BT-720]]
- [[Bauteil/BT-770|BT-770]]

## Vorgänge, die dieses Dokument nennen
- [[Vorgang/S1|S1]] – Gefahrenanalyse HARA ISO 26262-3, Sicherheitsziele, FSR (BAT-DOC-24)

## Inhalt (Kopie aus `docs/24_gefahrenanalyse_hara.md`)

| Dok.-Nr. | BAT-DOC-24 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Gefahrenanalyse und Risikobewertung (HARA) nach ISO 26262-3, Batteriesystem BT-000 | Ersteller | Claude Opus (KI) | Prüfer | – (Autor offen) |

> **KI-generiert (Claude Opus, 2026-11-24).** Entwurf, nicht vom Menschen freigegeben. Auftrag Autor 2026-11-24: „Bei Gefahrenanalyse und und und mußt du mir helfen.“
> **Quellenlage:** Der Normtext ISO 26262 ist kostenpflichtig und liegt nicht vor. Die Methode (S/E/C-Klassen, ASIL-Tabelle) ist hier aus allgemein bekanntem Fachwissen wiedergegeben (**Annahme Opus, Beleg fehlt**). Recherche W45 ist beauftragt. Alle Einstufungen sind **Vorschläge**. Die Einstufung von Schwere, Häufigkeit und Beherrschbarkeit ist eine Abwägung und bleibt beim Autor (Fragen F-S1 … F-S6 am Ende).

## 0 Lesehilfe: was eine HARA ist, in fünf Schritten
1. **Betrachtungseinheit festlegen:** Was gehört dazu, was nicht? (§1)
2. **Fehlfunktionen sammeln:** Was kann das System *falsch* tun? Gemeint ist nicht ein Bauteildefekt, sondern das falsche Verhalten an der Grenze, z. B. „lädt weiter, obwohl die Zelle voll ist“. (§2)
3. **Mit Fahrsituationen kreuzen:** Dieselbe Fehlfunktion ist auf der Autobahn anders gefährlich als in der Garage. (§3)
4. **Jedes Paar bewerten:**
   - **S** Schwere: S0 keine Verletzung … S3 lebensgefährlich
   - **E** Häufigkeit der *Situation*, nicht des Fehlers: E1 sehr selten … E4 > 10 % der Betriebszeit
   - **C** Beherrschbarkeit durch Fahrer oder Umstehende: C0 immer … C3 kaum
   - Daraus folgt der **ASIL**. Faustregel: S + E + C = 10 → D, 9 → C, 8 → B, 7 → A, darunter QM (normale Qualitätssicherung).
5. **Sicherheitsziele ableiten:** Je gefährlichem Ereignis ein Satz „Verhindere …“ mit ASIL, sicherem Zustand und Fehlertoleranzzeit (FTTI). Daraus werden später die technischen Anforderungen an CMU, BMS und Schütze (§5). Das ist der Teil, der in E3 die Platine verändert.

## 1 Betrachtungseinheit (Item)
| | |
|---|---|
| Item | Hochvolt-Batteriesystem BT-000 (800 V, REQ-P03), Varianten LFP und NMC, Pkw ≈ 1500 kg (REQ-P01) |
| Funktionen | Energie speichern und abgeben (Antrieb, Laden), Zustand überwachen (BT-300), Hochvolt zu- und abschalten (BT-710), Warnung bei thermischem Ereignis (BT-770) |
| Gehört dazu | Zellen, Verschaltung, BMS mit Software, CMU, Schütze, Vorladung, Sicherungen, Isolationswächter, Kühlplatte im Pack |
| Gehört nicht dazu (Annahme, F-S1) | Umrichter, Ladegerät und Ladesäule, Kühlkreis außerhalb des Packs, Fahrzeugsteuergerät. Diese Teile kommen nur als Schnittstelle vor: Das Fahrzeug setzt Leistungsgrenzen um, die Ladesäule beendet das Laden auf Anforderung. |
| Annahme Fahrzeug | Fahrzeugseitig vorhandener Warnweg (Anzeige, Ton), Crash-Signal per CAN oder Leitung |

## 2 Fehlfunktionen an der Systemgrenze
| Nr | Fehlfunktion | typische Ursache im Item |
|---|---|---|
| FF-01 | Zelle wird über U_max geladen | Spannungsmessung falsch (AFE, Messleitung BT-360), Ladeende nicht gemeldet, Schütz verklebt |
| FF-02 | Zelle wird unter U_min entladen, danach wieder geladen | Messung falsch, Ruhestrom zu hoch, Ladesperre fehlt |
| FF-03 | Zelle über T_krit, oder Laden unter 0 °C ohne Vorheizen | Fühler BT-330 falsch oder ausgefallen, Kühlung aus, Ladefreigabe falsch |
| FF-04 | Überstrom / Kurzschluss wird nicht getrennt | Strommessung BT-340 falsch, Sicherung BT-713 falsch ausgelegt |
| FF-05 | Hochvolt wird während der Fahrt unerwartet getrennt | Fehlauslösung einer Schutzfunktion, Spannungsversorgung BMS fällt aus |
| FF-06 | Hochvolt wird nach Crash oder Abschaltbefehl nicht getrennt | Schütz verklebt, Crashsignal nicht erkannt |
| FF-07 | Isolationsfehler wird nicht erkannt | Isolationswächter BT-350 falsch oder ausgefallen |
| FF-08 | Thermisches Ereignis wird nicht gemeldet | Gas-/Drucksensor BT-770 oder Meldeweg ausgefallen |
| FF-09 | Ladezustand wird zu hoch angezeigt | Zustandsschätzung falsch |

## 3 Gefährliche Ereignisse und Einstufung (Vorschlag Opus)
| Nr | FF | Situation | Gefahr | S | E | C | ASIL | Begründung |
|---|---|---|---|---|---|---|---|---|
| HE-01 | FF-01 | AC-Laden über Nacht, Fahrzeug in Garage, niemand anwesend | thermisches Durchgehen, Gebäudebrand | S3 | E4 | C3 | **D** | Laden ist häufig (E4). Nachts bemerkt es niemand (C3). |
| HE-02 | FF-01 | DC-Schnellladen, Fahrer in der Nähe | Brand am Fahrzeug | S3 | E3 | C2 | B | Fahrer kann weggehen. Wird durch HE-01 abgedeckt. |
| HE-03 | FF-02 | Laden nach langer Standzeit | innerer Kurzschluss, verzögerter Brand | S3 | E3 | C3 | **C** | Die Folge tritt später auf, deshalb kaum beherrschbar. |
| HE-04 | FF-03 | Fahrt mit hoher Last oder Schnellladen | Durchgehen einer Zelle | S3 | E4 | C2 | **C** | Mit Warnung kann man anhalten und aussteigen (C2). |
| HE-05 | FF-03 | Laden im Winter unter 0 °C | Lithium-Abscheidung, später Durchgehen | S3 | E3 | C3 | **C** | Folge verzögert |
| HE-06 | FF-04 | Fahrt, Kurzschluss außerhalb (Leitung, Umrichter) | Lichtbogen, Brand im Pack | S3 | E4 | C2 | **C** | Sicherung BT-713 als zweite, passive Ebene |
| HE-07 | FF-05 | Autobahn, Überholen oder Linksabbiegen | Antrieb fällt aus, Auffahrunfall | S3 | E3 | C2 | B | Antriebsverlust gilt meist als beherrschbar (C2). |
| HE-08 | FF-06 | nach einem Unfall, Rettungskräfte am Fahrzeug | Stromschlag | S3 | E2 | C3 | B | Unfallsituation selten (E2) |
| HE-09 | FF-06 | Werkstatt, Pack soll spannungsfrei sein | Stromschlag | S3 | E2 | C2 | A | Zusätzlich Service-Trennstecker BT-720 und Arbeitsvorschrift |
| HE-10 | FF-07 | Laden oder Waschen bei zweitem Isolationsfehler | Stromschlag beim Berühren der Karosserie | S3 | E2 | C3 | B | Nur bei Doppelfehler gefährlich, deshalb E2 (F-S3) |
| HE-11 | FF-08 | Fahrt mit Insassen | keine Warnung vor Rauch oder Feuer | S3 | E4 | C2 | **C** | Verknüpft mit REQ-P11: Warnzeit nach Norm |
| HE-12 | FF-09 | Fahrt, Akku leer | Liegenbleiben | S1 | E3 | C2 | QM | Liegenbleiben mit Vorwarnung |

## 4 Sicherheitsziele (Opus, Einstufungen HE-01…12 vom Autor übernommen 2026-11-24)
| SG | Ziel | aus | ASIL | sicherer Zustand | FTTI (Annahme Opus) |
|---|---|---|---|---|---|
| SG-01 | Verhindere, dass eine Zelle über U_max geladen wird | HE-01, 02 | D | Laden beendet, Schütze offen | 1 s |
| SG-02 | Verhindere das Laden einer tiefentladenen Zelle | HE-03 | C | Ladesperre bis Werkstatt | 1 s (bis Ladebeginn) |
| SG-03 | Verhindere Zelltemperaturen über T_krit und Laden außerhalb des Temperaturfensters | HE-04, 05 | C | Leistung begrenzen, dann trennen. Laden erst nach Vorheizen. | 1 s |
| SG-04 | Trenne bei Überstrom und Kurzschluss | HE-06 | C | Schütze oder Sicherung offen | 10 ms (Sicherung), 100 ms (Schütz) |
| SG-05 | Verhindere unerwartetes Trennen während der Fahrt | HE-07 | B | erst Leistung verringern und warnen, dann trennen (außer SG-01/04) | 2 s Vorwarnung |
| SG-06 | Trenne Hochvolt nach Crash und auf Abschaltbefehl | HE-08, 09 | B | Schütze offen, HV-Bus entladen | ≤ 60 s bis ≤ 60 V DC bzw. < 0,2 J auf dem HV-Bus (UN R94 Rev. 4, Beleg W48); Gedächtniswert 5 s verworfen |
| SG-07 | Erkenne Isolationsfehler und melde sie | HE-10 | B | Warnung. Kein Laden bei R_iso < 100 Ω/V (REQ-P13). | 10 s |
| SG-08 | Warne die Insassen rechtzeitig vor einem thermischen Ereignis | HE-11 | C | Warnung an Fahrzeug | ≥ 5 min vor gefährlicher Situation im Innenraum (UN R100, Beleg W35d, CELEX 42024X1955) |

**Zielkonflikt:** SG-05 („nicht trennen“) widerspricht SG-01, SG-03 und SG-04 („trennen“). Das ist ein Widerspruch im Sinne von TRIZ und der erste Kandidat für das Kreativwerkzeug (KR2, nach dem Pilot KR1).

## 5 Was daraus für die Hardware folgt (funktionales Sicherheitskonzept, Grobentwurf)
| FSR | Anforderung | SG | trifft |
|---|---|---|---|
| FSR-01 | Zellspannung auf **zwei unabhängigen Wegen** messen: AFE und ein zweiter, einfacher Überspannungsschalter je CMU (Sekundärschutz). Alternativ ein AFE mit ASIL-D-Diagnose. | SG-01 | BT-322, BT-325 |
| FSR-02 | Messleitungsbruch erkennen (Leitungsdiagnose) | SG-01, 02 | BT-322, BT-360 |
| FSR-03 | Temperatur plausibilisieren: Nachbarfühler vergleichen, Ausfall erkennen | SG-03 | BT-330 |
| FSR-04 | Strom redundant messen: Shunt und Hall (schon in E2) | SG-04 | BT-340 |
| FSR-05 | Verklebte Schütze erkennen (Spannung vor und hinter dem Schütz) | SG-01, 06 | BT-711 |
| FSR-06 | Unabhängigen Abschaltpfad vorsehen: Sekundärschutz öffnet Schütze ohne Software | SG-01, 04 | BT-325, BT-715 |
| FSR-07 | Derating vor dem Trennen: Leistungsgrenze per CAN, Warnzeit | SG-05 | BT-310 |
| FSR-08 | Crashsignal zweikanalig, aktive Entladung des Zwischenkreises fahrzeugseitig | SG-06 | BT-310, Schnittstelle |
| FSR-09 | Isolationswächter mit Selbsttest | SG-07 | BT-350 |
| FSR-10 | Gas-/Drucksensor mit eigenem Weckpfad (auch im Stand) | SG-08 | BT-770 |
| FSR-11 | Ausfall der Daisy-Chain-Kommunikation → Zeitüberwachung im BMS, sicherer Zustand innerhalb der FTTI (Voraussetzung für die Einstufung „sicher“ in der FMEDA E3d) | SG-01, 02 | BT-310, BT-322 |
| FSR-12 | Sekundärschutz misst **jede Zelle einzeln** (nicht die Summe, B-BAT-055) | SG-01 | BT-325 |

Was die CMU-Platine in E3 vorhalten muss: FSR-01, 02 und 06. Das heißt Platz für den Sekundärschutz und eine eigene Leitung zum Abschaltpfad.

## 6 Nicht im Umfang (Vorschlag)
Diese Arbeitsprodukte fehlen für eine echte ISO-26262-Freigabe. Im Testprojekt werden sie nur benannt:
- technisches Sicherheitskonzept (Hardware- und Softwareaufteilung)
- Hardwaremetriken SPFM/LFM/PMHF mit Ausfallraten
- FMEDA
- Software nach ISO 26262-6
- Sicherheitsnachweis

Die FMEDA lässt sich später aus der KiCad-Stückliste der CMU erzeugen (E3-Folge).

## 7 Fragen an den Autor
| Nr | Frage | Vorschlag Opus |
|---|---|---|
| F-S1 | Grenze des Items: Ladegerät, Ladesäule, Umrichter außerhalb? | **Autor 2026-11-24: nur Pack** |
| F-S2 | HE-01 mit C3 und damit ASIL D für SG-01? | **Autor 2026-11-24: ASIL D** |
| F-S3 | HE-10 Isolation: E2 wegen Doppelfehler? | **Autor 2026-11-24: ASIL B** |
| F-S4 | FTTI-Werte §4 als Annahme übernehmen? | **Autor 2026-11-24: übernommen (Annahme)** |
| F-S5 | Umfang: nur HARA, Sicherheitsziele und FSR (§6)? | **Autor 2026-11-24: HARA + SG + FSR + grobe FMEDA** |
| F-S6 | Grobentwurf der FMEDA für die CMU, wenn E3 fertig ist? | **Autor 2026-11-24: ja** |

---
*KI-generiert (Claude Opus, 2026-11-24). Status Entwurf. Freigabe nur durch den Autor.*

