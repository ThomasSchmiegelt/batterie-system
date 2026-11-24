---
typ: dokument
datei: "praesentation/bausteine/E3.md"
tags: ["dokument", "kopie"]
---
# E3

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/bausteine/E3.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf. Folienbaustein Vorgang E3.

# Die CMU-Platine bis zu Widerstand und Schalter
**Kernaussage: Die Überwachungsplatine passt mit allen 108 Teilen in 120 x 60 mm, der Ausgleich verheizt aber rund 10 W, die Platine braucht Kühlung über die Kühlplatte.**

**Bild:** sim/elektrik/e3_platine/platine_NMC_explosion.png (Explosionsansicht nach Lagen, beschriftet mit BT-321, ENT-168/185/187), platine_NMC_einbau.png (CMU am Einbauort), platine_LFP.png (Zielband: Umriss 120 x 60 mm, roter Rahmen)

**Zahlen** (Quellen sim/elektrik/e3_platine/ergebnis_ausgleich.json, ergebnis_vorladung.json, ergebnis_waerme.json, ergebnis_platine.json):
- Ausgleich je CMU LFP 9,99 W, NMC 9,64 W; bei Nennspannung Ausgleich rund 14 % länger
- Übertemperatur ohne Kühlpfad 67 bis 139 K (Abschätzung, über 105 °C)
- Vorladung 912 V: 9,12 A Spitze, 415,8 J im Widerstand
- Platine vollständig geroutet (4 Lagen, DRC 0 Verstöße, 0 offene Verbindungen, Quelle ergebnis_platine.json); 3D-Bilder platine_NMC_3d_*.png
- Thermovias im eigenen Netz mit B.Cu-Fläche je Widerstandsnetz: LFP 144 von 144, NMC 144 von 144 (davon 1 mit 0,45/0,2 mm als Ausnahme) (Quelle thermovias_<V>.json, ergebnis_platine.json)
- Masse der Platine ohne Pad LFP 27,2 g, NMC 27,2 g, Wärmeleitpad 21,6 g (Quelle ergebnis_platine.json)

*KI-generiert, Entwurf.*

