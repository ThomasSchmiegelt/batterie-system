| Dok.-Nr. | DEU-K1 | Version | 1.0 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Deutung K1: Schnellladen | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> KI-generiert (Opus, 2026-11-17). Grundlage ergebnis.json (Stichprobe Meta LFP/NMC K3), P0-Abgleich 0,0000 K, Wärmeintegral ≤ 0,34 %.
1. **LFP:** Beidseitige Kühlung (K3) erfüllt bei 20 min beide Vorgaben (33,8 °C / 4,6 K; mit h 1000: 30,8 °C / 3,8 K). Alternativ Begrenzung auf 30 min: 34,1 °C / 5,4 K (knapp verfehlt).
2. **Stufenladen** bringt thermisch nichts (LFP 44,1 °C / 11,3 K gegen 43,1 / 10,6), **Puls bzw. Zellen im Wechsel** verschlechtert stark (61,7 °C / 21,3 K) – wie vorab aus ∫I²dt erwartet.
3. **Bessere Kühlung (h) und Vorkühlung** senken nur T_max, nicht die Spreizung – bestätigt. Bei NMC steigt ΔT mit h sogar leicht (kühlerer Boden bei gleicher Kernspitze).
4. **Nachtrag (Tab-Scheibe statt Luft, Netz Kern r 6,25):** NMC K3 P0 38,9 °C / 5,8 K (knapp verfehlt), P3 (25 min) 34,0 °C / 3,8 K → **NMC erfüllt REQ-P09 mit Kühlung oben+unten und 25 min**. Ersatzleitfähigkeit des 3,6-mm-Spalts (k_z 31, Annahme Sonnet: Tab-Scheibe + gefaltete Fahnen) ist die stärkste neue Annahme.
4a. Erste Fassung: **NMC K3 verfehlt (47,9 °C / 12,3 K) wegen Modellannahme**: Im Netz liegt zwischen Wickel und Deckel Luft (k 0,026). Real verbindet die Al-Tab-Scheibe (tabless) den Wickel flächig mit dem Deckel. Das Ergebnis ist deshalb **nicht belastbar**; Nachrechnung mit Tab-Scheibe als Leiter nötig (Fehler der Erwartung/Vorgabe Opus: Anbindung oben nicht spezifiziert).
5. Erwartungsfehler Opus: Zeitkonstanten unterschätzt (P1-Spitze erst bei 810 s; NMC P3/P4 kühler als erwartet).
Offen: K0-NMC-Netz mit Kern r 7,0 statt 6,25 mm (Volumen +2 %, Wirkung < 0,5 K erwartet) – bei Nachrechnung NMC K3 mit aktualisieren.

6. **K1b (Opus):** Mit oberer Kühlung über Verbinder + Pad (h_eff 214) erfüllt die 4680 REQ-P09 bei 30 min (33,3 °C / 3,8 K), bei 25 min knapp nicht (36,86 / 5,47 K). Hebel: Bedeckung der Oberseite durch Verbinder (φ 0,7 → 4,7 K). Autor entschied 30 min (REQ-P05). Erwartung lag 1–3 K zu hoch.
