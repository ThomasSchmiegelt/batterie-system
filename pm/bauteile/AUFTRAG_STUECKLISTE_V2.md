| Dok.-Nr. | Auftrag SL2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Stückliste auf Konstruktionsstand je Variante, Kostenspalte vorbereitet | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet, 2026-11-18. Autor: „du kannst dich schon um die Stückliste kümmern und auch eine Kostenbewertung vornehmen.“ Anforderung REQ-P16 (vorgeschlagen), Vorgang SL2.

**Ziel:** `stueckliste.py --variante LFP|NMC` bildet das Pack ab, wie es konstruiert ist, und nicht mehr den Startwert-Entwurf.
**Eingaben:** `struktur.json` (60 BT), `parameter_<V>.json` sowie die vorgeschlagenen Akten über `cad/pack/entwurf_parameter.py`, `cad/pack/entwurf/ergebnis_<V>.json` und `ergebnis_<V>_e2.json` (Mengen, Massen), `sim/elektrik/e1_querschnitte/ergebnis.json`.

1. **Positionen:**
   - Jede Position hat genau ein BT (`bt`).
   - Fehlt für ein gebautes Teil ein BT, etwa CMU-Platine, FPC, Stromschienen, Servicedeckel, Trennbrücke oder Dichtungen: nicht anlegen, sondern auflisten. Opus erweitert dann `struktur.json`.
2. **Felder neu:**
   - `menge_<V>` (aus CAD/Akten, mit Quellpfad)
   - `masse_je_kg`, `masse_ges_kg` (CAD, sonst „offen“)
   - `art` (K Kaufteil / E Eigenteil)
   - `werkstoff`
   - `kosten_je_eur` und `kosten_ges_eur`: leer lassen, diese Spalten füllt die Kostenrechnung.
   - `quelle`
3. **Summen je Variante:** Masse gesamt gegen `pack_massen.py` (Abweichung > 2 % melden). Zellzahl gegen 250 (LFP) bzw. 868 (NMC).
4. **Ausgaben:** `docs/13_stueckliste_<V>.md` mit Version 0.2 und Dokumentkopf, `stueckliste_<V>.json`. Dazu ein Bild `docs/bilder/stueckliste_massen_<V>.png` mit Masse je Baugruppe als Balken und Lesehilfe.
5. **Kostenrechnung vorbereiten:** `pm/kosten/kosten.py` liest `stueckliste_<V>.json` und `pm/kosten/eingaben.json` und schreibt `ergebnis_<V>.json` mit €/Stück, €/Pack und €/kWh je Baugruppe. `eingaben.json` legst du als Gerüst an: je BT ein Feld `eur_je` mit `{wert: null, einheit, herkunft}`. Die Werte trägt Opus ein, du rechnest nichts mit erfundenen Preisen.

E2 läuft parallel (cad/pack/pack.py). Dort nichts ändern, nur lesen. E2-Massen sind Stand v1.0, die Stückliste wird nach E2 v1.1 neu erzeugt.
Abbruch → OPUS: fehlendes BT, Massen > 2 % daneben, Widerspruch zwischen Akte und CAD. Rückgabe höchstens 5 Zeilen.
