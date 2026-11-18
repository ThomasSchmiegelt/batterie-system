| Dok.-Nr. | BAT-DOC-13 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Abschlussvideo: Storyboard | Ersteller | Claude Opus (KI) | Prüfer | – |

> **KI-generiert.** Entsteht ganz am Schluss aus dem fertigen CAD. Hier nur der Plan.

## Regeln (Autor)
- Im Bild steht nur „Thomas Schmiegelt“ unten. Erklärungen gehören in den Begleittext bzw. Sprechertext, nicht ins Bild.
- Jede Szene zeigt ein Bauteil aus `pm/bauteile/struktur.json`. Der Begleittext nennt die Entscheidungen (ENT-…), die die Form bestimmt haben. Er entsteht aus `pm.py kontext <BT>`, nicht frei formuliert.
- Einzelbilder erst nach Freigabe löschen.

## Szenen (Reihenfolge = Entstehung)
| Nr | Bauteil | Bild | Begleittext (Quelle) |
|---|---|---|---|
| 1 | BT-100 Zelle | Zelle entsteht: Elektrodenlagen, Gehäuse, Pole, Ventil | Chemie und Maße (ENT zu BT-100) |
| 2 | BT-200 Zellstack | Zellen reihen sich, Verspannung | Verschaltung, Zellzahl |
| 3 | BT-300 Regelung (BMS) | Platinen und Messleitungen erscheinen | Messumfang, Schutz |
| 4 | BT-400 Verkabelung | Zellverbinder, Hochvoltleitungen | Querschnitte, Verluste |
| 5 | BT-500 Struktur | Träger, Rahmen, Gehäuse, Deckel | Bauraum, Crash, Cell-to-Pack |
| 6 | BT-600 Kühlung | Kühlplatte, Kanäle, Strömung (FluidX3D), Temperatur (Elmer) als Farbe | Auslegungsfall Schnellladen |
| 7 | BT-700 Zusatzkomponenten | Schütze, Sicherung, Stecker, Entgasung | Schutzkonzept |
| 8 | BT-000 Gesamtsystem | Rundflug, Explosionsdarstellung, Zusammenfahren | Erfüllung der Anforderungen (docs/03) |

## Technik
FreeCAD (Maße nur aus `pm/bauteile/parameter.json`) → Export glTF/STL je Bauteil → Blender (Kamera, Licht, Einblenden in Reihenfolge) → ffmpeg.
Ergebnisbilder aus Elmer und FluidX3D als Textur oder eingeblendete Ebene. Ausgabe `video/abschluss.mp4` und `video/begleittext.md` (DE/EN).
