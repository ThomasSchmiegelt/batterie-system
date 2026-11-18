| Dok.-Nr. | ERW-C2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung C2: Parametersätze Blade-LFP und 4680 aus Zerlegung + Literatur, kalibriert | Ersteller | Claude Opus (KI) | Prüfer | – |

> KI-generiert, vor der Rechnung. Autor: „der richtige parametersaz ist wichtig. erst den“. Grundlage: W20 (Geometrie, DCIR Abb. 8), W24/W28 (4680, LFP-Werte, nach pruefe.py), Blade-Pulsdaten Test#5 (Borealis doi:10.5683/SP3/RPCWBY, CC BY 4.0), PyBaMM-Materialsätze Prada2013 (LFP/Graphit) und Chen2020/ORegan2022 (NMC811/Graphit) als Ausgangspunkt (Annahme).
## Vorgehen (Methode Opus)
1. **Blade 135 Ah zuerst** (Messdaten vorhanden): Geometrie aus W20 (Original-Zelle), Materialsatz Prada; kalibrieren in dieser Reihenfolge: (a) OCV/Kapazität aus langsamer Entladung oder Pulspausen von Test#5, (b) 10-s-Pulswiderstand über SOC bei 25 °C (Kontaktwiderstand, Elektrolytleitfähigkeit, Austauschstrom), (c) Temperaturabhängigkeit (Arrhenius-Aktivierungsenergien) an −10/0/40 °C. Gütemaß: RMS-Fehler Spannung im Puls.
2. Danach auf **unsere 92,4-Ah-Zelle** nur über Elektrodenfläche skalieren (Akten ENT-032…047).
3. **4680:** Geometrie W20/W24 (Akten ENT-057…072), Materialsatz Chen2020; kalibrieren an DCIR W20 Abb. 8 und W24 (5,4–7 mΩ); keine Pulsdaten → schwächer belegt (so kennzeichnen).
4. Schnellladen neu: LFP 2,1C 20 min; 4680 CC-CV mit größtem Startstrom, der 10→80 % in 30 min schafft, mit Prüfung Anodenpotential ≥ 0 V gg. Li (Plating-Grenze).
## Erwartung
1. Blade 135 Ah: 10-s-Widerstand 25 °C, 50 % SOC ≈ 0,8–1,2 mΩ (W20 ≈ 1,0); bei −10 °C 2–4-fach. RMS Spannung ≤ 15 mV nach Kalibrierung.
2. Unsere LFP-Zelle: ≈ 1,2–1,75 mΩ; Wärme Schnellladen 2,1C ≈ 45–65 W (K1: 55 W).
3. 4680: 10→80 % in 30 min braucht Startstrom ≈ 1,7–2,0C; mittlere Wärme ≈ 8–12 W (K1b: 6,7 W) → K1b für 4680 mit Modellwärme neu nötig; Plating-Grenze könnte 30 min verhindern.
## Verfehlt
RMS > 30 mV; Blade-DCIR außerhalb 0,5–2 mΩ; 4680 erreicht 30 min auch mit 3C nicht.
