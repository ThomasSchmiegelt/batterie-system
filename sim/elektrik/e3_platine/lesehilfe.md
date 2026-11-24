| Dok.-Nr. | LH-E3 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe Bilder E3 (CMU-Platine, Ausgleich, Vorladung) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf, nicht freigegeben.

## platine_LFP.png, platine_NMC.png
- **Was man sieht:** Die Überwachungsplatine (CMU) von oben und von unten, gerendert aus der KiCad-Datei. Oben stehen die Bauteile: die breiten dunklen Blöcke sind die Ausgleichswiderstände (sie verheizen überschüssige Ladung einer Zelle), daneben je ein kleiner Schalter (FET), in der Mitte der Mess-Chip, links der flache Anschluss für die Zellabgriffe, rechts die Übertrager und die Anschlüsse zur nächsten Platine.
- **Zielband:** Der rote Rahmen ist der geforderte Umriss 120 x 60 mm. Alles liegt innerhalb.
- **Wichtig:** Die Platine ist bestückt, geroutet (Freerouting) und geprüft (DRC). Die dünnen Linien sind die Leiterbahnen, kleine Punkte die Durchkontaktierungen.
## schaltbild_cmu.png
- **Was man sieht:** Blockbild der Schaltung: Zellabgriffe, Filter, Mess-Chip, Ausgleich, Übertrager, Sekundärschutz. Es gibt kein Zielband, weil es ein Schaltbild ist. Der vollständige Schaltplan steht im Abschnitt zu schaltplan_<V>. Das ältere Blockbild ist die Netzliste `cmu_<V>.net`.
## schaltplan/schaltplan_<V>_*.png und cmu_<V>_schaltplan.pdf
- **Was man sieht:** Der Schaltplan der Platine in KiCad-Form. Das Deckblatt zeigt die Blöcke mit Verbindungen, das Kanalblatt eine Messstelle (Abgriff, Filter, zwei Ausgleichswiderstände, Doppel-FET), die auf dem Blatt „Kanäle“ 18-mal verwendet wird. Dazu Blätter für AFE, Sekundärschutz, Daisy-Chain, NTC und Stecker.
- **Zielband:** entfällt (Schaltplan). Prüfung: ERC 0 Fehler und Netzliste gleich der Platine (ergebnis_schaltplan.json).
- **Wichtig:** Die Symbole sind generische Kästen; Aktenverweise stehen im Feld „Akte“.
## ausgleich_LFP.cir / ergebnis_ausgleich.json (Zahlen)
- Der Ausgleichsstrom sinkt mit der Zellspannung (Widerstand fest). Bei Nennspannung dauert der Ausgleich rund 14 % länger als bei voller Zelle.
## platine_LFP_explosion.png, platine_NMC_explosion.png
- **Was man sieht:** Die Platine wie ein Lagenkuchen auseinandergezogen (Blender). Von oben: Bauteile, F.Cu, Substrat, In1, In2, B.Cu, darunter das Wärmeleitpad (gelb, 1,0 mm, ENT-185) und der Al-Rahmen mit dem Ausschnitt. Kupfer ist kupferfarben. Die Stäbe sind die Durchkontaktierungen (Vias); die orangen sind die Thermovias unter den Ausgleichswiderständen (ENT-187): LFP 144 von 144, NMC 144 von 144.
- **Wichtig:** Die Vias sitzen im eigenen Netz der Widerstandspads und enden auf einer Kupferfläche auf B.Cu je Widerstandsnetz. Die Abstände der Lagen und die Kupferdicke sind nur zur Darstellung überhöht. Zielband entfällt (Geometriebild).
## platine_LFP_einbau.png, platine_NMC_einbau.png
- **Was man sieht:** Oben das Pack von schräg oben; Zellen und Deckel sind ausgeblendet, alles außer den CMU ist grau und durchsichtig. Die orangen Streifen sind die Platinen in den Endzonen. Unten eine Nahansicht der Platinen einer Endzone vor dem Boden/Rahmen. Zielband entfällt (Geometriebild).
- **Masse:** Platine ohne Pad LFP 27,6 g, NMC 27,6 g; Pad 21,6 g (Quelle ergebnis_platine.json, Dichten aus ERWARTUNG Nachtrag 6, Bauteilmassen Nachtrag 8).
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

**Lesehilfe zu `schaltplan_LFP_deckblatt.png`** Deckblatt des Schaltplans: die Blöcke Sekundärschutz, NTC und Stecker, AFE, Daisy-Chain und Kanäle mit den Verbindungen ABSCHALT, NTC1-4, TX und RX über Blattpins. Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_LFP_kanaele.png`** Das Blatt Kanäle des Schaltplans: 18 gleiche Messkanäle als Unterblätter; die Pins hängen an den Zellabgriffen, Messeingängen und Gates. Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_LFP_kanal.png`** Ein Messkanal (wird 18-mal verwendet): Zellabgriff, Filter-Widerstand mit Kondensator zum Mess-Chip, zwei Ausgleichswiderstände parallel und der Doppel-FET (zwei Schalter in Reihe) zum Abgriff darunter. Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_LFP_afe.png`** Das Blatt AFE und Versorgung: der Mess-Chip mit Filterwiderstand am Abgriff 0 und vier Kondensatoren an der Versorgung. Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_LFP_sekundaerschutz.png`** Das Blatt Sekundärschutz: drei Überspannungsschutz-Bausteine für je sechs Zellen, ihre Ausgänge sind zusammen auf ABSCHALT gelegt (wired-OR). Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_LFP_daisy.png`** Das Blatt Daisy-Chain: zwei Übertrager mit Stecker und Überspannungsableiter zur galvanisch getrennten Verbindung zum Nachbarmodul. Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_LFP_ntc_stecker.png`** Das Blatt NTC und Stecker: Zellabgriff-Stecker mit 24 Pins und die vier Anschlüsse für externe Temperaturfühler. Variante LFP. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_deckblatt.png`** Deckblatt des Schaltplans: die Blöcke Sekundärschutz, NTC und Stecker, AFE, Daisy-Chain und Kanäle mit den Verbindungen ABSCHALT, NTC1-4, TX und RX über Blattpins. Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_kanaele.png`** Das Blatt Kanäle des Schaltplans: 18 gleiche Messkanäle als Unterblätter; die Pins hängen an den Zellabgriffen, Messeingängen und Gates. Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_kanal.png`** Ein Messkanal (wird 18-mal verwendet): Zellabgriff, Filter-Widerstand mit Kondensator zum Mess-Chip, zwei Ausgleichswiderstände parallel und der Doppel-FET (zwei Schalter in Reihe) zum Abgriff darunter. Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_afe.png`** Das Blatt AFE und Versorgung: der Mess-Chip mit Filterwiderstand am Abgriff 0 und vier Kondensatoren an der Versorgung. Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_sekundaerschutz.png`** Das Blatt Sekundärschutz: drei Überspannungsschutz-Bausteine für je sechs Zellen, ihre Ausgänge sind zusammen auf ABSCHALT gelegt (wired-OR). Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_daisy.png`** Das Blatt Daisy-Chain: zwei Übertrager mit Stecker und Überspannungsableiter zur galvanisch getrennten Verbindung zum Nachbarmodul. Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.

**Lesehilfe zu `schaltplan_NMC_ntc_stecker.png`** Das Blatt NTC und Stecker: Zellabgriff-Stecker mit 24 Pins und die vier Anschlüsse für externe Temperaturfühler. Variante NMC. Es gibt kein Zielband, weil es ein Schaltplan ist; geprüft wird mit ERC (0 Fehler) und dem Vergleich der Netzliste mit der Platine (0 Abweichungen, ergebnis_schaltplan.json). Generische Symbole, Aktenverweise im Feld Akte. KI-generiert, Entwurf.
