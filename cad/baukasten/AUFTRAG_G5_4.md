# AUFTRAG G5.1b + G5.4 (Sonnet): Stücklisten-Korrekturen und einfache Teile

KI-generiert (Claude Opus, 2026-11-19). Verbindlich: PLAN.md §3, §3a, §4. Vorlage für den Stil: teile/gehaeuse.py, teile/kuehlung.py, kern.py.

## G5.1b Korrekturen SL3 (Opus-Entscheidungen zu deinen offenen Punkten)
1. BT-440 als „Stromschiene“ erweitert: in Ordnung. FPC-Halter → BT-361 (vorhandenes Bauteil) statt 360.2. Zellträger NMC bei BT-250: in Ordnung. Verguss bei BT-220: in Ordnung; bei BT-220 die Variante NMC in struktur.json ergänzen.
2. Dichten Stahl 7850, Kunststoff 1200 und Dichtung (EPDM 1150) gelten. Sie stehen jetzt in cad/baukasten/farben.json („werkstoffe“). Die Stückliste nimmt die Dichten von dort, nicht aus einem eigenen Feld. Farbnamen → farben.json „farbnamen“.
3. Seitenrahmen 500.4: Menge **4** (2 Längs-, 2 Querprofile).
4. Mengen, die noch „offen“ sind (Opus-Entscheidung, Herkunft „Opus 2026-11-19“):
   - BT-220 LFP Zwischenlage: eine je Spalt zwischen benachbarten Zellen eines Feldes, also 250 − 2 × 4 = **242**. Dicke = A_zellabstand_LFP_mm, Fläche = Zellfläche, Werkstoff Mica, Stufe K, Generator zelle.zwischenlage.
   - BT-240 LFP Verspannung: **entfällt als Teil**, Detailstufe „-“. Querträger und Rahmen nehmen die Quellkraft auf (Cell-to-Pack). Das in die Bemerkung schreiben.
   - BT-350 Isolationswächter **1** (in der Schaltbox). BT-570 Druckausgleich **1** und BT-750 Entgasungsventil **1**, beide an der Rückwand. BT-640 Temperaturfühler Kühlmittel **2** (an den Anschlüssen). BT-780 Typschild **1** (auf dem Deckel). Formen kommen aus W34, solange keine Formangabe da ist, gilt Stufe H mit Vermerk.
5. Normteile (590.x), Dichtungen 580.1 und FPC-Detail 360.3: `menge_quelle: "CAD"`. montage.py übernimmt dann die Stückzahl aus der Geometrie.
6. masse_ges_kg für BT-510…560 und 610…630 bleibt der alte Wert, bis G5.7 läuft. Danach liest stueckliste_v3.py die Massen aus cad/baukasten/ausgabe/ergebnis_<V>.json (Schalter `--aus-cad`), das bitte jetzt vorbereiten.
7. pm/kosten/kosten.py für SL3 anpassen, damit die fehlenden BT Positionen sind (G5.9 vorgezogen, nur lauffähig machen, keine neuen Preise).

## G5.4 Einfache Teile (neue Module in cad/baukasten/teile/)
Die Logik der Lage nimmst du aus cad/pack/pack_e2d.py, e2d_geo.py und e2_verdrahtung.py. Den Code überträgst du in die neue Form und änderst ihn nicht nur oberflächlich:
- Maße nur aus `p()`/`a()`. Neue Detailmaße kommen nach `annahmen_g5.json` mit Herkunft „Annahme Sonnet G5.4: …“. Jede davon nennst du in der Rückgabe.
- Ausschnitte über `ctx.schneide(shape, [BT…])` statt der alten cutter-Liste.
- Je Generator ein Docstring: BT, Akten, Parameter, Annahmen, Stufe.
- Kaufteile werden lokal gebaut und mit `kern.setze()` an `ctx.einbau[BT]` gesetzt (PLAN §3a). Fehlt ein Einbauort, gibt der Generator 0 Teile zurück und meldet das. Einbauorte in der Schaltbox setzt Opus (schaltbox.py, läuft parallel).

| Modul | Generatoren (Namen genau wie in SL3) | Stufe | Hinweise |
|---|---|---|---|
| zelle.py | zelle_prismatisch, zelle_rund, zwischenlage, pad, verguss, zelltraeger | F/K | Lagen aus ctx.zellen. Blade: Kanten gerundet (Radius als Annahme), Pole als Laschen an den Stirnseiten. Maße der Pole: cad/zelle/aufbau_W20.json bzw. die Akten ENT-032…080. 4680: Pol-Nippel und Schulter oben. Pad mit Ausschnitten aus ctx (automatisch). |
| verbinder.py | zellverbinder_lfp (249!), zellabgriff (1736), gruppenverbinder, gruppenbruecke, hv_leitung, pol_lasche, stromschiene, beruehrschutz, trennbruecke, **gehaeuse.servicedeckel** (hier registrieren, weil er an der Trennbrücke liegt) | K | HV-Leitung: Rohrzug mit Biegeradius aus BT-430 von der Pol-Lasche zu ctx.schaltbox["hv_eingang"]. Stromschienen in der Box: Lagen aus ctx.schaltbox["schienen"] (Opus). Fehlt der Eintrag, bleibt die Position vorerst leer. |
| elektronik.py | cmu, fpc, fpc_halter, fpc_detail, daisy_kette, ntc; bms_platine, shunt, isolationswaechter (diese drei an ctx.einbau) | F | CMU hochkant in den Endzonen wie e2d. Platinen mit Bauteilandeutung (Stecker, 2–3 Bausteine) und Bohrungen. |
| kaufteile.py | schuetz_haupt, schuetz_vorlade, sicherungen, trennstecker (NMC), hv_stecker, nv_stecker, gassensor, druckausgleich, entgasungsventil, temperaturfuehler_kuehlmittel, typschild | F | Formen: Körper gerundet, Anschlussbolzen mit Mutter, Fußlaschen, Spulenstecker (Schütz: A_e2d_schuetz_*). Schütz so bauen, dass er auch **liegend** eingebaut werden kann (lokal +x = Bolzenrichtung). Maße W33-bestätigt: forschung/W31_W33_bestaetigt.md; W34 folgt. |
| normteile.py | schraube, kabelschuh, clip, schrumpfschlauch, dichtung | F | Schrauben mit echtem Kopf (Sechskant, Flachkopf ISO 7380 über kern.flachkopf, Senkkopf), Lagen von den Teilen, die verschraubt werden. Dafür legt jedes Modul seine Schraubstellen in `ctx.schrauben.append(dict(typ, d, l, placement))` ab. normteile baut sie alle. |

Test je Modul: `PACK_VARIANTE=LFP G5_NUR=zelle,… G5_STEP=0 $FREECAD_APPIMAGE freecadcmd cad/baukasten/montage.py`, danach NMC. Ergebnis: cad/baukasten/ausgabe/pruefung_<V>.txt. Erst wenn beide Varianten bei deinen Modulen 0 Kollisionen und keine Stückzahlfehler zeigen, ist die Arbeit fertig. Kollisionen mit Opus-Teilen (Gehäuse, Kühlung, Schaltbox) meldest du, lösen musst du sie nicht.

Rückgabe an Opus (≤ 8 Zeilen): Module fertig, Teile/Masse je Variante, neue Annahmen (Liste), Kollisionen mit Opus-Teilen, Laufzeit. Bei einem Widerspruch zu einer Akte brichst du ab und meldest ihn (PLAN §5).
