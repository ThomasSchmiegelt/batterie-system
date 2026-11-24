| Dok.-Nr. | BAT-KR-P1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Prüfung Opus KR1 und Vorgabe Lauf 2 | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert (Claude Opus, 2026-11-24). Geprüft an `kasten.json`, `konzepte.json`, `rang.json`, Stichprobe `paare.json`.

## Befund
1. **Der Ablauf funktioniert technisch:** TRIZ, Kasten, Kopfstand, Paarurteile in beiden Reihenfolgen, Zirkelzählung und Empfindlichkeit laufen. Die Vorliebe für die erste Position ist gering (68 : 59 : 13).
2. **Der Kasten ist unsauber.** Ausprägungen stehen in der falschen Zeile:
   - T5.4 „gepulster Betrieb“ ist ein Zeitpunkt, keine Wärmeabfuhr.
   - T5.5 „Transformatorkopplung“ ist ein Prinzip.
   - T2.3 „externer Flüssigkeitskreislauf“ ist kein Ort im Pack.
   Andere Ausprägungen sind schwach, etwa „Ultraschall-Konvektionsantrieb“ und „temperaturgepumpt“. Das Kürzen durch Opus (Stufe 3) war vorgesehen, hat aber nicht stattgefunden.
3. **Die Konzeptauswahl über den größten Hamming-Abstand ist ein Methodenfehler (Fehler Opus in METHODE.md).** Sie erzeugt maximal verschiedene, aber widersprüchliche Kombinationen. Beispiel: K2 „gepulster Hochstrom“ mit „externem Flüssigkeitskreis“. Konzepte müssen eine **Leitidee** haben. Der Hamming-Abstand prüft dann nur noch, ob sie verschieden genug sind.
4. K1 nennt noch 34 Ω. Gültig ist 32,45 Ω (ENT-172).
5. Ergebnis von Lauf 1: nur Erprobung des Werkzeugs, **keine Grundlage für eine Akte**.
6. Die von Sonnet ergänzte Empfindlichkeitsrechnung mit Gewichten 0 und 12 wird übernommen. Die TRIZ-Matrix bleibt „Lizenz ungeklärt, nur privat“.

## Vorgabe Lauf 2 (Kasten und Konzepte von Opus)
| Zeile | Ausprägungen |
|---|---|
| T1 Prinzip | 1 passiv, Widerstand · 2 aktiv induktiv (Zelle ↔ Modul, Übertrager) · 3 aktiv kapazitiv (umgeschalteter Kondensator) |
| T2 Ort der Verlustwärme | 1 CMU-Platine · 2 Widerstand auf Kühlplatte bzw. Zellverbinder (Leitung von CMU) · 3 kaum Verlust (aktiv) |
| T3 Zeitpunkt | 1 beim Laden und in Ruhe (Ist) · 2 nur in Ruhe (zyklisches Aufwachen) · 3 dauernd, auch beim Fahren |
| T4 Strom und Steuerung | 1 130 mA konstant · 2 260 mA, 50 % Takt, temperaturgeführt · 3 1–2 A (aktiv) |
| T5 Wärmeabfuhr | 1 Konvektion und Strahlung · 2 Wärmeleitpad CMU → Kühlplatte · 3 Kupferflächen, Platine größer |

| Konzept | Leitidee | T1 | T2 | T3 | T4 | T5 |
|---|---|---|---|---|---|---|
| K1 | Ist-Entwurf (Referenz) | 1 | 1 | 1 | 1 | 1 |
| K2 | Ist mit Wärmepfad | 1 | 1 | 1 | 1 | 2 |
| K3 | getaktet in Ruhe, temperaturgeführt | 1 | 1 | 2 | 2 | 3 |
| K4 | Wärme ausgelagert auf die Kühlplatte | 1 | 2 | 1 | 2 | 2 |
| K5 | aktiv induktiv | 2 | 3 | 3 | 3 | 1 |
| K6 | aktiv kapazitiv | 3 | 3 | 3 | 3 | 1 |

Zahlen für die Urteile nur aus E2, E3 (`sim/elektrik/e3_platine/ergebnis_*.json`, B-BAT-051) und Recherche. Fehlt eine Zahl, sagt das Urteil „ohne Zahl“.

## Erwartung Lauf 2 (Opus, vorher)
- Bei gleichen Gewichten liegen K2 oder K4 vorn. Beide lösen das Wärmeproblem aus B-BAT-051, ohne die Zeit zu verlängern.
- K3 verliert bei der Zeit, gewinnt bei Wärme und Kosten.
- K5 und K6 verlieren bei Kosten, Reifegrad und Fehlermöglichkeiten.
- K1 landet hinten, denn es verfehlt die Wärmegrenze.
- Gewichtet der Autor Kosten hoch: K3 vorne. Gewichtet er Zeit hoch: K5 vorne.

## Prüfung Lauf 2 (Opus, 2026-11-24, alle 105 Urteile der Kriterien Wärme, Fehler, Reife und Wirkungsgrad gelesen)
1. **Wärme K3, PI hat recht, meine Erwartung war physikalisch falsch.** Bei gleichem mittlerem Strom und 260 mA mit 50 % Takt verdoppelt sich die mittlere Verlustleistung (D · I² · R). Die Spitze von ≈ 39 W je CMU (18 × 0,26² A² × 32,45 Ω) ist richtig gerechnet. K3 als Leitidee taugt nicht, sie wird verworfen.
2. **Reifegrad falsch gelesen:** PI bewertet „im Projekt schon simuliert, DRC 0“ statt Serienreife der Technik. Dadurch werden K1 und K2 bevorzugt. Ursache: Opus hat das Kriterium im Auftrag nicht definiert (der Autor bekam die Definition „wie bewährt in Serienfahrzeugen“).
3. **Fehlermöglichkeiten zählen doppelt:** Die Überschreitung von 105 °C wird als Fehler gewertet, obwohl sie schon im Kriterium Wärme steckt. Daher kommen die 3 Zirkel in diesem Kriterium.
4. **K1 hätte gar nicht bewertet werden dürfen:** Es verfehlt einen Muss-Grenzwert (105 °C, B-BAT-051). Methodenfehler Opus: Festforderungen müssen vor dem Paarvergleich ausschließen (VDI-2225-Logik).
5. Hamming-Abstand 1 bei K1/K2 und K5/K6 ist gewollt (Variante einer Leitidee). Die Regel lautet künftig ≥ 1.
6. Urteil zum Stand: K2 (Ist mit Wärmeleitpad) liegt mit den Gewichten des Autors vorn und bleibt bei ±1 vorn. K6 (aktiv kapazitiv) folgt knapp. Wegen 2 bis 4 ist das noch nicht belastbar → Lauf 3.

## Vorgabe Lauf 3
- **Festforderung vor dem Vergleich:** Platinentemperatur ≤ 105 °C bei 45 °C Umgebung. K1 und K3 scheiden aus, mit Begründung im Bericht.
- Neu urteilen nur für die Kriterien **Reifegrad** und **Fehlermöglichkeiten** über K2, K4, K5, K6 (6 Paare × 2 Reihenfolgen), mit diesen Definitionen im Prompt:
  - **Reifegrad:** Wie verbreitet ist das Prinzip in Serien-BMS von Pkw? Nicht gemeint ist der Projektstand.
  - **Fehlermöglichkeiten:** neue Fehlerarten des Konzepts (Bauteile, Schalter, Software, Mechanik wie ein Pad, das sich löst) und ihr Bezug zu FSR-01/02/06. Die Temperatur ist hier **ausgeschlossen**, sie steckt im Kriterium Wärme.
- Die übrigen 5 Kriterien aus Lauf 2 übernehmen. Rang mit den Gewichten des Autors und mit gleichen Gewichten, Empfindlichkeit, Zirkel.
