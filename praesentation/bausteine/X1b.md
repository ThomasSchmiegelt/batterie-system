| Dok.-Nr. | FOLIE-X1b | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Folienbaustein X1b: Knautschzone im Seitenaufprall | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert**, Claude Sonnet, 2026-11-18. Entwurf; Zwischenstand (Probe LFP w20), Aussage vorläufig.

**Kernaussage (1 Satz):** Eine 20 mm breite Knautschzone aus Aluminium am Seitenrahmen hält die Kraft (mittel 80 kN), nimmt aber bei einem 5-kJ-Pfahlaufprall die Energie nicht auf, bevor die Zelle berührt wird (Zellkörper-Spalt bei 0,47 kJ erreicht).

**Bild:** `sim/mechanik/x1b_knautschzone/kraft_eindringung_oc.png`, Zielband: Kraft ab 100 kN, Energie 5 kJ, Innenwand unter 1 mm Verschiebung.

**Zahlen (Quelle `sim/mechanik/x1b_knautschzone/ergebnis_oc.json`, Fall `LFP_w20`):** mittlere Kraft bis w 80,1 kN (`kraft_mittel_bis_w_kN`), Spitze 131,7 kN (`kraft_max_kN`), Zellberührung bei 4 mm Spalt nach 466 J (`zellberuehrung.4.energie_J`), maximale Eindringung 50,1 mm (`eindringung_max_mm`), Energiefehler 0,0072 % (`energiefehler_proz_max`), Energieverlust im Pack 2,35 % (`energieverlust_proz`). Zweitbild: `verformung_oc_LFP_w20.png`.

**Trend:** Energie bis Zellberührung (Spalt 4 mm) 416 J (w15), 455 J (w20), 568 J (w30) (`zerlegung_bei_zellberuehrung.4.energie_J`), Ziel 5 kJ; etwa die Hälfte des Wegs ist Ausweichen des ganzen Rahmens. Bild `energie_bis_zellberuehrung_ueber_w.png`.

**Methode:** CalculiX (implizit) divergierte beim Falten dünner Wände, deshalb explizite Rechnung mit OpenCourant. Gegenprüfung der Anfangssteifigkeit: 7,6 % Abweichung zu CalculiX bei 2 mm.

*KI-generiert, Entwurf. Dokument FOLIE-X1b, Version 0.1.*
