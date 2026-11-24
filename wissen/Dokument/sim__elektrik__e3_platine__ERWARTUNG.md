---
typ: dokument
datei: "sim/elektrik/e3_platine/ERWARTUNG.md"
tags: ["dokument", "kopie"]
---
# ERWARTUNG

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `sim/elektrik/e3_platine/ERWARTUNG.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

| Dok.-Nr. | ERW-E3 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung E3: CMU-Leiterplatte (KiCad), Ausgleichs- und Vorladekreis (SPICE) | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Opus, 2026-11-24), vor der Rechnung. Auftrag Autor 2026-11-24: „die elektronik weiter detailieren können, also auch mosfets und wiederstände und die Platine“. Anforderungen: REQ-P15, P17–P20 (Vorschlag), HARA BAT-DOC-24 (FSR-01, 02, 06). **Alle Werte unten sind Annahmen Opus** (Herkunft „ERW-E3“), sofern nicht als Akte oder E2-Ergebnis genannt. Die Normwerte stammen aus dem Gedächtnis, ein Beleg fehlt (W45/W46 beauftragt).


## Anforderung
REQ-P15, REQ-P17, REQ-P18, REQ-P19, REQ-P20

## Eingaben (vorhanden)
- LFP: s = 250, 14 CMU, U_max Zelle 3,65 V → **U_max Pack 912 V**; Ausgleich 150 mA (ENT-115)
- NMC: s = 217, 13 CMU, 4,2 V → **911 V**; Ausgleich 130 mA (ENT-146)
- CMU: 18 Kanäle, Platine 120 × 60 × 10 mm, 80 g (`cad/pack/entwurf_parameter.py`, A_e2_cmu_mm, ERW-E2 N1). Wärme je CMU 9,85 / 9,83 W (E2).
- Vorladung: C_ZK 1000 µF, R 100 Ω (ERW-E2)

## Annahmen Opus (ERW-E3)
| BT | Merkmal | LFP | NMC | Begründung |
|---|---|---|---|---|
| BT-321 | lagen / dicke / Kupfer | 4 / 1,6 mm / 70 µm außen | gleich | Wärmespreizung der Ausgleichswiderstände |
| BT-321 | laenge × breite | 120 × 60 mm (E2) | gleich | Prüfen, ob es passt (Erwartung 6) |
| BT-322 | AFE | generischer 18-Kanal-Mess-IC, ASIL-D-fähig, Ausgleich über externe FETs | gleich | Stand der Technik. Kein Herstellerteil ins Repo, nur ein eigenes KiCad-Symbol mit Pinliste „generisch“. |
| BT-323 | widerstand_Ohm | 2 × 47 Ω parallel = 23,5 Ω (2512, je 1 W) | 2 × 68 Ω = 34 Ω | R = U_max / I. Aufgeteilt auf zwei Widerstände, damit sich die Wärme verteilt. |
| BT-323 | schalter | N-MOSFET, Logikpegel, R_DS,on ≤ 0,5 Ω, AEC-Q101 | gleich | |
| BT-323 | Filter je Messeingang | 100 Ω + 100 nF | gleich | EMV und Aliasing (REQ-P17) |
| BT-324 | pruefspannung_V | CMU ↔ CMU: Basisisolierung, ≥ 1,5 kV Prüfspannung | gleich | Zwischen Nachbar-CMUs liegen nur ≈ 2 × 76 V an. Die volle Packspannung liegt erst an der letzten Strecke zum BMS (BT-311). |
| BT-325 | schwelle_V | 3,75 V je Zelle, 1 s | 4,25 V, 1 s | FSR-01: knapp über U_max, unter der Gefahrengrenze |
| BT-321 | kriechstrecke_mm | innerhalb CMU ≥ 0,6 mm (≤ 76 V), am Daisy-Chain-Ausgang ≥ 2,5 mm | gleich | IEC 60664-1, PD2, Werkstoffgruppe IIIa (Gedächtnis) |
| BT-311 | kriechstrecke_hv_nv_mm | ≥ 10 mm verstärkt (Arbeitsspannung 1000 V-Klasse) | gleich | dito, nur als Vorgabe. BT-311 wird in E3 nicht gebaut. |
| BT-712 | schalter / pulsenergie_J | Vorladeschütz + Widerstand ≥ 450 J Puls | gleich | Siehe Erwartung 4. Die MOSFET-Variante kommt aus KR später. |

## Erwartung
1. **Ausgleichsstrom hängt von der Zellspannung ab:**
   - LFP: 23,5 Ω → 155 mA bei 3,65 V, aber 136 mA bei 3,2 V (Nennspannung)
   - NMC: 34 Ω → 124 mA bei 4,2 V, 109 mA bei 3,7 V
   - Folge: Die Ausgleichszeit aus E2 (12,3 / 14,2 h) gilt nur bei voller Zelle. Im Mittel ist sie ≈ 10–15 % länger. SPICE muss das zeigen (Kennlinie I(U)).
2. **Verlust je Kanal** ≈ 0,53–0,57 W, je Widerstand ≈ 0,28 W (≤ 50 % von 1 W, Derating eingehalten). Im FET ≤ 0,02 W. Je CMU ≈ 9,8 W, deckungsgleich mit E2 ±3 %.
3. **Wärme auf der Platine:** 9,8 W auf 120 × 60 mm sind ≈ 1,4 kW/m². Bei freier Konvektion im Pack (h ≈ 5–10 W/m²K, zwei Seiten) folgt eine Übertemperatur von **≈ 60–100 K**. Das liegt über 105 °C bei 45 °C Umgebung, also **wahrscheinlich verfehlt**. Abhilfen: Wärmeleitpad zur Kühlplatte oder Taktung. Thermik nicht selbst rechnen, nur die Abschätzung in ERGEBNIS. Opus beauftragt danach E3b (Elmer).
4. **Vorladung (SPICE, 912 V):** I_spitze = 9,1 A, Energie im Widerstand = ½ C U² = 416 J, t_95 = 3 τ = 300 ms. Der Widerstand muss diesen Puls aushalten (≥ 450 J). E2 hatte mit 800 V gerechnet (8 A, 320 J). Diese Abweichung ist bekannt und kein Fehler von E2.
5. **Anzahl Bauteile je CMU** ≈ 130–170: AFE, 18 × (2 R + FET + RC-Filter), 4 NTC-Eingänge, 2 Übertrager, Sekundärschutz, Stecker FPC, Daisy-Chain-Stecker ×2.
6. **Layout passt in 120 × 60 mm** mit 4 Lagen. DRC und ERC mit 0 Fehlern. Kriechstrecken aus der Tabelle als Netzklassen-Regel umgesetzt.
7. **STEP der Platine** im Pack (Fall b, beide Varianten) ohne Kollision. Masse ≤ 80 g.

## Abbruch → OPUS
Erwartung 1, 2, 4 oder 6 verfehlt; Kollision; fehlendes Maß; ein Werkzeug lässt sich nicht ohne sudo installieren; jede neue Annahme.

## Nachtrag 1 (Opus, 2026-11-24, nach SPICE-Zwischenstand, Prüfung an `ergebnis_ausgleich.json` und `ergebnis_vorladung.json`)
- **Erwartung 1:** Die Rohdaten sind plausibel (LFP 152,0 mA bei 3,65 V = (3,65 − U_DS)/23,5 Ω). Bei Nennspannung beträgt die Verlängerung +14,1 % / +13,5 %. Das trifft meine Abschätzung, denn die 10–15 % hatte ich bei U_nenn gerechnet. „Im Mittel“ war von mir unklar formuliert. Der lineare Mittelwert von U_nenn − 0,2 V bis U_max (+6,6 %) ist eine zulässige Lesart. Maßgebend ist künftig die Verlängerung bei U_nenn als ungünstiger Fall. Meine Formulierung war falsch, das Modell ist richtig. Ein U_min ist nicht nötig, weil der Ausgleich nahe dem vollen Ladezustand läuft. Die FET-Werte U_GS 5 V und VTO 1,5 V werden als Modellwahl übernommen.
- **Erwartung 2 NMC:** Die Abweichung kommt aus meiner Tabelle. Mit 34 Ω (E24-Rundung) sind 130 mA nicht erreichbar, und das Band 0,53–0,57 W galt nur für LFP. **Korrektur: NMC 2 × 64,9 Ω (E96) = 32,45 Ω**, ENT-172 geändert. Erwartung NMC: ≈ 128 mA bei 4,2 V, ≈ 0,53 W je Kanal, ≈ 9,6 W je CMU.
- **Erwartung 4:** ok.
- **Neue Merkmale:** BT-323 `filter_R_Ohm` 100, `filter_C_nF` 100; BT-321 `kriechstrecke_daisy_mm` 2,5. Akten dafür anlegen.
- **KiCad:** Der Flatpak war um 09:2x noch in Installation (PID 13253). Abwarten mit einem Hintergrundbefehl, der sich meldet, nicht in einer Schleife abfragen.

## Nachtrag 2 (Opus, 2026-11-24): Routing und Platzhalter
- Der Autor gibt Freerouting frei (2.5.0 CLI, `$FREEROUTING`).
- Ergänzt werden (Annahme Opus): 100 nF je AFE-Versorgungspin, TVS an Daisy-Chain-Ein- und -Ausgang, GND/VCC am Daisy-Stecker.
- Erwartung: dann ≈ 115–125 Teile, vollständig geroutet auf 4 Lagen, DRC 0.
- Wärme bleibt verfehlt, Bearbeitung in E3b.

## Nachtrag 3 (Opus, 2026-11-24): Korrekturen nach Routing-Abbruch
- **Freerouting:** Die native CLI stürzt ab (GraalVM). `$FREEROUTING` zeigt jetzt auf das Jar mit Temurin JRE 25, headless, getestet.
- **Fehler Opus in N2: GND/VCC am Daisy-Stecker ist falsch.** Die Strecke ist über Übertrager galvanisch getrennt, deshalb kommen über den Stecker nur die 2 Datenleitungen (verdrillt). Entfernen.
- **Stecker:** 2-polig, liegend, Raster ≤ 1,25 mm, Bauhöhe ≤ 5 mm (generischer Footprint). Damit bleibt die Platine bei 10 mm Bauraum. Den Bauraum nicht erhöhen.
- **2,5-mm-Regel:** Sie gilt nur über die Trennstelle, also zwischen Netzen verschiedener Potenzialbereiche (Zellseite gegen Daisy-Leitungsseite des Übertragers). Zwischen den Pins einer Seite gilt sie nicht, wie bei der Ausnahme im Bauteil (B-BAT-051). Als Klasse-zu-Klasse-Abstand im DSN bzw. in den KiCad-Regeln umsetzen.
- Erwartung: ≈ 104–108 Teile, vollständig geroutet, DRC 0, NMC ohne Kollision.

## Nachtrag 4 (Opus, 2026-11-24): Hinweise des Autors zu Luft- und Kriechstrecken
Quelle: Fachartikel eines Kabelherstellers (COTRONIC, 20.10.2025), vom Autor eingefügt. Sekundärquelle, nicht zitatgeprüft. Daraus kommt **nur die Methode**, keine Werte als Beleg. Die Beispielwerte gelten für Netzwechselspannung mit Überspannungskategorie III und Verschmutzungsgrad 3. Sie sind auf das Pack (DC 912 V, PD2 im IP67-Gehäuse) nicht übertragbar.
Übernommen als Regeln (Annahme Opus, ERW-E3 N4):
1. **Kriechstrecke ≥ Luftstrecke** immer. Als zusätzliche Prüfung in `drc_regeln.py` aufnehmen.
2. **Die Luftstrecke richtet sich nach der Stoßspannung (Überspannungskategorie), die Kriechstrecke nach der Arbeitsspannung.** Im Artikel ist das vermischt. Beide getrennt ausweisen.
3. **Höhenkorrektur über 2000 m** gilt für Luftstrecken. **Autor 2026-11-24: Auslegungshöhe 3000 m** (bis zum Normtext Faktor 1,25, der ungünstigere Wert). Der Artikel nennt 1,25, mein Gedächtnis nennt IEC 60664-1 Tab. A.2 mit 1,14 bei 3000 m und 1,29 bei 4000 m. Die Auslegungshöhe ist eine Anforderung, Frage an den Autor.
4. **Werkstoffgruppe:** CMU in Standard-FR4 (IIIa, CTI ≥ 175). Nur wenn die HV/NV-Trennung auf BT-311 nicht passt: FR4 mit CTI ≥ 600 (Gruppe I) oder eine **Schlitzfräsung** unter dem Übertrager bzw. Isolator.
5. **Schutzlack:** keine Annahme PD1. PD2 bleibt, der Lack ist nur eine zusätzliche Reserve.

## Nachtrag 5 (Opus, 2026-11-24): Ursache des Routing-Abbruchs
- **Ursache: Fehler Opus.** Die 0,6 mm „innerhalb CMU“ wurden als globaler Abstand im DSN gesetzt (`clearance 600`). Bei 0,5 mm Pinabstand von AFE und FPC kommt keine Bahn aus dem Pinfeld. Das liegt nicht an Freerouting.
- **Korrektur ENT-168: 0,2 mm innerhalb der CMU** (Spalte Leiterplatten, PD2, ≤ 100 V, Annahme). 2,5 mm nur Klasse gegen Klasse über die Trennstelle. Die Regel Kriechstrecke ≥ Luftstrecke ist damit erfüllt.
- Leiterbahn 0,2 mm Signal, 0,3 mm Ausgleichspfad (155 mA, 70 µm), Via 0,6/0,3 mm.
- Erwartung: vollständig geroutet in ≤ 10 Durchläufen, DRC 0. Bleiben Verbindungen offen: Platzierung nach Kanalreihenfolge ordnen (Kanal n: Filter, Widerstände und FET in einer Spalte vor dem AFE-Pin n), dann neu routen.

## Nachtrag 6 (Opus, 2026-11-24, nach Routing Lauf 3; Bilder `platine_<V>_3d_*.png` angesehen)
- Routing vollständig, DRC 0, 0 offen: **Erwartung 6 erfüllt.** Die Methodenwahl von Sonnet wird bestätigt:
  - Daisy-Strecke von Hand vorverlegt
  - T-Netze mit 0,2 mm Breite (155 mA, 70 µm außen, ausreichend)
  - Mindestbreite 0,15 mm
  - hängende Vias und unbenutzte Pads entfernt
- **Erwartung 5 (130–170 Teile) zu hoch angesetzt:** 108 Teile mit Entkopplung, TVS und Sekundärschutz sind für diese Funktion plausibel. Verfehlt durch meine Schätzung, kein Mangel.
- **Korrektur Thermovias (Fehler im Detail, ENT-187 gilt weiter):** Isolierte Kupferinseln ohne Fläche auf B.Cu leiten die Wärme nicht wie in E3b angenommen. Neu:
  - Die Vias sitzen im **eigenen Netz der Widerstandspads** (je Widerstandsende).
  - Auf B.Cu liegt je Netz eine Kupferfläche unter dem Paar, Abstand zwischen den Flächen ≥ 0,2 mm (ENT-168).
  - Das Pad ist elektrisch isolierend.
  - Alle 144 Vias setzen.
- **Masse (Annahme Opus):** FR4 1,85 g/cm³, Cu 8,96 g/cm³ mit Kupferanteil aus dem Layout. Bauteile: 2512 ≈ 0,045 g, 0603 ≈ 0,005 g, SOT-23 ≈ 0,01 g, LQFP-64 ≈ 0,35 g, Übertrager ≈ 1 g, Stecker aus Footprint-Volumen × 1,4 g/cm³. Erwartung ≈ 25–35 g ohne Pad. Das Pad (1 mm, 3 g/cm³ Annahme) wiegt ≈ 22 g.

## Nachtrag 7 (Opus, 2026-11-24, nach FMEDA E3d)
- **Befund B-BAT-055: Der Sekundärschutz misst falsch.** In `cmu_skidl.py` misst er die Summe T18–T0 (VTOP/VBOT) statt jede Zelle. Eine Schwelle von 3,75 / 4,25 V **je Zelle** (ENT zu BT-325) lässt sich so nicht prüfen, FSR-01 ist nicht erfüllt. Ursache: Opus hat das in ERW-E3 nur als „Sekundärschutz je CMU“ beschrieben, die Netzliste folgte dem.
  - **Korrektur:** 3 × generischer 6-Zellen-Überspannungsschutz (je 7 Messeingänge, TSSOP-16). Die Ausgänge gehen als wired-OR auf ABSCHALT (FSR-06). Konservativ, bewährtes Prinzip.
- **Maßnahme M1 aus E3d wird umgesetzt (keine Optimierung, sondern Pflicht für das ASIL-C-Ziel von SG-02):**
  - Zwei Schalter in Reihe je Ausgleichskanal, als Doppel-N-FET im SOT-363 statt eines einzelnen FET.
  - E3d rechnet SPFM SG-02 97,85 % (Ziel ≥ 97 %).
  - OPT-013 wird damit erledigt.
- Erwartung:
  - ≈ 110–112 Teile (+3 OVP, FETs bleiben 18 Gehäuse)
  - vollständig neu geroutet, DRC 0
  - Thermovias unverändert 144
  - Bilder und Explosionsansicht neu

## Nachtrag 8 (Opus, 2026-11-24, Routing nach N7 bleibt stehen)
Nach N7 (3 OVP, Doppel-FET, AFE LQFP-80) bleiben 1 bzw. 3 Verbindungen offen, das Routing stagniert. Entscheidung, der Reihe nach, erst konservativ:
1. **Platzierung lockern bei gleicher Größe:** AFE in die Mitte, die 3 OVP direkt an den FPC-Zellabgriff, je 6 Kanäle als Block vor „ihrem“ OVP. Fanout-Vias am AFE vorgeben. Danach neu routen.
2. Bleibt etwas offen: **Platine 10 mm länger (130 × 60 mm)**, als neue Akte BT-321 laenge_mm (ersetzt die alte). Danach Pack-Kollisionen beider Varianten prüfen. Gibt es eine Kollision → OPUS.
3. **6 Lagen** nur, wenn auch 2. scheitert → OPUS.
- „via_dangling“ (Vias ohne Bahn) und track_width nach dem Routing bereinigen. Abnahme: DRC 0, 0 offen, 144 Thermovias.
- Annahmen Opus für die Masse (ERW-E3 N8): SOT-363 0,006 g, TSSOP-16 0,06 g, LQFP-80 0,45 g. AFE LQFP-80 ist bestätigt (69 Pins).

## Nachtrag 9 (Opus, 2026-11-24, Prüfung N7/N8)
- Geprüft an `ergebnis_platine.json`: beide 120 × 60 mm, 110 Teile, DRC 0, 0 offen, 399 Vias. Größer werden musste die Platine nicht.
- Die Übertragung des LFP-Routings auf NMC ist **bestätigt**: Netzliste, Footprints und Platzierung sind gleich, nur die Werte unterscheiden sich, und der DRC auf der NMC-Platine selbst meldet 0. Methode zulässig.
- Kanalblatt gelesen: Doppel-FET SOT-363 richtig in Reihe (D1 ← Widerstände, S1–D2 verbunden, S2 → TL). Masse SOD-323 0,005 g (Annahme Opus, vernachlässigbar).

