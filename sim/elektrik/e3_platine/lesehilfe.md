| Dok.-Nr. | LH-E3 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe Bilder E3 (CMU-Platine, Ausgleich, Vorladung) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.

## platine_LFP.png, platine_NMC.png
- **Was man sieht:** Die Überwachungsplatine (CMU) von oben und von unten, gerendert aus der KiCad-Datei. Oben stehen die Bauteile: die breiten dunklen Blöcke sind die Ausgleichswiderstände (sie verheizen überschüssige Ladung einer Zelle), daneben je ein kleiner Schalter (FET), in der Mitte der Mess-Chip, links der flache Anschluss für die Zellabgriffe, rechts die Übertrager und die Anschlüsse zur nächsten Platine.
- **Zielband:** Der rote Rahmen ist der geforderte Umriss 120 x 60 mm. Alles liegt innerhalb.
- **Wichtig:** Die Platine ist bestückt, geroutet (Freerouting) und geprüft (DRC). Die dünnen Linien sind die Leiterbahnen, kleine Punkte die Durchkontaktierungen.
## schaltbild_cmu.png
- **Was man sieht:** Blockbild der Schaltung: Zellabgriffe, Filter, Mess-Chip, Ausgleich, Übertrager, Sekundärschutz. Es gibt kein Zielband, weil es ein Schaltbild ist. Das vollständige Schaltbild ist die Netzliste `cmu_<V>.net`.
## ausgleich_LFP.cir / ergebnis_ausgleich.json (Zahlen)
- Der Ausgleichsstrom sinkt mit der Zellspannung (Widerstand fest). Bei Nennspannung dauert der Ausgleich rund 14 % länger als bei voller Zelle.
## platine_LFP_explosion.png, platine_NMC_explosion.png
- **Was man sieht:** Die Platine wie ein Lagenkuchen auseinandergezogen (Blender). Von oben: Bauteile, F.Cu, Substrat, In1, In2, B.Cu, darunter das Wärmeleitpad (gelb, 1,0 mm, ENT-185) und der Al-Rahmen mit dem Ausschnitt. Kupfer ist kupferfarben. Die Stäbe sind die Durchkontaktierungen (Vias); die orangen sind die Thermovias unter den Ausgleichswiderständen (ENT-187): LFP 144 von 144, NMC 144 von 144.
- **Wichtig:** Die Vias sitzen im eigenen Netz der Widerstandspads und enden auf einer Kupferfläche auf B.Cu je Widerstandsnetz. Die Abstände der Lagen und die Kupferdicke sind nur zur Darstellung überhöht. Zielband entfällt (Geometriebild).
## platine_LFP_einbau.png, platine_NMC_einbau.png
- **Was man sieht:** Oben das Pack von schräg oben; Zellen und Deckel sind ausgeblendet, alles außer den CMU ist grau und durchsichtig. Die orangen Streifen sind die Platinen in den Endzonen. Unten eine Nahansicht der Platinen einer Endzone vor dem Boden/Rahmen. Zielband entfällt (Geometriebild).
- **Masse:** Platine ohne Pad LFP 27,2 g, NMC 27,2 g; Pad 21,6 g (Quelle ergebnis_platine.json, Dichten aus ERWARTUNG Nachtrag 6).
## Pack
- `pack_<V>_e2d_e3.step` zeigt die Platine anstelle des 10-mm-Quaders; die Platine ist mit Steckern rund 10,9 mm dick, 0,9 mm mehr als der Platz.

## Lesehilfe je Bild (für docs/16)

**Lesehilfe zu `platine_LFP.png`** Die Überwachungsplatine der Variante LFP von oben (Bestückung) und von unten (Kupferflächen und Durchkontaktierungen), in den roten Rahmen = Zielband 120 x 60 mm gezeichnet. Alles liegt innerhalb. Die Platine ist vollständig verdrahtet und geprüft (DRC 0 Verstöße, 0 offene Verbindungen). Unten sind die Kupferflächen unter den Ausgleichswiderständen zu sehen (Wärmeableitung, 144 von 144 Thermovias).

**Lesehilfe zu `platine_LFP_3d_iso.png`** Schrägansicht der Platine LFP (KiCad 3D). Die Platine von schräg oben mit Bauteilen, hellen Leiterbahnen und gelben Via-Ringen. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_LFP_3d_top.png`** Oberseite der Platine LFP (KiCad 3D). Draufsicht auf die Bestückung; die Leiterbahnen schimmern durch die grüne Lötstoppmaske. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_LFP_3d_bottom.png`** Unterseite der Platine LFP (KiCad 3D). Unterseite ohne Bauteile; zu sehen sind die Kupferflächen unter den Widerstandspaaren, Bahnen und Via-Punkte. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_LFP_3d_nah.png`** Nahaufnahme Ausgleichskanal der Platine LFP (KiCad 3D). Ein Ausgleichskanal: zwei große Widerstände (verheizen Ladung), ein kleiner Schalter (FET) und Filterteile; die Vias liegen unter den Widerständen und sind verdeckt. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_LFP_explosion.png`** Die Lagen der Platine LFP wie ein Lagenkuchen nach oben auseinandergezogen (Blender): Bauteile, F.Cu, Substrat, In1, In2, B.Cu, darunter das Wärmeleitpad (ENT-185, 1,0 mm) und der Al-Rahmen mit dem Ausschnitt. Kupfer ist kupferfarben; die orangen Stäbe sind die Thermovias unter den Ausgleichswiderständen (ENT-187): 144 von 144. Abstand der Lagen und Kupferdicke sind nur zur Darstellung überhöht. Kein Zielband (Geometriebild).

**Lesehilfe zu `platine_LFP_einbau.png`** Das Pack LFP mit den CMU-Platinen am Einbauort in den Endzonen (Blender). Zellen und Deckel sind ausgeblendet, alles außer den Platinen ist grau und durchsichtig; oben die Übersicht, unten eine Nahansicht der Endzone. Platinenmasse 27,2 g, mit Wärmeleitpad 48,9 g. Kein Zielband (Geometriebild).

**Lesehilfe zu `platine_NMC.png`** Die Überwachungsplatine der Variante NMC von oben (Bestückung) und von unten (Kupferflächen und Durchkontaktierungen), in den roten Rahmen = Zielband 120 x 60 mm gezeichnet. Alles liegt innerhalb. Die Platine ist vollständig verdrahtet und geprüft (DRC 0 Verstöße, 0 offene Verbindungen). Unten sind die Kupferflächen unter den Ausgleichswiderständen zu sehen (Wärmeableitung, 144 von 144 Thermovias).

**Lesehilfe zu `platine_NMC_3d_iso.png`** Schrägansicht der Platine NMC (KiCad 3D). Die Platine von schräg oben mit Bauteilen, hellen Leiterbahnen und gelben Via-Ringen. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_NMC_3d_top.png`** Oberseite der Platine NMC (KiCad 3D). Draufsicht auf die Bestückung; die Leiterbahnen schimmern durch die grüne Lötstoppmaske. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_NMC_3d_bottom.png`** Unterseite der Platine NMC (KiCad 3D). Unterseite ohne Bauteile; zu sehen sind die Kupferflächen unter den Widerstandspaaren, Bahnen und Via-Punkte. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_NMC_3d_nah.png`** Nahaufnahme Ausgleichskanal der Platine NMC (KiCad 3D). Ein Ausgleichskanal: zwei große Widerstände (verheizen Ladung), ein kleiner Schalter (FET) und Filterteile; die Vias liegen unter den Widerständen und sind verdeckt. Es gibt kein Zielband, weil es ein Geometriebild ist; der Umriss 120 x 60 mm steht in der Kopfzeile.

**Lesehilfe zu `platine_NMC_explosion.png`** Die Lagen der Platine NMC wie ein Lagenkuchen nach oben auseinandergezogen (Blender): Bauteile, F.Cu, Substrat, In1, In2, B.Cu, darunter das Wärmeleitpad (ENT-185, 1,0 mm) und der Al-Rahmen mit dem Ausschnitt. Kupfer ist kupferfarben; die orangen Stäbe sind die Thermovias unter den Ausgleichswiderständen (ENT-187): 144 von 144. Abstand der Lagen und Kupferdicke sind nur zur Darstellung überhöht. Kein Zielband (Geometriebild).

**Lesehilfe zu `platine_NMC_einbau.png`** Das Pack NMC mit den CMU-Platinen am Einbauort in den Endzonen (Blender). Zellen und Deckel sind ausgeblendet, alles außer den Platinen ist grau und durchsichtig; oben die Übersicht, unten eine Nahansicht der Endzone. Platinenmasse 27,2 g, mit Wärmeleitpad 48,9 g. Kein Zielband (Geometriebild).

**Lesehilfe zu `schaltbild_cmu.png`** Blockbild der Schaltung der CMU: Zellabgriffe, Filter, Mess-Chip, Ausgleich, Übertrager, Sekundärschutz. Es gibt kein Zielband, weil es ein Schaltbild ist; das vollständige Schaltbild ist die Netzliste `cmu_<V>.net`.

**Lesehilfe zu `spice_ausgleich_vorladung.png`** Links der Ausgleichsstrom über der Zellspannung (sinkt mit der Spannung, Widerstand fest), rechts die Vorladung des Hochvoltkreises über den Widerstand. Die Zahlen stehen in `ergebnis_ausgleich.json` und `ergebnis_vorladung.json`; Zielbänder aus der Erwartung sind im Bild eingezeichnet, soweit es eines gibt.

*KI-generiert (Claude Sonnet, 2026-11-24).*
