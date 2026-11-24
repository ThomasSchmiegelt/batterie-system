| Dok.-Nr. | Auftrag E3 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | CMU-Leiterplatte in KiCad, Ausgleich und Vorladung in SPICE | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> KI-generiert, Opus → Sonnet, 2026-11-24. Grundlage: `ERWARTUNG.md` (nicht ändern, keine eigenen Annahmen; fehlt etwas → als offene Frage melden). Nur CPU, `nice`. Die GPU wird nicht genutzt.

## Ziel
Die CMU (BT-321…325) wird bis zu MOSFET und Widerstand detailliert, als Code-Schaltplan und Layout. Vorladung und Ausgleich sind per SPICE nachgerechnet. Das Platinen-STEP kommt in den Pack.

## Schritte
1. **Werkzeuge ohne sudo** (sudo ist nicht verfügbar):
   - KiCad 9: `flatpak remote-add --user --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo && flatpak install --user -y flathub org.kicad.KiCad`. `kicad-cli` über `flatpak run --command=kicad-cli org.kicad.KiCad`, Wrapper `werkzeuge/kicad-cli.sh`.
   - ngspice: `apt-get download ngspice libngspice0` und weitere fehlende Abhängigkeiten, dann `dpkg -x` nach `~/.local/opt/ngspice`. Den Pfad in `umgebung.sh` eintragen.
   - Python: `skidl`, `PySpice` (oder `spicelib`) in `.venv`, in `requirements.txt` aufnehmen.
   - Versionen in `SOFTWARE.md`. Lizenzen (KiCad GPL-3, KiCad-Bibliotheken CC-BY-SA 4.0 mit Ausnahme, ngspice, SKiDL MIT) in `docs/10_lizenzen_und_quellen.md`.
   - Geht etwas nicht → OPUS.
2. **Akten:** Für jede Zeile der Annahmen-Tabelle `python3 pm/pm.py neu "…" BT-xxx merkmal`, Wert eintragen. Status „vorgeschlagen“, wer „Opus (Annahme ERW-E3)“, belege [B-BAT-050], anforderungen passend (REQ-P15/P17/P18/P19). Danach `pm.py pruefe` mit 0 Fehlern und `pm.py register`.
3. **SPICE** (`spice_ausgleich.py`, `spice_vorladung.py`, Netzlisten im Ordner):
   - Ausgleich je Variante: Kennlinie I(U_Zelle) von U_min bis U_max, Verlust R und FET. Nimm ein generisches FET-Modell (Level 1, R_DS,on aus der Tabelle). Herstellermodelle nur mit geklärter Lizenz.
   - Vorladung bei 912 V: i(t), u_C(t), Energie im Widerstand, t_95.
   - Ergebnisse → `ergebnis.json`. Bilder mit Zielband nach Erwartung.
4. **Schaltplan als Code** (`cmu_skidl.py`): Liest die Werte aus `pm/bauteile/parameter.json`, und zwar aus Akten mit dem Status „entschieden“ und „vorgeschlagen“. Fehlt ein Wert, nimmt es `A_*` aus der Erwartung mit Herkunft „ERW-E3“. Inhalt:
   - AFE als eigenes generisches Symbol
   - 18 Kanäle mit Filter, 2 Widerständen und FET
   - NTC-Eingänge, 2 Übertrager, Sekundärschutz BT-325 mit eigener Abschaltleitung
   - FPC-Stecker, 2 Daisy-Chain-Stecker
   Ausgabe: Netzliste, Stückliste CSV, Schaltplan-PDF (falls SKiDL/KiCad es erzeugen kann, sonst Blockbild mit schemdraw).
5. **Layout** (KiCad, per Skript `pcbnew` oder IPC-API):
   - Umriss aus BT-321, 4 Lagen
   - Netzklassen mit den Kriechstrecken aus der Tabelle
   - Platzierung per Skript, Ausgleichswiderstände über die Fläche verteilt
   - Routing mit Freerouting, falls installierbar, sonst nur die kritischen Netze und Ratsnest dokumentieren
   - Prüfen: `kicad-cli pcb drc` und `kicad-cli sch erc` (bzw. Netzlisten-Prüfung). Berichte in den Ordner.
   - Ausgaben: Gerber und STEP nach `/home/cae/cae_projekte/batterie/e3/` (groß, nicht ins Repo), Bild der Platine (Ober- und Unterseite, PNG) ins Repo
6. **Pack:** STEP statt des CMU-Quaders in `cad/pack/` (Schalter E3, bestehende Skripte erweitern, nicht ersetzen). Kollisionsprüfung beider Varianten, Masse.
7. **Bericht:**
   - `ERGEBNIS.md` v0.1 mit Abgleichtabelle Erwartung 1–7 (ok/verfehlt) und Wärmeabschätzung (Erwartung 3)
   - `lesehilfe.md`
   - Folienbaustein `praesentation/bausteine/E3.md`
   - Bilder in `docs/16_ergebnisbilder.md`
   - Zeile in `docs/08_ki_einsatz_protokoll.md`

≤ 180 min. Rückgabe ≤ 5 Zeilen. Abbruch → OPUS wie in der Erwartung.

## Fortsetzung Bilder (Opus, 2026-11-24, Wunsch Autor: „im rendering die leiterbahnen darstellen und eine explosionsansicht“)
Erst nach vollständigem Routing (Lauf 3) und mit den Vias nach ENT-187:
1. **KiCad-3D** (`$KICAD_CLI pcb render`, quality high, Projektdateien in einem Ordner unter /home/cae/cae_projekte, weil der Flatpak /tmp nicht lesen kann): je Variante iso (`--rotate -50,0,30 --perspective --floor`), top, bottom, dazu eine Nahaufnahme eines Ausgleichskanals (zoom) mit sichtbaren Leiterbahnen und Vias.
2. **Explosionsansicht** (Blender Cycles CPU wie `cad/pack/render_pack.sh`):
   - Quelle: `kicad-cli pcb export step` mit Bauteilen **und Kupfer** (`--include-tracks --include-pads --include-zones`, falls vorhanden). Umwandeln über FreeCAD in Netze je Objekt.
   - Ebenen von oben nach unten auf der Z-Achse auseinandergezogen: Bauteile · F.Cu · Substrat · In1.Cu · In2.Cu · B.Cu (mit Vias als Stäbe durch alle Ebenen) · Wärmeleitpad (ENT-185, 1,0 mm) · Ausschnitt Al-Rahmen. Je Ebene eine eigene Farbe, Kupfer kupferfarben.
   - Beschriftung der Ebenen mit Akte (BT-321, ENT-168/185/187).
   - Dazu eine zweite Ansicht: die CMU an ihrem Einbauort im Pack (Ausschnitt Endzone, Rest grau-transparent).
3. Alle Bilder mit Kopfzeile, Lesehilfe-Zeile und dem Vermerk „KI-generiert, Entwurf“ (Muster: `platine_NMC_3d_*.png`). PNG ins Repo, `.blend` nach /home/cae/cae_projekte/batterie/e3/. `pm/plan/bilder.py` nachführen, Baustein E3 nachführen.

## Fortsetzung Schaltplan (Opus, 2026-11-24, Wunsch Autor: „ich möchte auch einen schaltplan haben“)
Bisher gibt es nur die SKiDL-Netzliste und ein Blockbild, keinen echten Schaltplan. Ziel: **echter KiCad-Schaltplan `.kicad_sch`**, aus derselben Quelle wie das Layout (`cmu_skidl.py` bzw. parameter.json), damit Schaltplan und Platine nicht auseinanderlaufen.
1. Weg (der Reihe nach probieren):
   - (a) SKiDL `generate_schematic()`, falls es mit KiCad 10 lesbare Dateien erzeugt.
   - (b) sonst ein eigenes Skript `schaltplan.py`, das die `.kicad_sch` mit fester Anordnung schreibt.
2. Gliederung, **hierarchisch**:
   - Deckblatt (Blockübersicht mit Akten)
   - Blatt „Kanal“ einmal gezeichnet und 18-mal instanziiert: Filter-RC, 2 Widerstände, Doppel-FET, Abgriff
   - Blatt „AFE und Versorgung“
   - Blatt „Sekundärschutz“ (3 × 6 Zellen, wired-OR)
   - Blatt „Daisy-Chain“ (Übertrager, TVS, Stecker)
   - Blatt „NTC und Stecker“
3. Jedes Bauteil mit Referenz, Wert und Aktenverweis im Feld (z. B. `ENT-171`). Schriftfeld mit Dok.-Nr., Version, „KI-generiert, Entwurf“.
4. Prüfen:
   - `kicad-cli sch erc` mit 0 Fehlern
   - Netzliste aus dem Schaltplan (`kicad-cli sch export netlist`) = Netzliste des Layouts (Skript-Vergleich, 0 Abweichungen)
5. Ausgabe:
   - `schaltplan_<V>.pdf` (`kicad-cli sch export pdf`) und PNG je Blatt ins Repo
   - `.kicad_sch` nach /home/cae/cae_projekte/batterie/e3/
   - in docs/16 und Baustein E3 aufnehmen
