| Dok.-Nr. | Auftrag C0b + Stückliste je Variante | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Variantenvergleich LFP-Blade/NMC-4680 mit Messwerten; Stückliste je Variante | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-16. Akten: ENT-005 (LFP, [LFP]), ENT-006 (800 V), ENT-007…011 (NMC 4680, [NMC]), ENT-012 (Baum mit `varianten`, vorgeschlagen).

## Teil 1: Rechnung `sim/chemie/varianten_lfp_nmc/`
- `varianten.py`: gleicher Rechenweg wie `sim/chemie/vergleich_lfp_nmc/AUFTRAG.md` Schritte 1–9 (Code dort wiederverwenden, Grundannahmen aus `../vergleich_lfp_nmc/eingaben.json` lesen), Zellwerte aus `eingaben.json` hier. Unterschiede:
  - U_sys aus `vorgaben.systemspannung_V`. s = ceil(U_sys/U_zelle).
  - LFP: p = 1, Ah = E_brutto/(s·U) (Ausgabe). Zellband w ∈ [160, 185, 210] (unten, Mitte = Bandmitte, oben); Hauptwert 160 (gemessen) zusätzlich ausgeben.
  - NMC: Ah fest 23,125 → p = ceil(E_brutto·1000/(s·U·Ah)); E_ist = s·p·U·Ah; Zellmasse = s·p·355 g; Packmasse = Zellmasse/k. In Fall B mit E_ist iterieren. Zellwert fest (kein Band), nur k-Band.
  - Bauraum: nötige Pack-Wh/L gegen Zelle_Wh_L × Volumennutzung (LFP 0,60; NMC Band 0,40–0,60) → „erfüllt / knapp (±2 %) / nicht erfüllt“.
- Ausgaben: `ergebnis.json`, `packmasse.png` (wie C0: Balken Mitte, Fehlerbalken k-Band; Grenze 30 % beschriftet, nicht über den Balken), `packmasse_lesehilfe.md`, `ERGEBNIS.md` (Kopf, Tabellen, **Abgleich mit ERWARTUNG.md Punkt für Punkt**, keine Deutung), `ERGEBNIS_kurz.txt` (≤ 15 Zeilen), `praesentation/bausteine/C0b.md` (Kernaussage „(Opus)“).

## Teil 2: `pm/bauteile/stueckliste.py --variante V`
- Ist `BT-100 nennspannung_V` bzw. `kapazitaet_Ah` in `parameter_<V>.json` entschieden, gelten diese Werte (statt A_U_ZELLE / Ableitung). Dann p = ceil(E·1000/(s·U·Ah)), Energie = s·p·U·Ah.
- Positionen, deren Bauteil in `struktur.json` ein Feld `varianten` ohne V hat, entfallen in der Variante (Hinweis „entfällt bei V“ im Kopf). Für BT-250 Zellhalter eine neue Position (nächste freie Nummer in 200.x, Menge 1 Satz, nur NMC, Bemerkung „Maße offen, G4“).
- Läufe: `--variante LFP`, `--variante NMC`, ohne Variante; danach `pm.py pruefe`, `wissensnetz.py`, `wissensnetz_ansicht.py`.

## Abbruch und Rückgabe
- Fertig, wenn alles fehlerfrei läuft. Abbruch nach 30 min. Nicht ändern: ENT-Akten, struktur.json, eingaben.json, ERWARTUNG.md, forschung/.
- Rückgabe ≤ 15 Zeilen: Kernzahlen je Variante und Fall, Abgleich Erwartung (erfüllt/verfehlt), Stückliste je Variante (s×p, Zellen, kWh, Positionen).
- **→ OPUS**: verfehlte Erwartung, fehlende Eingabe, Widerspruch Stückliste ↔ Rechnung.
