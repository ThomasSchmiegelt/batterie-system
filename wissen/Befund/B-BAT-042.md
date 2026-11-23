---
typ: befund
tags: ["befund"]
---
# B-BAT-042

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

Quetschfall LFP_b instabil, Löser rechnete 2,5 h ohne Alarm (2026-11-23, Opus)

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- –

## Text aus BEFUNDE.md

- Bei t = 5,16 ms brach im Kontakt Zellknoten–Schalen der Zeitschritt auf 1e-12 ms ein, die Energien stiegen auf 1e19. Der Löser meldete trotzdem „NORMAL TERMINATION“, schrieb keine Restart-Datei, und erst der nächste Abschnitt brach ab. Weder Warteschlange noch Auswertung hatten ein Kriterium dafür.
- Korrektur ERWARTUNG Nachtrag 4: für Fall b Kontaktsteifigkeit Istf = 4, Massenzugabe statt Zeitschrittkollaps (/DT/NODA/CST), Wächter in lauf.sh (Abschnitt > 45 min oder ohne Restart-Datei = FEHLER). Umsetzung Sonnet mit Probelauf bis 8 ms.
- Lehre: Neben „Erwartung vor dem Ergebnis“ braucht auch die Maschine Abbruchkriterien, sonst verbraucht ein unsinniger Lauf stundenlang Rechenzeit.
- Nachtrag (23.11.): Die Korrektur nach Nachtrag 4 (Istf = 4, /DT/NODA/CST) machte den Lauf instabiler (Kollaps schon bei 0,535 ms) und wurde verworfen (Nachtrag 5). LFP_b wird aus dem alten Lauf bis 5 ms ausgewertet: Bei 100 kN verformt sich der Rahmen um 0,4 mm, die Zellen praktisch gar nicht. Bis 693 kN, also etwa dem Siebenfachen der Prüfkraft, wächst die Rahmenverformung auf 2,9 mm. Die Grenze von 10 mm ist weit eingehalten. Die Erwartung von Opus (2–8 mm Weg bis 100 kN) war um eine Größenordnung zu weich, weil der Lastpfad axial über die Querträger läuft. Was oberhalb von etwa 700 kN passiert, ist nicht gerechnet, und die Ursache der Instabilität bleibt offen.
- NMC_a (5 kJ Pfahl, 23.11.): Pfahl 13,9 mm, Zellen 8,3 mm, 440 kN, Energiefehler 0,1 %, max |U| der Zellen 13,5 mm (Grenze 1,5 × 13,9 = 20,9 mm), kin 2,7 %, Modellprüfung ok. Opus hat das Verformungsbild angesehen. Der Streifen im Querträgerspalt bei x ≈ 975 mm, der sich nach innen bis etwa 15 mm verschiebt, ist plausibel der Querträger, der die Pfahllast aufnimmt; die Zellblöcke bleiben ruhig. Am Bildaufbau (Leerraum links, abgeschnittene Beschriftungen) muss vor dem Druck nachgebessert werden.
- Schärferer Wächter (Nachtrag 6) ist eingesetzt: Fall a mit dt < dt0/10 oder |ERROR| > 10 %, Fall b nur dt. Die Offline-Prüfung an allen Läufen ergab keinen Fehlalarm; der instabile LFP_b hätte bei 5,160 ms ausgelöst. NMC_b läuft noch mit der alten Fassung (Start 09:47, Austausch 09:54).
- NMC_b (Quetschung bis 5 ms, 23.11.): bei 100 kN Zellen 0,07 mm, Rahmen < 10 mm erfüllt; bis 739 kN Zellen 2,6 mm, max |U| 3,3 mm, Modellprüfung ok. Damit sind alle X3-Fälle gerechnet. PI_PRUEFUNG X3: Energiebilanz in allen a-Fällen < 0,25 %. Die Pfahl-Eindringung liegt in allen 5-kJ-Fällen mit 13,6–13,9 mm knapp unter dem Band aus Nachtrag 3 (15–40 mm), das Pack ist also steifer als erwartet. LFP_a2 (20 kJ, 38 mm) liegt im Band.
