| Dok.-Nr. | Auftrag B1-c | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Projektbericht Fassung 0.3: Stand 2026-11-18 | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet. Autor 2026-11-18: „jetzt bericht ergänzen, hochladen, crash“. Es gelten die Regeln aus AUFTRAG_BERICHT.md: jede Zahl mit Fundstelle, Lesehilfe je Bild, Bilder nach bericht/bilder kopieren, keine eigene Rechnung.

**Vorher (mechanisch):** Stückliste und Kosten aus dem Detailstand neu erzeugen:
- `python3 pm/bauteile/stueckliste.py --variante LFP|NMC` mit den Massen aus `cad/pack/entwurf/ergebnis_<V>_e2d.json`, wo vorhanden.
- Danach `pm/kosten/kosten.py` und die Bilder.
- HV-Länge direkt aus `e2`/`e2d` übernehmen, nicht aus dem Volumen.
- Die neuen Zahlen in docs/13 und docs/18 übernehmen. Weichen die Summen um mehr als 3 % von B-BAT-028/029 ab → melden.

**Neu bzw. zu ändern in `bericht/bericht.tex`, Version 0.3:**
1. Zellmodell C1/C2 (B-BAT-022, 023): NMC 10→80 % in 36 min, LFP-Parametersatz passt nicht, Blade 0,877 mΩ gemessen, 4680 schafft 30 min bei 1,5C, Plating-Risiko. Risiken R-PLAT und R-4680W.
2. Kühlung: K1c (LFP 32,7 °C / 4,0 K; 4680 34,0 / 4,15 bzw. 39,1 / 6,5) und K2 Kühlplatte (B-BAT-021, laminar, 4-mm-Kanäle, Durchfluss ENT-107/108). Werte mit Quellpfad aus `sim/kuehlung/`.
3. Neues Kapitel „Elektronik und Kabel E2“ (B-BAT-024…027, `sim/elektrik/e2_elektronik/ERGEBNIS.md` v1.1):
   - Schaltbox als Turm unter der Rücksitzbank (ENT-144), LFP-Trennbrücke (ENT-150), Mäander bzw. Schleife (ENT-145/148).
   - Verluste: HV 15,2/11,3 W, Al 75,6/316 W.
   - Bilder: e2_<V>_draufsicht, kabelplan_<V>, schaltbild_<V>, e2d_LFP_boxoffen, e2d_LFP_bruecke_zu.
   - Offen: Detailstand noch quaderhaft, Überarbeitungsschleife geplant (Autor).
4. Neues Kapitel „Stückliste und Kosten“ (SL2/KO1, docs/13_<V>, docs/18):
   - Massen je Baugruppe, €/Pack, €/kWh, Zellanteil.
   - Deutlich hinschreiben: Alle Preise sind Schätzungen, verifiziert ist nur der BNEF-Packpreis 97 USD/kWh. REQ-P16 hat keinen Zielwert.
   - Bilder: stueckliste_massen_<V>, kosten_vergleich.
5. Kapitel Fehler ergänzen (Ereignisse aus BEFUNDE B-BAT-024…029):
   - Opus-Erwartung HV ≤ 15 W war physikalisch unmöglich.
   - Vorgabe „Mitte hinten“ hat einen Scheinkonflikt erzeugt.
   - Fall b vorne verletzt die Packhöhe (Autor löst das mit der Rücksitzbank).
   - Kosten Lauf 1: Fertigung auf Zellen, Kühlplatte Vollmaterial.
   - Detailtiefe stand nicht im Auftrag.
   - E1 15×3 gegen Akte 25×3.
6. Entscheidungen aus docs/04 neu (150 Akten, Status zählen). Offene Punkte: Freigaben ENT-104…150, Crash X1, Überarbeitungsschleife E2, Zählwidersprüche B-BAT-028.
7. Zusammenfassung aktualisieren (½ Seite).

Zweimal kompilieren, 0 Fehler. Die neuen Seiten als Bild ansehen. Folienbausteine E2, SL2, KO1 prüfen und nachführen. Höchstens 60 min. Rückgabe höchstens 4 Zeilen.
