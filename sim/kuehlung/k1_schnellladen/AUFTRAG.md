| Dok.-Nr. | Auftrag K1 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Schnellladen: Ladeprofile, Kühlvarianten, Begrenzung (Elmer, Fortsetzung K0) | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-17. Erwartung `ERWARTUNG.md` (nicht ändern). Grundlage: `../k0_zelle/` (Skripte wiederverwenden: importieren oder kopieren, K0-Dateien nicht ändern; VTU-Ablage wie K0 unter /home/cae/cae_projekte/batterie/k1_schnellladen/, hier nur Link `elmer`).

## Ziel
1. `eingaben.json`: Profile P0–P4, Kühlfälle Kh1000, Kh2000, K3, V15, Kombinationen genau wie in ERWARTUNG.md, Herkunft je Wert (Autor-Zitat / Annahme Opus). Strom zeitabhängig: Q(t) = I(t)²·R als tabellierte Wärmequelle (Elmer: `Heat Source = Variable Time; Real` mit Tabelle; Puls P2 mit genügend Stützstellen und Zeitschritt ≤ 5 s, sonst ≤ 10 s).
2. Netz: f1 aus K0 (Netzstudie dort 0,017 K). Rechnen: zuerst P0 beider Varianten als Abgleich mit K0 L2 (> 0,3 K Abweichung → Stopp, an Opus). Dann alle Fälle aus der Erwartung für LFP und NMC. Laufzeit messen.
3. `auswertung.py`: je Fall T_max(t), ΔT_Kern(t), Spitzenwerte und Werte bei Ladeende, Zeit über 45 °C, Zeit über 5 K, Wärmeintegral ∫Q dt (Prüfung gegen Tabelle ±2 %), Ladezeit. `ergebnis.json`, `ERGEBNIS.md` (Kopf, Tabellen, Abgleich ERWARTUNG Punkt für Punkt, keine Deutung), `ERGEBNIS_kurz.txt`.
4. Bilder (Zielbereich + Lesehilfe, `k1_lesehilfe.md`):
   - `profile.png`: Ladestrom über Zeit der Profile P0–P4 (oben) und Ladezustand (unten).
   - `verlauf_profile_<V>.png`: T_max und ΔT über Zeit je Profil, Vorgaben 45 °C / 5 K als Linien.
   - `verlauf_kuehlung_<V>.png`: dasselbe für die Kühlfälle.
   - `landkarte.png`: Ergebnisraster (Zeilen Fälle, Spalten LFP/NMC, je T_max-Spitze und ΔT-Spitze, Ampel gegen REQ-P09).
   - Gerenderte Bilder: den bestandenen bzw. besten Fall je Variante mit dem neuen Cycles-Renderskript aus `../k0_zelle/` (wird parallel gebaut: `render_cycles.py`; falls bei deinem Ende noch nicht vorhanden, Render auslassen und melden).
5. `praesentation/bausteine/K1.md` (Kernaussage „(Opus)“), `pm/plan/bilder.py` Zuordnung k1_schnellladen → K1, laufen lassen.
## Abbruch und Rückgabe
CPU only, `nice -n 10`, ein Lauf ≤ 15 min, gesamt ≤ 90 min (bei Zeitnot Kombinationen zuerst streichen). Läuft parallel zu einem Blender-Auftrag (k0_zelle/render*) – dessen Dateien nicht anfassen. Nicht ändern: Akten, ERWARTUNG.md, K0-Dateien. Rückgabe ≤ 15 Zeilen. **→ OPUS**: P0-Abgleich verfehlt, Wärmeintegral > 2 %, verfehlte Erwartung, fehlende Eingabe.
