#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-17), Entwurf. Erzeugt ERGEBNIS.md, ERGEBNIS_kurz.txt, k0_lesehilfe.md, bilder/render_lesehilfe.md und den Folienbaustein K0 aus ergebnis.json (alle Zahlen von dort)."""
import json, os, datetime
H = os.path.dirname(os.path.abspath(__file__)); R = os.path.abspath(f"{H}/../../..")
D = json.load(open(f"{H}/ergebnis.json")); F = D["faelle"]; ZT, ZD = D["ziel_T_max_C"], D["ziel_dT_K"]
def meta(n): return json.load(open(f"{H}/elmer/fall_{n}/meta.json"))
def g(n, k): return F[n][k]
datum = datetime.date.today().isoformat()
kopf = lambda nr, titel: f"| Dok.-Nr. | {nr} | Version | 0.1 | Status | Entwurf |\n|---|---|---|---|---|---|\n| Titel | {titel} | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | – (Opus offen) |\n\n> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Stand {datum}. Quelle aller Zahlen: `sim/kuehlung/k0_zelle/ergebnis.json` (erzeugt von `auswertung.py` aus `elmer/fall_*/`).\n\n"
fuss = "\n---\n*KI-generiert (Claude Sonnet), Entwurf, nicht vom Menschen freigegeben.*\n"
HF = ["LFP_K1_L1", "LFP_K1_L2", "NMC_K1_L1", "NMC_K1_L2", "NMC_K2_L1", "NMC_K2_L2"]
def zeile(n):
    r = F[n]; m = r["meta"]; ok_t = "ja" if r["T_max_C"] <= ZT else "nein"; ok_d = "ja" if r["dT_kern_K"] <= ZD else "nein"
    return f"| {n} | {m['P_W']:.2f} | {r['T_max_C']:.1f} | {r['T_kern_min_C']:.1f} | {r['dT_kern_K']:.1f} | {ok_t} | {ok_d} | " + (f"{r['bilanz_abw_prozent']:+.3f} %" if 'bilanz_abw_prozent' in r else f"{r['bilanz_transient_abw_prozent']:+.3f} % (Energie)") + " |"
s = [kopf("ERG-K0", "Ergebnis K0: Wärmesimulation einer Zelle je Variante (Elmer)")]
s.append(f"""## Was getan wurde
Elmer-Wärmeleitung (HeatSolver) mit einem homogenisierten, orthotropen Kern, Gehäuse als eigene Schicht, Luft im NMC-Kernloch und in den LFP-Endzonen, Wärmequelle Q = I²·R gleichmäßig im Kern. Netz mit gmsh (nur Hexaeder), je Fall Netzstudie auf zwei Stufen. Alle Eingaben aus `eingaben.json` und `cad/zelle/entwurf/parameter_<V>_entwurf.json`. Grenzen **T_max ≤ {ZT:g} °C und ΔT ≤ {ZD:g} K sind Vorgabe (REQ-P09, Autor 2026-11-17)**. K1 (Boden gekühlt, ENT-081) ist Hauptfall, K2 nur Vergleich. Rechnung CPU, ein Kern.

## Hauptergebnisse (ΔT = Kern max − Kern min; T_max über die ganze Zelle)
| Fall | Wärme (W) | T_max (°C) | T_min Kern (°C) | ΔT Kern (K) | T_max ≤ {ZT:g} | ΔT ≤ {ZD:g} | Bilanz (Quelle − Kühlrand) |
|---|---|---|---|---|---|---|---|
""" + "\n".join(zeile(n) for n in HF))
s.append(f"""
Bei L2 (transient, 1200 s) stehen T_max und ΔT zum Endzeitpunkt t = 1200 s; die Zelle ist dort nicht stationär (Kühlrandleistung am Ende: LFP {g('LFP_K1_L2','Q_kuehlrand_W'):.1f} von {g('LFP_K1_L2','Q_quelle_W'):.1f} W, NMC K1 {g('NMC_K1_L2','Q_kuehlrand_W'):.1f} von {g('NMC_K1_L2','Q_quelle_W'):.1f} W, NMC K2 {g('NMC_K2_L2','Q_kuehlrand_W'):.1f} von {g('NMC_K2_L2','Q_quelle_W'):.1f} W).

Zeitpunkte (L2, Quelle `ergebnis.json` → `faelle.<Fall>.t_Tmax45_s` bzw. `t_dT5_s`; ΔT nur auf dem Raster t = 30, 70, 110, … s ausgewertet: erster Rasterpunkt mit ΔT ≥ Vorgabe):
| Fall | T_max erreicht {ZT:g} °C bei (s) | ΔT erreicht {ZD:g} K bei (s) |
|---|---|---|
""" + "\n".join(f"| {n} | {g(n,'t_Tmax45_s') if g(n,'t_Tmax45_s') is not None else 'nie in 1200 s'} | {g(n,'t_dT5_s')} |" for n in ("LFP_K1_L2", "NMC_K1_L2", "NMC_K2_L2")))
s.append("\n## Eingänge der Rechnung (aus `elmer/fall_*/meta.json`)\n| Fall | C-Rate | Strom (A) | R (mΩ) | Wärme Q (W) | Q/V Kern (W/m³) | Kernleitfähigkeit (W/(m·K)) | h (W/(m²·K)) | Kühlfläche (mm²) | Knoten |\n|---|---|---|---|---|---|---|---|---|---|")
for n in HF:
    m = meta(n); s.append(f"| {n} | {m['C_rate']:.2f} | {m['I_A']:.1f} | {m['R_mOhm']:.3f} | {m['P_W']:.2f} | {m['q_W_m3']:.0f} | {m['orient']} | {m['h']:g} | {m['A_kuehlrand_mm2']:.0f} | {m['n_knoten']} |")
s.append("\nVergleich Leitfähigkeit LFP (L1/L2, K1): Hauptfall W18 gegen Schichtmischung\n| Fall | T_max (°C) | ΔT Kern (K) |\n|---|---|---|")
for n in ("LFP_K1_L1", "LFP_K1_L1_mischung", "LFP_K1_L2", "LFP_K1_L2_mischung"): s.append(f"| {n} | {g(n,'T_max_C'):.1f} | {g(n,'dT_kern_K'):.1f} |")
s.append("\n## Netzstudie (L1, Feinheit 1 gegen 2, doppelte Elementzahl je Richtung)\n| Fall | T_max f1 (°C) | T_max f2 (°C) | Differenz (K) | ΔT f1 (K) | ΔT f2 (K) | Knoten f1 / f2 |\n|---|---|---|---|---|---|---|")
for n, r in D["netzstudie"].items(): s.append(f"| {n} | {r['T_max_f1']:.3f} | {r['T_max_f2']:.3f} | {r['diff_K']:+.3f} | {r['dT_f1']:.2f} | {r['dT_f2']:.2f} | {r['knoten_f1']} / {r['knoten_f2']} |")
s.append("\nKriterium aus dem Auftrag: Änderung von T_max < 0,5 K. Die Stufe 2 der NMC-Fälle lief mit iterativem Löser (BiCGStab/ILU2), weil der direkte Löser (Umfpack) bei 122 000 Knoten den Speicher überschritt.")
s.append("\n## Empfindlichkeit L1 (K1, ΔT Kern, jeweils ein Parameter; Bänder aus `eingaben.json`)\n| Variante | Parameter | ΔT Grenze 1 (K) | ΔT Grenze 2 (K) |\n|---|---|---|---|")
s.append("Spalte „Grenze 1“ = Parametergrenze mit erwartet kleinerem ΔT (R tief, h hoch, Stoffbänder hoch); „Grenze 2“ = die andere Grenze; LFP-Leitfähigkeit: Grenze 1 = Hauptfall W18, Grenze 2 = Schichtmischung.\n")
for v, lst in D["tornado"].items():
    for e in lst: s.append(f"| {v} | {e['parameter']} | {e['dT_tief_K']:.2f} | {e['dT_hoch_K']:.2f} |")
b = {n: F[n] for n in ("NMC_K1_L1_spalt", "NMC_K1_L2_spalt")}
s.append(f"\nZusatzfall NMC mit Luftspalt unter dem Kern (0,6 mm Luft zwischen Becherboden und Kern, Modellvariante, keine Messung): L1 T_max {b['NMC_K1_L1_spalt']['T_max_C']:.1f} °C, ΔT {b['NMC_K1_L1_spalt']['dT_kern_K']:.1f} K; L2 T_max {b['NMC_K1_L2_spalt']['T_max_C']:.1f} °C, ΔT {b['NMC_K1_L2_spalt']['dT_kern_K']:.1f} K (`NMC_K1_L1_spalt`, `NMC_K1_L2_spalt`).")
# Abgleich
L, N, N2 = "LFP_K1", "NMC_K1", "NMC_K2"
qL, qN = meta("LFP_K1_L1")["q_W_m3"], meta("NMC_K1_L1")["q_W_m3"]
mL = meta("LFP_K1_L1_mischung")["k_kern"]; mN = meta("NMC_K1_L1")["k_kern"]
def stat(x, lo, hi): return "innerhalb" if lo <= x <= hi else "außerhalb"
s.append(f"""
## Abgleich mit ERWARTUNG.md (Punkt für Punkt, keine Deutung)
1. **Wärme.** Erwartet LFP 1C ≈ 12,5 W, 2,1C ≈ 55 W; 4680 1C ≈ 3,5 W, 2,1C ≈ 15 W; je Volumen etwa doppelt so viel bei 4680. Gerechnet: LFP {g('LFP_K1_L1','Q_quelle_W'):.2f} W und {g('LFP_K1_L2','Q_quelle_W'):.2f} W; NMC {g('NMC_K1_L1','Q_quelle_W'):.2f} W und {g('NMC_K1_L2','Q_quelle_W'):.2f} W; Q/V NMC zu LFP = {qN/qL:.2f} ({qN:.0f} gegen {qL:.0f} W/m³). **Erfüllt** (innerhalb ±10 %).
2. **Leitfähigkeit.** Erwartet Mischung LFP Ebene ≈ 28, quer ≈ 1,0; 4680 axial ≈ 21, radial ≈ 1,2. Gerechnet (volumengewichtete Mischregel): LFP Ebene {mL[0]:.1f}, quer {mL[2]:.2f}; NMC axial/tangential {mN[0]:.1f}, radial {mN[2]:.2f} W/(m·K). **Erfüllt.** Hauptfall LFP mit W18 (21,04 / 19,82 / 4,11).
3. **L1.** Erwartet LFP ΔT ≈ 3–4 K, T_max ≈ 30 °C; 4680 ΔT ≈ 4–5 K, T_max ≈ 31 °C. Gerechnet: LFP ΔT Kern {g('LFP_K1_L1','dT_kern_K'):.2f} K ({stat(g('LFP_K1_L1','dT_kern_K'),3,4)} 3–4; als Gesamtzelle T_max − T_min {g('LFP_K1_L1','dT_gesamt_K'):.2f} K), T_max {g('LFP_K1_L1','T_max_C'):.1f} °C. NMC ΔT Kern {g('NMC_K1_L1','dT_kern_K'):.2f} K ({stat(g('NMC_K1_L1','dT_kern_K'),4,5)} 4–5), T_max {g('NMC_K1_L1','T_max_C'):.1f} °C (**{g('NMC_K1_L1','T_max_C')-31:+.1f} K gegenüber ≈ 31 °C**). Beide im Ziel (T ≤ {ZT:g} °C, ΔT ≤ {ZD:g} K).
4. **L2.** Erwartet LFP T_max ≈ 40–45 °C, ΔT ≈ 10–13 K; 4680 Boden T_max ≈ 45–50 °C, ΔT ≈ 15–18 K; ΔT-Vorgabe von beiden verfehlt, 4680 T_max knapp. Gerechnet: LFP T_max {g('LFP_K1_L2','T_max_C'):.1f} °C ({stat(g('LFP_K1_L2','T_max_C'),40,45)}), ΔT {g('LFP_K1_L2','dT_kern_K'):.1f} K ({stat(g('LFP_K1_L2','dT_kern_K'),10,13)}); NMC K1 T_max {g('NMC_K1_L2','T_max_C'):.1f} °C (**{stat(g('NMC_K1_L2','T_max_C'),45,50)} 45–50, {g('NMC_K1_L2','T_max_C')-50:+.1f} K über dem oberen Wert; Erwartung verfehlt**), ΔT {g('NMC_K1_L2','dT_kern_K'):.1f} K ({stat(g('NMC_K1_L2','dT_kern_K'),15,18)}). ΔT-Vorgabe {ZD:g} K: von beiden überschritten (Erwartung bestätigt). LFP-Wärmeabfuhr am Ende {g('LFP_K1_L2','Q_kuehlrand_W')/g('LFP_K1_L2','Q_quelle_W')*100:.0f} % der Quelle, also nicht nahezu stationär wie erwartet.
5. **K2.** Erwartet ΔT eher größer als bei Bodenkühlung, 20 K oder mehr. Gerechnet: L1 ΔT {g('NMC_K2_L1','dT_kern_K'):.2f} K (K1: {g('NMC_K1_L1','dT_kern_K'):.2f} K), T_max {g('NMC_K2_L1','T_max_C'):.1f} °C (K1: {g('NMC_K1_L1','T_max_C'):.1f}); L2 ΔT {g('NMC_K2_L2','dT_kern_K'):.1f} K (K1: {g('NMC_K1_L2','dT_kern_K'):.1f}), T_max {g('NMC_K2_L2','T_max_C'):.1f} °C (K1: {g('NMC_K1_L2','T_max_C'):.1f}). ΔT bei K2 ist etwas größer als bei K1, der Wert ≥ 20 K **wird nicht erreicht**; T_max ist bei K2 **niedriger** als bei K1.
6. **Stärkste Annahmen.** Empfindlichkeit L1: größte Wirkung auf ΔT durch den Innenwiderstand (LFP {D['tornado']['LFP'][0]['dT_tief_K']:.1f}…{D['tornado']['LFP'][0]['dT_hoch_K']:.1f} K, NMC {D['tornado']['NMC'][0]['dT_tief_K']:.1f}…{D['tornado']['NMC'][0]['dT_hoch_K']:.1f} K), dann h; die Leitfähigkeit wirkt bei NMC wenig. Der Luftspalt unter dem NMC-Kern (Modellvariante) verändert ΔT stärker als die Stoffbänder.
**„Verfehlt“-Kriterien der Erwartung:** Wärme L1 außerhalb ±10 %: nein. LFP L1 ΔT > 8 K oder < 1 K: nein ({g('LFP_K1_L1','dT_kern_K'):.2f} K). Energiebilanz stationär > 2 %: nein (größte Abweichung {max(abs(r['bilanz_abw_prozent']) for r in F.values() if 'bilanz_abw_prozent' in r):.4f} %). Transiente Energiebilanz (Quelle gegen Kühlrand plus gespeichert): größte Abweichung {max(abs(r['bilanz_transient_abw_prozent']) for r in F.values() if 'bilanz_transient_abw_prozent' in r):.3f} % (Elmer-Randlast gegen Trapezregel, nur Plausibilitätsprüfung).

## Methode und Modellvereinfachungen (bitte von Opus prüfen)
- **Geometrie.** LFP 681 × 90 × 14 mm, Boden = Schmalseite y = 0 (681 × 14 mm), Wand 0,3 mm Aluminium (237), Kern = Innenraum x 32,75…648,25 mm (Elektrodenlänge 615,5 mm, ENT-032), Endzonen je 32,75 mm Luft (0,026; symmetrisch aufgeteilt, Annahme). NMC Ø 46 × 80 mm, Becherwand/Boden/Deckel 0,4 mm Stahl (50), Kern Ringzylinder r 7…22,6 mm, z 0,4…76 mm, Kernloch und Raum oberhalb Luft.
- **NMC-Kern reicht bis auf den Becherboden** (Annahme dieser Auswertung: Tabless-Ableiter in Kontakt mit dem Boden; Parameterdatei nennt Kernbeginn bei z = 1,0 mm, dazwischen wäre sonst 0,6 mm Luft). Die Variante mit Luftspalt ist als Zusatzfall gerechnet (s. o.).
- **Orthotropie LFP:** Länge x = 21,04, Höhe y (Richtung zur Kühlplatte) = 19,82, Dicke z = 4,11 (W18; welche der beiden Ebenenwerte in welche Richtung gehört, ist aus W18 nicht eindeutig: Annahme). **NMC:** Wickel als Zylinderkoordinaten; je Sektor (48 Körper à 7,5°) ein konstanter, um den Mittelwinkel gedrehter 3×3-Tensor (axial = tangential, radial). Probe: Achsensymmetrie bei K1 – Streuung der Mantel-Temperatur am Umfang {F['NMC_K1_L1'].get('achsensymmetrie_streuung_K', float('nan')):.2g} K.
- **Wärmekapazität (L2):** Dichte und c nur im Kern; Dichte = Zellmasse (ENT-020 bzw. ENT-011) / Kernvolumen, c = 1112 bzw. 1100 J/(kg·K); Gehäuse und Luft ohne Wärmekapazität. Dichte und c des Gehäuses stehen nicht in `eingaben.json` (**offene Frage**).
- **Wärmequelle** Q = I²R gleichmäßig im Kern (Annahme laut Eingaben), R LFP = 1,0 mΩ · 135/92,4 (Regel R ∝ 1/Ah, Annahme), R NMC 6,5 mΩ. Kühlung: Randbedingung Wärmeübergang h = 500 W/(m²K) gegen 25 °C (Annahme); Rest adiabat. L2: BDF 2. Ordnung, Schritt 10 s, 120 Schritte, Start 25 °C; Last 2,1 C = 70 % Ladungsänderung in 1200 s.
- **Löser.** Stationär direkt (Umfpack), transient und NMC-Netzstufe 2 iterativ (BiCGStab, ILU2, Toleranz 1e-12). Bei den ersten beiden Läufen von NMC L2 wurde Umfpack nach ca. 12 Schritten wegen Dauer abgebrochen und neu mit dem iterativen Löser gerechnet; LFP L2 lief zuerst mit Umfpack, dann zur Konsistenz der VTU-Ausgabe (jeder Schritt) mit dem iterativen Löser neu.
- **Dateien:** Netz `elmer/netz_*`, Fälle `elmer/fall_*/{{case.sif,scalars.dat,meta.json,solver.log,case_t*.vtu}}`; Skripte `geometrie.py`, `rechnen.py`, `auswertung.py`, `bilder_render.py`, `render_blender.py`; Läufe `alle*.sh` (Scope `hermes-batterie-k0*`).

## Bilder (Lesehilfe: `k0_lesehilfe.md`, `bilder/render_lesehilfe.md`)
`temperatur_<LFP|NMC>_<K1|K2>_<L1|L2>.png` (Schnitt, 6 Stück), `temperatur3d_*_L2.png` (3 Stück, matplotlib), `verlauf_L2.png`, `empfindlichkeit_K0.png`; gerendert (Blender Workbench, CPU, da `pvbatch` ohne Python-Modul `paraview` nicht lauffähig ist; ParaView 5.11.2 ist installiert, aber nur die GUI/Binärdateien) in `bilder/render_<Fall>_t<0|300|600|900|1200>s.png` und `bilder/verlauf_<Fall>.mp4` (41 Bilder, 8 B/s, ffmpeg).

## Offene Fragen (→ Opus)
1. Dichte und Wärmekapazität des Gehäuses (Aluminium/Stahl) fehlen in `eingaben.json`; derzeit ohne Kapazität gerechnet.
2. Zuordnung der W18-Werte 21,04 / 19,82 zu Länge/Höhe der LFP-Zelle (hier Länge 21,04, Höhe 19,82).
3. NMC: Kontakt des Wickels zum Becherboden (hier ja) bzw. Luftspalt: Zusatzfall zeigt starken Einfluss.
4. Erwartung Punkt 4 (NMC L2 T_max 45–50 °C) und Punkt 5 (K2 ΔT ≥ 20 K) verfehlt.
5. Endzonen (Pole, Halter, Stromschienen) als reine Luft ist eine grobe Vereinfachung; Wärmeleitung über die Pole nicht berücksichtigt.
""" + fuss)
open(f"{H}/ERGEBNIS.md", "w").write("\n".join(s))
k = [f"K0 Ergebnis ({datum}, KI-generiert, Entwurf). Quelle sim/kuehlung/k0_zelle/ergebnis.json. Vorgabe REQ-P09: T_max <= {ZT:g} C, dT <= {ZD:g} K. Hauptfall K1 (Boden gekuehlt).",
     f"L1 (1C, stationaer): LFP T_max {g('LFP_K1_L1','T_max_C'):.1f} C, dT {g('LFP_K1_L1','dT_kern_K'):.1f} K; NMC T_max {g('NMC_K1_L1','T_max_C'):.1f} C, dT {g('NMC_K1_L1','dT_kern_K'):.1f} K; Bilanz < 0,001 %.",
     f"L2 (2,1C, 1200 s): LFP T_max {g('LFP_K1_L2','T_max_C'):.1f} C, dT {g('LFP_K1_L2','dT_kern_K'):.1f} K; NMC K1 {g('NMC_K1_L2','T_max_C'):.1f} C / {g('NMC_K1_L2','dT_kern_K'):.1f} K; NMC K2 {g('NMC_K2_L2','T_max_C'):.1f} C / {g('NMC_K2_L2','dT_kern_K'):.1f} K.",
     f"dT-Vorgabe {ZD:g} K bei L2 von allen verfehlt; T_max-Vorgabe {ZT:g} C nur von LFP eingehalten.",
     f"Netzstudie: max. Aenderung T_max {max(abs(r['diff_K']) for r in D['netzstudie'].values()):.3f} K (< 0,5 K).",
     "Verfehlte Erwartung: NMC L2 T_max (45-50 erwartet), K2 dT >= 20 K. Offen: Gehaeuse-Dichte/c, W18-Richtungszuordnung, NMC-Bodenkontakt/Spalt.",
     "Bilder: sim/kuehlung/k0_zelle/*.png, bilder/ (gerenderte Folge und MP4, Blender statt pvbatch)."]
open(f"{H}/ERGEBNIS_kurz.txt", "w").write("\n".join(k) + "\n")
# Folienbaustein
open(f"{R}/praesentation/bausteine/K0.md", "w").write(f"""> **KI-generiert** (Claude Sonnet, {datum}), Entwurf. Folienbaustein Vorgang K0 (Wärmesimulation Zelle).

# Zelltemperatur beim Schnellladen
**Kernaussage: Beim Schnellladen 10→80 % in 20 min bleibt die LFP-Zelle mit Bodenkühlung unter 45 °C ({g('LFP_K1_L2','T_max_C'):.1f} °C), die 4680-Zelle nicht ({g('NMC_K1_L2','T_max_C'):.1f} °C); die Spreizung {ZD:g} K halten beide nicht ein (LFP {g('LFP_K1_L2','dT_kern_K'):.1f} K, NMC {g('NMC_K1_L2','dT_kern_K'):.1f} K) (Opus).**

**Bild:** sim/kuehlung/k0_zelle/verlauf_L2.png (Vorgabe 45 °C und 5 K beschriftet, REQ-P09); gerendert sim/kuehlung/k0_zelle/bilder/render_LFP_K1_L2_t1200s.png und render_NMC_K1_L2_t1200s.png, Video bilder/verlauf_*.mp4

**Zahlen** (Quelle sim/kuehlung/k0_zelle/ergebnis.json):
- L1 (1C): LFP T_max {g('LFP_K1_L1','T_max_C'):.1f} °C, ΔT {g('LFP_K1_L1','dT_kern_K'):.1f} K; NMC {g('NMC_K1_L1','T_max_C'):.1f} °C, {g('NMC_K1_L1','dT_kern_K'):.1f} K
- L2: LFP {g('LFP_K1_L2','T_max_C'):.1f} °C / {g('LFP_K1_L2','dT_kern_K'):.1f} K; NMC K1 {g('NMC_K1_L2','T_max_C'):.1f} °C / {g('NMC_K1_L2','dT_kern_K'):.1f} K; NMC K2 (nur Vergleich) {g('NMC_K2_L2','T_max_C'):.1f} °C / {g('NMC_K2_L2','dT_kern_K'):.1f} K
- Annahmen: Innenwiderstand, h = 500 W/(m²K), 25 °C Kühlmittel; Entwurf, noch nicht von Opus geprüft

*KI-generiert, Entwurf.*
""")
# Lesehilfen
LH = [kopf("LH-K0", "Lesehilfe zu den K0-Bildern (Zellwärme)")]
txt = {"T": "Das Bild zeigt, wie warm die Zelle innen wird. Links ein Schnitt, rechts ein zweiter Schnitt quer dazu. Je heller (gelb), desto heißer, je dunkler (violett), desto kühler. Die Kühlung sitzt an der in der Achsenbeschriftung genannten Seite. Die türkise Linie (falls sichtbar) ist die Grenze {zt:g} °C; die Vorgabe der Spreizung ist {zd:g} K zwischen heißester und kühlster Stelle im Zellkern (Vorgabe REQ-P09). Die Zahlen im Titel stammen aus der Rechnung."}
for fall in ("LFP_K1_L1", "LFP_K1_L2", "NMC_K1_L1", "NMC_K1_L2", "NMC_K2_L1", "NMC_K2_L2"):
    last = "stationär bei Dauerladung 1C" if fall.endswith("L1") else "am Ende des Schnellladens (20 min, ca. 2,1C)"
    LH.append(f"**Lesehilfe zu `temperatur_{fall}.png`** Temperaturfeld der Zelle {fall.replace('_', ' ')} {last}. " + txt["T"].format(zt=ZT, zd=ZD) + "\n")
for fall in ("LFP_K1_L2", "NMC_K1_L2", "NMC_K2_L2"):
    LH.append(f"**Lesehilfe zu `temperatur3d_{fall}.png`** Dieselbe Zelle {fall.replace('_', ' ')} nach 20 min als aufgeschnittenes 3D-Bild (Gitterdarstellung, matplotlib). Farben wie oben: heller = heißer; die türkise Marke an der Farbskala zeigt {ZT:g} °C (Vorgabe).\n")
LH.append(f"**Lesehilfe zu `verlauf_L2.png`** Zeitlicher Verlauf beim Schnellladen. Durchgezogene Linien (linke Achse): heißeste Stelle der Zelle. Gestrichelt (rechte Achse): Temperaturunterschied im Zellkern. Die schwarze waagerechte Linie ist die Vorgabe {ZT:g} °C, die graue gepunktete die Vorgabe {ZD:g} K (REQ-P09). Wo eine Linie über ihrer Vorgabe liegt, ist sie überschritten.\n")
LH.append(f"**Lesehilfe zu `empfindlichkeit_K0.png`** Wie stark sich der Temperaturunterschied im Kern (ΔT, 1C-Dauerbetrieb, Bodenkühlung) ändert, wenn man genau eine unsichere Annahme innerhalb ihrer Spanne ändert. Je länger der Balken, desto wichtiger die Annahme. Die senkrechte schwarze Linie ist der Hauptfall, die graue gepunktete die Vorgabe {ZD:g} K. Der Luftspalt ist keine Messspanne, sondern eine Modellvariante.\n")
open(f"{H}/k0_lesehilfe.md", "w").write("\n".join(LH) + fuss)
B = [kopf("LH-K0B", "Lesehilfe zu den gerenderten K0-Bildern und Videos")]
for fall in ("LFP_K1_L2", "NMC_K1_L2", "NMC_K2_L2"):
    for t in (0, 300, 600, 900, 1200):
        B.append(f"**Lesehilfe zu `render_{fall}_t{t:04d}s.png`** Die Zelle {fall.replace('_', ' ')} nach {t} s ({t/60:.0f} min) Schnellladen, aufgeschnitten (" + ("bis zur halben Dicke; Dicke nur zur Darstellung 4-fach überhöht" if fall.startswith("LFP") else "ein Viertel weggeschnitten") + "), sodass man ins Innere sieht. Farbe = Temperatur: dunkel/violett kühl, gelb heiß; die türkise Marke an der Farbskala ist die Vorgabe {ZT:g} °C (REQ-P09). Alle Bilder derselben Zelle haben dieselbe Farbskala, damit man die Erwärmung über die Zeit vergleichen kann. Kühlung: ".format(ZT=ZT) + ("Kühlplatte unten" if "K1" in fall else "Kühlband am Mantel (nur Vergleich)") + ".\n")
B.append("Videos (MP4, 41 Bilder, 8 Bilder/s) mit derselben Darstellung: `verlauf_LFP_K1_L2.mp4`, `verlauf_NMC_K1_L2.mp4`, `verlauf_NMC_K2_L2.mp4`. Gerendert mit Blender (Workbench, CPU); Temperaturen aus den Elmer-Ergebnisdateien.\n")
open(f"{H}/bilder/render_lesehilfe.md", "w").write("\n".join(B) + fuss)
print("ok")
