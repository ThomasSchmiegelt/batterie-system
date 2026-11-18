| Dok.-Nr. | ERW-G2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung G2: parametrische Zelle (LFP verkürzte Blade, NMC 4680) in FreeCAD | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Vor dem CAD festgelegt. Maße aus den Akten ENT-014…029 (vorgeschlagen) bzw. ENT-008…011 (entschieden).

## Erwartung (Prüfgrößen am Modell)
1. **LFP-Zelle:** Quader 660 × 90 × 14 mm, Außenvolumen 0,832 L. Wand 0,3 mm. Zwei Pole an den Stirnseiten (Lage aus W20: Pole an beiden Enden; Maße Pol = **Annahme**, im Modell als Parameter mit Kennzeichnung). Energie je Volumen: 295,6 Wh / 0,832 L ≈ 355 Wh/L (wie gemessen).
2. **NMC-4680:** Zylinder Ø 46 × 80 mm, Volumen 0,133 L (W20: 133 mL), Wand 0,4 mm. Pole: Plus oben mittig, Minus Becherrand (Annahme für Maße).
3. **Masse aus Volumen** ist nicht prüfbar (Innenaufbau nicht modelliert) → Masse wird als Akte geführt, nicht aus CAD.
4. Modell liest **nur** parameter_<V>.json; ändert man dort eine Länge, ändert sich das Modell ohne Codeänderung.
5. Ausgabe: STEP je Variante, PNG-Ansicht (isometrisch, Maßpfeile oder Maßtext), Volumen-Ausgabe in ergebnis.json.

## Verfehlt
- Volumen weicht um mehr als 1 % von 1. bzw. 2. ab.
- Ein Maß steht im Code statt im Parameter.

## Nachtrag 2026-11-17: Detailmodell Innenaufbau (ENT-015 korrigiert, ENT-031…080), vor dem Modell
1. **LFP:** Stapel aus 38 Kathoden (20 + 2 × 70 µm), 39 Anoden (10 + 2 × 65 µm), 78 Separatorlagen (12 µm) = **12,48 mm**, passt in 14 − 2 × 0,3 = 13,4 mm innen (Rest ≈ 0,9 mm für Isolationsbeutel und Spiel). Elektroden 615,5/620/631 mm lang; Zelle 681 mm → Endzonen je Seite ≈ 25–33 mm für Fahnen, Stromschiene, Halter, Pol.
2. **4680:** Wickel aus Kathode–Separator–Anode–Separator, Dicke je Windung 0,45 mm; Kathode 3215 mm → **≈ 34 Windungen**, Außenradius ≤ 22,6 mm (Becher innen), Kern Ø ≈ 14 mm. Anode (3305 mm) und Separatoren (3550 mm) länger als Kathode (Überstände).
3. Breiten: LFP Elektroden 82,5/85 mm, Separator 87 mm in 90 − 0,6 mm innen; 4680 Kathode 72, Anode 73, Separator 75 mm in 80 mm Höhe (Rest für Tab-Scheiben, Deckel, Boden).
4. Alles, was W20 nicht bemaßt (Halter, Stromschienendicke, Pole, Dichtring, Ventil, Füllniet), als `ANNAHME_*` im Skript und im Bild gekennzeichnet.
## Verfehlt
- LFP-Stapel passt nicht in die Innendicke oder 4680-Wickel ragt über den Becher.
- Windungszahl 4680 außerhalb 30–38.
