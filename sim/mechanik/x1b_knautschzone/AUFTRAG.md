| Dok.-Nr. | Auftrag X1b/X2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Knautschzone (CalculiX) und dynamischer Pfahl (OpenCourant) | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> KI-generiert, Opus → Sonnet, 2026-11-18. Grundlage ist ERWARTUNG.md, keine eigenen Annahmen.

**Teil A: X1b mit CalculiX.** Modell aus `../x1_seitencrash/x1.py`, Knautschprofil wie in der Annahme. w 15, 20, 30, je LF1 (zwischen den Querträgern) und je Variante.
- Pfahlweg bis zur Zellberührung, mindestens bis w + 5 mm.
- Ausgabe: Kraft und Energie bei Zellberührung, PEEQ, Energieverlust in %, Bild `kraft_weg_w.png` mit Zielband, Verformung je w.
- Läufe mit `setsid nohup nice … < /dev/null &`, ein Hintergrundbefehl wartet auf sie, kein Abfragen in Schleife.

**Teil B: OpenCourant, erst nach Teil A.**
1. Quelle nur github.com/OpenCourant/OpenCourant bzw. die offizielle Download-Seite dort, Linux-x86-64-Build.
2. Ziel `/home/cae/cae_projekte/werkzeuge/opencourant/`, nichts systemweit, kein sudo.
3. Prüfsumme festhalten, wenn sie angegeben ist. Eintrag in `docs/10_lizenzen_und_quellen.md`: AGPLv3, intern genutzt, nicht weitergegeben. Eintrag in SOFTWARE.md mit Version.
4. Rauchtest mit einem mitgelieferten Beispiel.
5. Dann X2: Starter- und Engine-Deck für die Variante und das w mit dem besten Verhältnis aus Ziel und Energieverlust (aus Teil A), Pfahl 1500 kg bei v aus der Annahme.
6. Ausgabe: Kraft-Zeit, Eindringung-Zeit, Energiebilanz (intern, kinetisch, Hourglass), Vergleich mit X1b, Bild mit Zielband.

`ERGEBNIS.md` mit Abgleich gegen die Erwartung, `lesehilfe.md`, Folienbaustein `praesentation/bausteine/X1b.md`.
Abbruch → OPUS: Verfehlt-Fall, Download oder Lizenz unklar, kein Rauchtest. Rückgabe höchstens 5 Zeilen.
