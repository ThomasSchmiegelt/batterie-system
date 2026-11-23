# Inhalt Abschlussbericht 1.0: Vorgaben Opus (Deutung)

KI-generiert (Claude Opus, 2026-11-23). Grundlage für Sonnet. Die Deutung stammt von Opus, die Zahlen nur aus den genannten Quellen. Vorgabe des Autors (23.11.): „Im Abschlussbericht soll auch eine Analyse für mögliche Verbesserungen stehen. Und auch was bei einer Konstruktionsschleife besser gemacht werden kann.“

## A. Analyse möglicher Verbesserungen (Produkt)
Je Punkt: Befund mit Zahl und Quelle, Ursache, Vorschlag, erwarteter Nutzen, Aufwand (klein/mittel/groß), Priorität.
1. **Thermik ΔT:** Die neue Platte (zwei parallele Mäander, freigegeben, ENT-158/159) senkt ΔT von 16,4 auf 7,6 K (LFP-Schnellladen) bei 0,17 bar. Rest-ΔT ist überwiegend das Gefälle innerhalb der Zelle (Kühlseite–Mitte). Vorschlag: zuerst klären, wie REQ ΔT ≤ 5 K gemeint ist (zwischen Zellen oder im Block); erst dann Pad (λ, Anpressung) oder beidseitige Kühlung untersuchen. Quellen: sim/kuehlung/k5_parallel/ERGEBNIS.md, B-BAT-038/040/043.
2. **Crash Pfahl 20 kJ:** Zellen 16 mm eingedrückt (LFP_a2), Vorgabe „Zellen unverformt“ verfehlt; schon bei 5 kJ 6,7 mm (LFP) bzw. 8,3 mm (NMC). Hinweis: Modell nur Batteriebox, ohne Schweller des Fahrzeugs (konservativ). Vorschlag: Verformungsraum zwischen Rahmen und Zellen vergrößern oder Seitenprofil versteifen; Schnittstelle Schweller–Pack mit dem Fahrzeughersteller festlegen. Quellen: sim/mechanik/x3_crash_g5/ergebnis.json, B-BAT-039/040/042.
3. **Quetschung (b):** Rahmen 0,4 mm bei 100 kN, bis rund 700 kN unter 3 mm: große Reserve. Vorschlag: Leichtbaupotenzial im Rahmen prüfen, aber nur gemeinsam mit dem Pfahlfall (dort fehlt Reserve). Grenze: b nur bis 5 ms ausgewertet, Instabilität ungeklärt.
4. **Elektrik NMC:** Verluste 364,5 W (Ziel ≤ 300 W), LFP 73 W ok; Gruppenverbinder im CAD 75 mm², in E1 45 mm² (Widerspruch). Vorschlag: Querschnitt angleichen und E1 mit CAD-Maßen neu rechnen. Quelle: sim/elektrik/e1_querschnitte/ergebnis_g5.json.
5. **Kühlkreis:** dreifacher Durchfluss braucht eine andere Pumpe; Δp gesunken, Pumpenleistung neu bestimmen (Stückliste).
6. **Modellgrenzen/Validierung:** K3 FluidX3D Δp +232 % gegenüber Korrelation, Massenerhalt im Film verfehlt; keine Rechnung validiert. Vorschlag: Prüfplan mit drei Versuchen (Zelle thermisch, Plattendurchfluss Δp/Verteilung, quasistatische Quetschung).
7. **Datenlage Zelle:** Abweichungen zu den Datenblättern (DB2) und Annahmen in startwerte.json; Vorschlag: Zellmuster und Messungen anfragen.
Am Ende eine Prioritätentabelle (Nutzen × Aufwand).

## B. Was bei der nächsten Konstruktionsschleife besser gemacht werden kann (Prozess)
Je Punkt: was passiert ist (Beleg B-BAT/BA), Lehre, konkrete Regel für die nächste Schleife. Zuschreibung genau: Vorgaben des Autors als Vorgabe, Befunde und Fehler der KI als Handlung der KI.
1. **Erwartung aus Fakten, nicht aus der Vorstellung:** Drei Erwartungen von Opus lagen falsch, weil das Bild im Kopf nicht der Geometrie entsprach: Kühlmittelaufwärmung vergessen (B-BAT-038), 120 Kanäle statt weniger Bahnen (B-BAT-043), Rahmen um eine Größenordnung zu weich geschätzt (B-BAT-042). Regel: Vor jeder ERWARTUNG ein automatisch erzeugter Steckbrief des Bauteils aus CAD/parameter.json (Anzahlen, Querschnitte, Lastpfad).
2. **Billige Vorrechnung vor teurer Rechnung:** Die Verteilerrechnung (Sekunden) verhinderte eine Elmer-Rechnung mit falscher Annahme. Regel: Jede FEM/CFD-Rechnung hat eine analytische oder 1D-Vorrechnung als Tor.
3. **Modellprüfungen von Anfang an:** Der ungültige Crash (Zellreihen ohne Kontakt) fiel erst am Bild auf; danach Kriterium max |U|. Regel: Plausibilitätskriterien (Verschiebung, Energie, Massenzugabe) gehören in die Vorlage der ERWARTUNG, nicht erst nach dem Fehler.
4. **Abbruchkriterien für die Maschine:** LFP_b rechnete 2,5 h instabil weiter. Wächter (Zeitschritt, Energiefehler, Laufzeit, Restart-Datei) jetzt für jeden Lauf; Schwellen offline an alten Läufen testen (Fehlalarm im Fall b gefunden).
5. **Kollisionen laufend prüfen:** G5 begann mit 67 Kollisionen (B-BAT-036/037). Regel: Kollisionsprüfung nach jeder CAD-Änderung, nicht am Ende.
6. **Eine Quelle für Maße:** Widersprüche CAD ↔ Rechnung (HV-Länge 2024 statt 779 mm, Gruppenverbinder 75/45 mm²). Regel: Rechnungen lesen Maße aus parameter.json bzw. dem CAD, nicht aus Abschriften.
7. **Anforderungen schärfen, bevor gerechnet wird:** ΔT ≤ 5 K ohne Definition; ECE R100 aus dem Gedächtnis, nicht am Normtext geprüft. Regel: zu jeder Anforderung Messgröße, Ort und Lastfall festlegen und vom Autor bestätigen lassen.
8. **Bilder mit Zielband (Vorgabe Autor) bewährt;** zusätzlich Drucktauglichkeit prüfen (abgeschnittene Beschriftungen).
9. **Rechenzeit gezielt einsetzen:** Varianten s10/s40 brachten keinen Erkenntnisgewinn (< 1 %). Regel: Varianten nach erwartetem Informationsgewinn auswählen.
10. **Freigaben bündeln:** ENT-104 bis 150 sind noch offen; Regel: feste Freigaberunden mit dem Autor.
11. **Orchestrierung:** Aufträge mit Abbruchbedingung „Erwartung verfehlt → zurück, nicht anpassen“ haben mehrfach gegriffen (K5, Wächter-Schwelle). Beibehalten.
