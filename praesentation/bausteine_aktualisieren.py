#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Vorgang B5: aktualisiert Zahlenabschnitte der Folienbausteine
aus den Ergebnisdateien (Skript, nichts abgetippt). Der Abschnitt zwischen den Markern wird ersetzt, der Rest bleibt."""
import os, re, sys, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daten as D
from daten import f
A, Z = "<!-- AUTO-B5 Anfang -->", "<!-- AUTO-B5 Ende -->"
kopf = f"## Stand aus Ergebnisdateien (Skript praesentation/bausteine_aktualisieren.py, {datetime.date.today().isoformat()}, KI-generiert, Entwurf)\n"


def setze(name, text, neu_kopf=None):
    p = D.P("praesentation", "bausteine", name + ".md")
    block = f"{A}\n{kopf}{text.strip()}\n{Z}\n"
    if os.path.exists(p):
        s = open(p, encoding="utf-8").read()
        if A in s:
            s = re.sub(re.escape(A) + r".*?" + re.escape(Z) + r"\n?", lambda m: block, s, flags=re.S)
        else:
            s = s.rstrip() + "\n\n" + block
    else:
        s = (neu_kopf or "") + "\n" + block
    open(p, "w", encoding="utf-8").write(s)
    print("aktualisiert", name)


x3d, q = D.x3()
zeilen = ["| Fall | Pfahl-Eindringung max [mm] | Zellblock-Vorderseite dy max [mm] | Kraft max [kN] | Energiefehler max [%] |", "|---|---|---|---|---|"]
for k, v in x3d.items():
    ef = v.get("energiefehler_proz_max")
    zeilen.append(f"| {k} | {f(v['pfahl_eindringung_max_mm'])} | {f(v['zellblock_vorderseite_dy_max_mm'])} | {f(v['kraft_max_kN'], 0)} | {f(ef, 2) if ef is not None else '–'} |")
setze("X3", "Quelle: " + q + " (nur gültige Fälle mit pruef_modell_ok; Probelauf und ungültiger Erstlauf LFP_a_ungueltig_N3 ausgeschlossen).\n\n" + "\n".join(zeilen) +
      "\n\nLastfall b (Quetschung) nur bis 5 ms ausgewertet, danach instabil (Quelle LFP_b, Feld hinweis_instabil). Erwartungsvergleich offen (Opus).")

kl = D.kuehlung()
k5 = kl["k5"]
setze("K5_parallel",
      f"- Verteilung (Quelle {k5['quelle']}, gruppen.faelle.k2_d25_x3): max. Abweichung {f(k5['abw_x3'])} %, Δp {f(k5['dp_x3'], 3)} bar; bei einfachem Durchfluss (k2_d25_x1) {f(k5['dp_x1'], 3)} bar; Mäander nachgerechnet (einfacher Durchfluss) {f(k5['dp_maeander_x1'], 3)} bar.\n"
      f"- LFP V4p: T_max {f(kl['LFP']['T'], 2)} °C, Spreizung {f(kl['LFP']['dT'], 2)} K ({kl['LFP']['quelle']}); NMC V4p: {f(kl['NMC']['T'], 2)} °C, {f(kl['NMC']['dT'], 2)} K.\n"
      f"- Maßgeblich ist V4p wie gebaut. {f(kl['LFP_V4']['dT'], 1)} K (V4, {kl['LFP_V4']['quelle']}) gilt nur mit Gegenlauf, nicht im CAD (Verbesserungsvorschlag). Die Angabe 0,70 bar entfällt (in keiner Ergebnisdatei).")

p = D.pack()
L, N = p["LFP"], p["NMC"]
txt = ""
for v in (L, N):
    txt += (f"- {('LFP' if v is L else 'NMC')}: Teile {v['teile']}, Masse {f(v['masse'], 3)} kg, Länge {f(v['L'], 0)} mm, Breite {f(v['B'], 0)} mm, Höhe max {f(v['H'], 1)} mm, "
            f"Kollisionen {v['koll']}, Prüfmeldungen {v['pruefmeldungen']} ({v['q_cad']}); Kosten Pack-Teilsumme {f(v['kosten'], 0)} € ({v['q_kosten']}).\n")
setze("G5_9", txt)
setze("G5", txt + "- Zahlen nur aus ergebnis_LFP/NMC.json und Stückliste (daten.py); ältere Werte entfallen.")

rows, z, qv = D.v_modell()
tab = "| Bewertung | Anzahl |\n|---|---|\n" + "\n".join(f"| {k} | {v} |" for k, v in z.items())
setze("V_Modell", f"Quelle: {qv} (Zählung je Bewertung).\n\n{tab}\n\n**Bild:** Säulendiagramm auf Folie 10 (praesentation/unternehmenspraesentation.pptx), Zielzustand: nachgewiesen. Zielband nicht anwendbar (Zählung).",
      "# Folienbaustein V_Modell – Nachweisstand (KI-generiert, Entwurf)\n**Kernaussage:** Von den Anforderungen ist keine nachgewiesen; die meisten sind noch nicht prüfbar definiert (docs/06).")

# G5.md komplett aus Ergebnisdateien neu (keine alten Werte); K5-Kernaussage bereinigt
g5 = ("> **KI-generiert** (Claude Sonnet, 2026-11-23, Skript), Entwurf. Folienbaustein Vorgang G5 (Baukasten-Renders).\n\n# Das ganze Pack als parametrisches CAD, aus Stückliste und Akten montiert\n"
      f"**Kernaussage:** Das G5-Modell baut Zellen, Kühlplatte, Rahmen, Schaltbox und Kühlkreis aus der Stückliste zu einem Pack zusammen: LFP {f(L['L'], 0)} × {f(L['B'], 0)} × {f(L['H'], 0)} mm, NMC {f(N['L'], 0)} × {f(N['B'], 0)} × {f(N['H'], 0)} mm.\n\n"
      "**Bild:** cad/baukasten/bilder/g5_LFP_explosion.png (Konstruktionsansicht, kein Zielband; feste Breite 1430 mm beschriftet)\n\n**Zahlen**\n" + txt)
open(D.P("praesentation", "bausteine", "G5.md"), "w", encoding="utf-8").write(g5)
p = D.P("praesentation", "bausteine", "K5_parallel.md")
t = open(p, encoding="utf-8").read()
t = re.sub(r"\*\*Kernaussage:\*\*.*\n", lambda m: f"**Kernaussage:** Zwei parallele Gruppen aus je 4 Bahnen mit außenliegendem Verteilerrohr Ø 25 verteilen auf ±{f(k5['abw_x3'], 1)} % gleichmäßig bei {f(k5['dp_x3'], 2)} bar (dreifacher Durchfluss); die LFP-Zellspreizung beim Schnellladen beträgt wie gebaut (V4p) {f(kl['LFP']['dT'], 1)} K, NMC {f(kl['NMC']['dT'], 1)} K (Ziel 5 K). {f(kl['LFP_V4']['dT'], 1)} K gelten nur mit Gegenlauf, nicht im CAD (Verbesserungsvorschlag).\n", t, count=1)
open(p, "w", encoding="utf-8").write(t)
