#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Vorgang B5 (REQ-D14), Auftrag praesentation/AUFTRAG_B5.md.
Schreibt praesentation/unternehmenspraesentation.pptx (16:9, neutrale Vorlage, DE): 15 Folien + Anhang.
Jede Zahl kommt ueber daten.py aus einer Projektdatei. Quellpfade stehen in den Notizen jeder Folie.
Schalter --en ist nur vorgesehen (Englisch wird nicht erzeugt)."""
import sys, os, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import daten as D
from daten import f
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from PIL import Image

if "--en" in sys.argv:
    print("Englische Fassung ist nicht Teil von B5 (Auftrag Punkt 5). Abbruch.")
    sys.exit(2)

AUTOR = "Thomas Schmiegelt"
FUSS = "KI-generiert – freigegeben (Autor 2026-11-23) | " + AUTOR + " | "
DUNKEL = RGBColor(0x1F, 0x2A, 0x37)
AKZENT = RGBColor(0x1B, 0x6E, 0xA8)
GRAU = RGBColor(0x60, 0x66, 0x70)
HELL = RGBColor(0xEE, 0xF2, 0xF6)
ROT = RGBColor(0xB0, 0x2A, 0x2A)
GELB = RGBColor(0xFF, 0xF3, 0xC4)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
NR = [0]


def tb(slide, x, y, w, h, text="", size=14, bold=False, color=DUNKEL, align=PP_ALIGN.LEFT, fill=None, anchor=MSO_ANCHOR.TOP):
    s = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = s.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.08)
    tf.margin_top = tf.margin_bottom = Inches(0.04)
    if fill is not None:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    lines = text if isinstance(text, list) else [text]
    for i, l in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if isinstance(l, tuple):
            txt, sz, b = l
        else:
            txt, sz, b = l, size, bold
        p.alignment = align
        p.space_after = Pt(3)
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(sz)
        r.font.bold = b
        r.font.color.rgb = color
    return s


def folie(titel, kern, notizen, nr=None):
    s = prs.slides.add_slide(BLANK)
    NR[0] += 1
    nr = nr or str(NR[0])
    bar = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(0.12))
    bar.fill.solid(); bar.fill.fore_color.rgb = AKZENT; bar.line.fill.background()
    tb(s, 0.5, 0.25, 12.3, 0.7, titel, 28, True)
    if kern:
        tb(s, 0.5, 0.95, 12.3, 0.95, kern, 15, False, GRAU)
    tb(s, 0.5, 7.05, 10.5, 0.35, FUSS + nr, 10, False, GRAU)
    s.notes_slide.notes_text_frame.text = notizen
    s._nr = nr
    return s


def bild(s, rel, x, y, w, h, cap=None):
    p = D.P(rel)
    im = Image.open(p)
    iw, ih = im.size
    sc = min(w / iw, (h - (0.45 if cap else 0)) / ih)
    pw, ph = iw * sc, ih * sc
    s.shapes.add_picture(p, Inches(x + (w - pw) / 2), Inches(y), Inches(pw), Inches(ph))
    if cap:
        tb(s, x, y + ph + 0.02, w, 0.45, cap, 10, False, GRAU)


def tabelle(s, x, y, w, rows, colw, size=12, hdr=True, rowh=0.34):
    n, m = len(rows), len(rows[0])
    shp = s.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(rowh * n))
    t = shp.table
    tot = sum(colw)
    for j, cw in enumerate(colw):
        t.columns[j].width = Inches(w * cw / tot)
    for i, r in enumerate(rows):
        t.rows[i].height = Inches(rowh)
        for j, c in enumerate(r):
            cell = t.cell(i, j)
            cell.margin_left = cell.margin_right = Inches(0.06)
            cell.margin_top = cell.margin_bottom = Inches(0.02)
            cell.text = str(c)
            for p in cell.text_frame.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(size)
                    run.font.bold = (hdr and i == 0)
                    run.font.color.rgb = RGBColor(255, 255, 255) if (hdr and i == 0) else DUNKEL
            cell.fill.solid()
            cell.fill.fore_color.rgb = AKZENT if (hdr and i == 0) else (HELL if i % 2 == 0 else RGBColor(255, 255, 255))
    return shp


def ann(s, x, y, w, text, h=0.5):
    tb(s, x, y, w, h, text, 11, False, DUNKEL, fill=GELB)


datum = datetime.date.today().isoformat()
pk = D.pack()
kl = D.kuehlung()
vm_rows, vm_z, Q_VM = D.v_modell()
sw, Q_SW = D.startwerte()
areq, Q_AR = D.anforderungen()
lh, Q_LH = D.lastenheft_status()
el, Q_EL = D.elektrik()
ze = D.zelle()
x3d, Q_X3 = D.x3()
ris, Q_RIS = D.risiken()
pat, Q_PAT = D.patente()
ki, Q_KI = D.ki_einsatz()
nlic, Q_LIC = D.lizenzen()

# ---------------- 1 Titel ----------------
s = prs.slides.add_slide(BLANK)
NR[0] += 1
bg = s.shapes.add_shape(1, 0, 0, prs.slide_width, Inches(2.9)); bg.fill.solid(); bg.fill.fore_color.rgb = DUNKEL; bg.line.fill.background()
tb(s, 0.6, 0.6, 12, 1.0, "Batteriesystem BT-000: LFP- und NMC-Variante", 36, True, RGBColor(255, 255, 255))
tb(s, 0.6, 1.6, 12, 0.8, "Unternehmenspräsentation des Testprojekts „KI im Engineering“", 20, False, RGBColor(220, 228, 236))
tb(s, 0.6, 3.1, 7.2, 1.0, [("KI-generiert", 20, True), ("Alle Folien, Zahlen und Texte wurden von KI-Agenten aus den Projektdateien erzeugt. Vom Autor freigegeben am 2026-11-23.", 13, False)], fill=GELB, color=DUNKEL)
tb(s, 0.6, 4.3, 7.2, 0.5, "Vorgaben Vorschlag KI (Vorgabe B0 vom Autor nicht festgelegt)", 14, True, ROT)
tb(s, 0.6, 4.9, 7.2, 0.5, f"Autor: {AUTOR} | Stand: {datum}", 14)
tabelle(s, 8.2, 3.1, 4.6, [["Dokumentkopf", ""], ["Dok.-Nr.", "BAT-DOC-14"], ["Version", "0.1"], ["Status", "freigegeben (Autor 2026-11-23)"],
                           ["Ersteller", "Claude Sonnet (KI), im Auftrag von Claude Opus"], ["Prüfer", "– (Opus, Mensch offen)"]],
        [1, 2], 12, rowh=0.42)
tb(s, 0.5, 7.05, 10.5, 0.35, FUSS + "1", 10, False, GRAU)
s.notes_slide.notes_text_frame.text = (
    "Sprechertext: Dies ist die vom Autor freigegebene Unternehmenspräsentation. Sie wurde von KI-Agenten aus den Projektdateien erzeugt "
    "Die Vorgaben zu Zielgruppe, Länge und Vorlage hat der Autor nicht festgelegt, es gelten die Vorschläge der KI "
    "(praesentation/STORYBOARD.md, Abschnitt Vorgaben B0).\nQuellen: praesentation/STORYBOARD.md, praesentation/AUFTRAG_B5.md.")

# ---------------- 2 Aufgabe ----------------
a = sw["abgeleitet"]
s = folie("Aufgabe: ein Pkw-Batteriepack, zwei Zellvarianten",
          f"Startsatz: „{sw['satz']}“. Daraus leitet das Projekt als Vorschlag ab: {f(a['kWh_brutto'])} kWh brutto, {a['U_nenn_V']} V, "
          f"Ladeleistung bis {a['P_laden_spitze_kW']} kW (Annahmen). Die Vorgaben des Autors stehen unten.",
          "Sprechertext: Aufgabe ist ein komplettes Batteriepack für einen Pkw, gebaut in zwei Varianten: LFP (Eisenphosphat, robust, günstig) "
          "und NMC (Nickel-Mangan-Kobalt, dichter, schwerer zu kühlen). Startwerte sind Annahmen, bis der Autor sie festlegt.\n"
          f"Quellen: pm/startwerte.json (abgeleitet, annahmen), {Q_AR}, {Q_LH}. ENT: ENT-006 (800 V), ENT-013 (Länge), ENT-030 (Breite), ENT-005/007 (Zellen).", )
rows = [["REQ", "Anforderung", "Wert (Vorgabe Autor bzw. offen)"]]
for k in ["REQ-P01", "REQ-P02", "REQ-P03", "REQ-P05", "REQ-P07", "REQ-P09"]:
    r = lh[k]
    rows.append([k, r["text"], r["wert"]])
tabelle(s, 0.5, 2.0, 12.3, rows, [1, 3, 9], 11, rowh=0.52)
ann(s, 0.5, 5.9, 12.3, f"Startwerte sind Annahmen ({sw['hinweis']}). Zwei Zellvarianten gleicher Spezifikation: LFP-Blade und NMC-4680 (REQ-P06). Quelle: {Q_LH}, pm/startwerte.json.", 0.6)

# ---------------- 3 Kennzahlen ----------------
def ist(req):
    v = vm_rows[req]["ist"].replace("<br>", "; ")
    return v


p05 = vm_rows["REQ-P05"]
rows = [["Kennzahl", "Ziel", "Ist LFP / NMC", "Bewertung (docs/06)"],
        ["Energie brutto [kWh]", f"{f(a['kWh_brutto'])} (Vorschlag Startwerte)", f"{f(pk['LFP']['summen']['energie_kWh'], 2)} / {f(pk['NMC']['summen']['energie_kWh'], 2)}", vm_rows["REQ-P02"]["bewertung"]],
        ["Nennspannung [V]", f"{a['U_nenn_V']} (REQ-P03)", "kein Nachweis verknüpft", vm_rows["REQ-P03"]["bewertung"]],
        ["Dauer-/Spitzenleistung", "≥ 150 kW (10 s) / ≥ 60 kW (Annahme)", "kein Nachweis", vm_rows["REQ-P04"]["bewertung"]],
        ["Laden 10→80 % [min]", "LFP ≤ 20 / NMC ≤ 30", "kein Nachweis (blockiert)", p05["bewertung"]],
        ["Länge L [mm]", "≤ 1950", f"{f(pk['LFP']['L'], 0)} / {f(pk['NMC']['L'], 0)}", ("verfehlt" if max(pk["LFP"]["L"], pk["NMC"]["L"]) > 1950 else "eingehalten") + " (Grenze aus REQ-P07)"],
        ["Breite B [mm]", "≤ 1430", f"{f(pk['LFP']['B'], 0)} / {f(pk['NMC']['B'], 0)}", ("eingehalten" if max(pk["LFP"]["B"], pk["NMC"]["B"]) <= 1430 else "verfehlt") + " (Grenze aus REQ-P07)"],
        ["T_max Zelle [°C]", "≤ 45", f"{f(kl['LFP']['T'])} / {f(kl['NMC']['T'])}", ("unter Grenze" if max(kl["LFP"]["T"], kl["NMC"]["T"]) <= 45 else "über Grenze")],
        ["Spreizung [K]", "≤ 5", f"{f(kl['LFP']['dT'])} / {f(kl['NMC']['dT'])}", vm_rows["REQ-P09"]["bewertung"]],
        ["Masse Stückliste [kg]", "Obergrenze Startwert (REQ-P07)", f"{f(pk['LFP']['summen']['masse_stueckliste_kg'])} / {f(pk['NMC']['summen']['masse_stueckliste_kg'])}", "Teil von REQ-P07: " + vm_rows["REQ-P07"]["bewertung"]]]
s = folie("Kennzahlen auf einen Blick: Ziel und erreichter Stand",
          f"Von {vm_z['gesamt']} Anforderungen sind {vm_z['verfehlt']} verfehlt, {vm_z['nachgewiesen']} nachgewiesen, {vm_z['offen']} offen und {vm_z['blockiert']} blockiert (Kriterien teils Annahme, docs/19). "
          "Die Kennzahlen unten sind Rechenergebnisse, keine Messungen.",
          "Sprechertext: Die Tabelle stellt Ziel und Ist gegenüber. Wo kein Prüfmaß definiert ist, steht es so da. Länge und Spreizung verfehlen das Ziel; "
          "die Höchsttemperatur der Zellen liegt unter der Grenze. Die Zahlen sind gerechnet (nicht validiert).\n"
          f"Quellen: {Q_VM}; {Q_AR}; {pk['LFP']['q_sl']}, {pk['NMC']['q_sl']}; {pk['LFP']['q_cad']}, {pk['NMC']['q_cad']}; {kl['LFP']['quelle']}, {kl['NMC']['quelle']}; pm/startwerte.json.\n"
          "Offener Widerspruch (an Opus): Lastenheft L = 1950 mm (ENT-013), Bericht nennt L LFP 2030 mm (ENT-102), CAD liefert 2373/2273 mm (docs/06).")
tabelle(s, 0.5, 2.0, 12.3, rows, [3, 3.2, 3, 4], 11, rowh=0.42)
ann(s, 0.5, 6.35, 12.3, "Alle Werte aus Rechnung (Elmer, CAD, Stückliste), nicht gemessen. Ziel „Vorschlag“ = Annahme der KI. Bewertungsstufen: docs/17_workflow_schleife.md.", 0.5)

# ---------------- 4 Lösung ----------------
L, N = pk["LFP"], pk["NMC"]
s = folie("Lösung im Überblick: das ganze Pack als parametrisches CAD",
          f"Zellen, Kühlplatte, Rahmen, Schaltbox und Kühlkreis sind aus der Stückliste zu einem Pack zusammengebaut: "
          f"LFP {f(L['L'], 0)} × {f(L['B'], 0)} × {f(L['H'], 0)} mm, NMC {f(N['L'], 0)} × {f(N['B'], 0)} × {f(N['H'], 0)} mm, je {L['koll']} Kollisionen.",
          "Sprechertext: Das Pack wird nicht gezeichnet, sondern aus Akten und Stückliste automatisch aufgebaut. Links LFP, rechts NMC in Explosionsdarstellung. "
          "Die Breite 1430 mm ist durch die Fahrzeugbreite fest, die Länge wächst mit den Zellen. Es ist eine Konstruktionsansicht ohne Zielband.\n"
          f"Quellen: {L['q_cad']}, {N['q_cad']}; Bilder bericht/bilder/g5_LFP_explosion.png, g5_NMC_explosion.png (Quelle cad/baukasten/bilder/). ENT: ENT-030 (Breite), ENT-102, ENT-158, ENT-159.\n"
          "Hinweis: Baustein G5.md nennt ältere Zahlen (628,8 kg, 2335 mm); Folie liest die aktuelle Ergebnisdatei.")
bild(s, "bericht/bilder/g5_LFP_explosion.png", 0.4, 1.95, 4.6, 5.0, "LFP, Explosion. Konstruktionsansicht, kein Zielband; Breite 1430 mm fest.")
bild(s, "bericht/bilder/g5_NMC_explosion.png", 5.1, 1.95, 4.6, 5.0, "NMC, Explosion. Konstruktionsansicht, kein Zielband.")
tabelle(s, 9.85, 2.0, 3.1, [["", "LFP", "NMC"], ["Teile", L["teile"], N["teile"]], ["Masse CAD [kg]", f(L["masse"]), f(N["masse"])],
                            ["Kollisionen", L["koll"], N["koll"]], ["Zellen", L["summen"]["zellen"], N["summen"]["zellen"]]], [2, 1.2, 1.2], 11, rowh=0.4)
tb(s, 9.85, 4.2, 3.1, 1.5, f"Prüfmeldungen: LFP {L['pruefmeldungen']}, NMC {N['pruefmeldungen']} (Massenabweichungen u. a., siehe pruefung_<V>.txt, offen).", 11, False, GRAU)

# ---------------- 5 Zelle ----------------
r = ze["r10"]["p25"]
sch = ze["schnell"][1.5]
s = folie("Zelle: das Modell passt bei Raumtemperatur, bei Kälte nicht",
          f"Das an Messdaten kalibrierte Blade-Modell trifft den 10-s-Widerstand bei {f(r['T'], 0)} °C ({f(r['modell'] * 1, 2)} mΩ gegen {f(r['mess'], 2)} mΩ gemessen), "
          f"die 4680-Rundzelle erreicht 10→80 % in {f(sch['zeit_10_80_min'])} min bei 1,5C, dabei fällt das Anodenpotential auf {f(sch['phi_an_min_V'], 3)} V (Grenze 0 V, Lithium-Ablagerung).",
          "Sprechertext: Die Zelle wird in PyBaMM chemisch nachgerechnet und an Messdaten (Blade 135 Ah, CC-BY-Datensatz) abgeglichen. Bei 28 °C passt der Widerstand, bei Kälte nicht. "
          "Die 4680 schafft 30 min nur mit Lithium-Ablagerung an der Anode. Das ist ein Risiko (R-PLAT).\n"
          f"Quellen: {'; '.join(ze['q'])}. Bilder bericht/bilder/c2_blade_widerstand.png, c2_schnellladen_4680.png. ENT: ENT-005, ENT-007 bis ENT-011. "
          "Annahmen: Parametersätze Prada2013/Chen2020, Fitgrenzen von Sonnet (sim/chemie/c2_kalibrierung/ERGEBNIS.md).")
bild(s, "bericht/bilder/c2_blade_widerstand.png", 0.4, 2.0, 6.2, 3.2, "Widerstand Messung gegen Modell, Zielband ±15 mV im Bild beschriftet (zu prüfen).")
bild(s, "bericht/bilder/c2_schnellladen_4680.png", 6.7, 2.0, 6.2, 3.6, "Schnellladen 4680, Plating-Grenze und 30-min-Linie im Bild.")
rk = ze["r10"]["m10"]
tabelle(s, 0.5, 5.5, 6.0, [["10-s-Widerstand 50 % SOC", "gemessen [mΩ]", "Modell [mΩ]"],
                           [f"{f(ze['r10']['p25']['T'], 0)} °C", f(r["mess"], 3), f(r["modell"], 3)],
                           [f"{f(rk['T'], 0)} °C", f(rk["mess"], 3), f(rk["modell"], 3)]], [3, 2, 2], 11, rowh=0.38)
tb(s, 6.8, 5.7, 6.1, 1.2, f"4680 DCIR 25 °C: {f(ze['dcir']['n4680_25']['R10_mOhm'], 2)} mΩ (R10). Wärme bei 1,5C: {f(sch['waerme_mittel_gesamt_W'], 2)} W (gesamt), {f(sch['waerme_mittel_IdU_W'], 2)} W (I·ΔU). Modellwerte, Entwurf, nicht von Opus geprüft.", 11, False, GRAU)

# ---------------- 6 Pack und Struktur ----------------
s = folie("Pack und Struktur: Cell-to-Pack in festem Bauraum",
          f"Die Zellen liegen ohne Modulgehäuse direkt im Pack. Die Breite {f(L['B'], 0)} mm ist durch das Fahrzeug fest. Stückliste: LFP {f(L['summen']['masse_stueckliste_kg'])} kg, NMC {f(N['summen']['masse_stueckliste_kg'])} kg.",
          "Sprechertext: Cell-to-Pack heißt, dass die Zellen ohne Zwischengehäuse (Modul) direkt im Pack sitzen. Das spart Masse und Platz. Der Bauraum ist in der Breite fest. "
          "Die Länge der gerechneten Packs liegt über der Vorgabe 1950 mm. Die Bilder zeigen den Massenvergleich mit Zielband (früherer Stand SL2/E2D); die Tabelle enthält den aktuellen Stand.\n"
          f"Quellen: {L['q_sl']}, {N['q_sl']}, {L['q_cad']}, {N['q_cad']}; Bilder docs/bilder/stueckliste_massen_LFP.png, _NMC.png (Stand SL2). ENT: ENT-030, ENT-096 bis ENT-103.")
bild(s, "docs/bilder/stueckliste_massen_LFP.png", 0.4, 2.0, 4.4, 3.2, "LFP-Masse mit Zielband 560–620 kg im Bild (Stand SL2/E2D).")
bild(s, "docs/bilder/stueckliste_massen_NMC.png", 4.9, 2.0, 4.4, 3.2, "NMC-Masse mit Zielband 390–430 kg im Bild (Stand SL2/E2D).")
bm = L["sl"]["masse_je_baugruppe_kg"]
tabelle(s, 9.5, 2.0, 3.5, [["Kenngröße", "LFP", "NMC"], ["Masse Stückliste [kg]", f(L["summen"]["masse_stueckliste_kg"]), f(N["summen"]["masse_stueckliste_kg"])],
                           ["Masse CAD [kg]", f(L["masse"]), f(N["masse"])], ["Länge [mm]", f(L["L"], 0), f(N["L"], 0)],
                           ["Breite [mm]", f(L["B"], 0), f(N["B"], 0)], ["Höhe max [mm]", f(L["H"], 0), f(N["H"], 0)]], [2.3, 1.1, 1.1], 11, rowh=0.4)
ann(s, 0.5, 5.7, 12.3, "Länge: Vorgabe 1950 mm (ENT-013), gerechnet über der Vorgabe (siehe Folie 3, docs/06). Bilder zeigen den früheren Stand E2D, die Tabelle den aktuellen CAD-Stand.", 0.6)

# ---------------- 7 Elektrik ----------------
eL, eN = el["LFP"], el["NMC"]
s = folie("Elektrik: der Strom bestimmt den Querschnitt",
          f"LFP kommt mit {f(eL['masse_kg'])} kg Verbindern und {f(eL['verlust_W'], 0)} W Verlust aus, NMC braucht {f(eN['masse_kg'])} kg und verliert {f(eN['verlust_W'], 0)} W "
          f"(über der 300-W-Grenze: {'ja' if el['verfehlt'] else 'nein'}).",
          "Sprechertext: Dicke und Material der Stromschienen folgen aus dem Strom. LFP führt wenige hundert Ampere in wenigen Verbindern, NMC viele kleine Zellabgriffe. "
          "Die NMC-Variante verliert mehr Leistung als die gesetzte Grenze. Der Verlustwert ist eine Annahme-Grenze (ERWARTUNG).\n"
          f"Quellen: {Q_EL} (maßgeblich, E1 mit G5-Längen); früherer Stand sim/elektrik/e1_querschnitte/ergebnis.json: LFP {f(el['alt']['LFP_summe']['verlust_W'])} W, NMC {f(el['alt']['NMC_summe']['verlust_W'])} W; Bilder sim/elektrik/e1_querschnitte/querschnitte_g5.png, verluste_g5.png. ENT: ENT-147, ENT-150, ENT-146 (Schaltbox, E2). "
          "Hinweis: Baustein E2 nennt spätere Verlustwerte (Al-Verbinder LFP 75,6 W, NMC 316 W bis 461 W, sim/elektrik/e2_elektronik/verlust_al_e2d.json), das Entscheidungsthema ist offen (an Opus).")
bild(s, "sim/elektrik/e1_querschnitte/querschnitte_g5.png", 0.4, 2.0, 6.3, 3.4, "Querschnitte E1 mit G5-Längen, Zielband je Art im Bild.")
bild(s, "sim/elektrik/e1_querschnitte/verluste_g5.png", 6.8, 2.0, 6.3, 3.4, "Verluste E1 mit G5-Längen, Zielband < 100 W und Grenze 300 W im Bild.")
tabelle(s, 0.5, 5.6, 8.5, [["", "LFP", "NMC"], ["Verlust gesamt [W]", f(eL["verlust_W"]), f(eN["verlust_W"])],
                           ["Spannungsabfall [% Nenn]", f(eL["spannungsabfall_prozent_Nenn"], 3), f(eN["spannungsabfall_prozent_Nenn"], 3)]], [3, 2, 2], 11, rowh=0.38)
tb(s, 9.3, 5.6, 3.7, 1.3, "Schutzkonzept und BMS-Umfang: Anforderung REQ-P15 offen (Umfang vom Autor festzulegen).", 11, False, GRAU)

# ---------------- 8 Kühlung ----------------
k5 = kl["k5"]
s = folie("Kühlung beim Schnellladen: die Spreizung im LFP ist zu groß",
          f"Beim Schnellladen erreicht der LFP-Zellblock {f(kl['LFP']['T'])} °C (Grenze 45 °C), die Temperaturspreizung beträgt aber {f(kl['LFP']['dT'])} K (Ziel 5 K, verfehlt). "
          f"NMC: {f(kl['NMC']['T'])} °C und {f(kl['NMC']['dT'])} K ({"Ziel erreicht" if kl["NMC"]["dT"] <= 5 else "Ziel verfehlt"}).",
          "Sprechertext: Das Pack wird beim Schnellladen heiß. Die Kühlplatte hält die Höchsttemperatur unter 45 °C. Die Unterschiede zwischen den Zellen (Spreizung) sind beim LFP über dem Ziel von 5 K. "
          "Die Verteilung auf zwei parallele Gruppen mit außenliegendem Verteilerrohr hält die Durchflussabweichung unter 3 %.\n"
          f"Quellen: {kl['LFP']['quelle']}, {kl['NMC']['quelle']}, {k5['quelle']}; Bild sim/kuehlung/k5_parallel/k4_vergleich_V0_V3_V4_V4p.png. ENT: ENT-152 bis ENT-159. "
          f"Maßgeblich ist V4p wie gebaut (Opus). 7,6 K (V4, {kl['LFP_V4']['quelle']}: {f(kl['LFP_V4']['dT'])} K) gilt nur mit Gegenlauf, nicht im CAD (Verbesserungsvorschlag).")
bild(s, "sim/kuehlung/k5_parallel/k4_vergleich_V0_V3_V4_V4p.png", 0.4, 2.0, 7.4, 3.6, "Spreizung (Ziellinie 5 K im Bild) und Höchsttemperatur je Kühlvariante; Grenze 45 °C nur im Text.")
tabelle(s, 8.0, 2.0, 5.0, [["", "LFP", "NMC"], ["T_max Zellblock [°C]", f(kl["LFP"]["T"]), f(kl["NMC"]["T"])], ["Spreizung [K]", f(kl["LFP"]["dT"]), f(kl["NMC"]["dT"])],
                           ["Grenze T_max / Spreizung", "45 °C / 5 K", "45 °C / 5 K"]], [3, 1.5, 1.5], 11, rowh=0.4)
tb(s, 8.0, 3.8, 5.0, 1.9, [f"Verteilung: Abweichung zwischen den Bahnen {f(k5['abw_x3'])} % (dreifacher Durchfluss).",
                           f"Druckverlust: {f(k5['dp_x3'], 2)} bar (parallele Gruppen, dreifacher Durchfluss) gegenüber {f(k5['dp_maeander_x1'], 2)} bar (Mäander, einfacher Durchfluss)."], 12)
ann(s, 0.5, 5.9, 12.3, "Zellblock-Werte aus Elmer-Rechnung (Variante V4p), Definition der Spreizung offen (bericht.tex Kap. K3/K4). Modellrechnung, nicht validiert.", 0.5)

# ---------------- 9 Sicherheit (X3) ----------------
xa, xa2, xb = x3d["LFP_a"], x3d["LFP_a2"], x3d["LFP_b"]
s = folie("Sicherheit: Seitenpfahl-Crash und Quetschung am ganzen Pack",
          f"Beim Pfahlaufprall (5 kJ) dringt der Pfahl {f(xa['pfahl_eindringung_max_mm'])} mm ein, die erste Zellreihe wird {f(xa['zellblock_vorderseite_dy_max_mm'])} mm verschoben "
          f"(Energiefehler {f(xa['energiefehler_proz_max'], 2)} %). Bei 20 kJ sind es {f(xa2['pfahl_eindringung_max_mm'])} mm.",
          "Sprechertext: Das ganze Pack (Rahmen, Zellen, Kühlplatten) wird explizit auf Crash gerechnet. Lastfall a ist ein Pfahl mit 5 kJ, a2 mit 20 kJ, Lastfall b eine Quetschung mit einer Platte. "
          "Die Quetschung wurde nur bis 5 ms ausgewertet, danach wurde das Modell instabil. Die Ergebnisse sind Entwurf; die Erwartungswerte sind noch nicht von Opus verglichen. "
          "Der erste Dauerlauf (LFP_a) war wegen eines Modellfehlers ungültig und wird nicht verwendet.\n"
          f"Quellen: {Q_X3} (Schlüssel LFP_a, LFP_a2, LFP_b, NMC_a, NMC_b); Bilder sim/mechanik/x3_crash_g5/kraft_weg_LFP_a.png, verformung_LFP_a.png. "
          "Annahmen: Platzhalter-Zellwerkstoff (E 1 GPa, Fließgrenze 20 MPa), Pfahl- und Plattengröße (sim/mechanik/x3_crash_g5/ERGEBNIS.md, offene Fragen). "
          "X1/X2 (Rahmen quasistatisch, Knautschzone) stehen im Anhang A2.")
bild(s, "sim/mechanik/x3_crash_g5/kraft_weg_LFP_a.png", 0.4, 2.0, 4.6, 3.7, "Kraft über Weg, LFP, Lastfall a; grünes Band = Erwartung im Bild. Erwartung von Opus verfehlt: Rahmen steifer als geschätzt (B-BAT-042) – Deutung Opus.")
bild(s, "sim/mechanik/x3_crash_g5/verformung_LFP_a.png", 5.1, 2.0, 4.0, 3.7, "Verformung LFP, Lastfall a.")
def zeile(name, v, bis=False):
    return [name, f(v["pfahl_eindringung_max_mm"]), f(v["zellblock_vorderseite_dy_max_mm"]), f(v["kraft_max_kN"], 0)]
tabelle(s, 9.2, 2.0, 3.9, [["Fall", "Pfahl [mm]", "Zellblock [mm]", "Kraft max [kN]"], zeile("LFP a 5 kJ", xa), zeile("LFP a2 20 kJ", xa2), zeile("NMC a 5 kJ", x3d["NMC_a"]),
                           zeile("LFP b (≤ 5 ms)", xb), zeile("NMC b (≤ 5 ms)", x3d["NMC_b"])], [2.3, 1.3, 1.5, 1.4], 10, rowh=0.45)
ann(s, 0.5, 5.9, 12.3, "Quetschung (b) nur bis 5 ms ausgewertet (danach instabil). Erwartungsvergleich offen (Opus). Ungültiger Erstlauf nicht verwendet.", 0.55)

# ---------------- 10 Nachweisstand ----------------
s = folie("Nachweisstand: was ist belegt, was fehlt",
          f"Von {vm_z['gesamt']} Anforderungen sind {vm_z['nachgewiesen']} nachgewiesen, {vm_z['verfehlt']} verfehlt, {vm_z['offen']} offen und {vm_z['blockiert']} blockiert; nur {vm_z['autor_gesamt']} haben ausschließlich Kriterien des Autors.",
          "Sprechertext: Jede Anforderung hat jetzt ein prüfbares Kriterium. Viele Kriterien sind aber Vorschläge der KI und warten auf die Bestätigung des Autors; solche Bewertungen tragen den Zusatz „Kriterium Annahme, Autor offen“. Offen heißt: es gibt noch keine Rechnung dazu. "
          "Bei Methode S (Simulation) ist die höchste Stufe „rechnerisch erfüllt (nicht validiert)“.\n"
          f"Quellen: {Q_VM}, pm/anforderungen.json, docs/17_workflow_schleife.md.")
cd = CategoryChartData()
reihe = ["nachgewiesen", "rechnerisch erfüllt (nicht validiert)", "verfehlt", "offen", "blockiert"]
cd.categories = ["nachgewiesen", "rechn. erfüllt", "verfehlt", "offen", "blockiert"]
cd.add_series("Anzahl", [vm_z[k] for k in reihe])
ch = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(0.5), Inches(2.0), Inches(7.6), Inches(4.3), cd).chart
ch.has_legend = False
ch.plots[0].has_data_labels = True
ch.plots[0].data_labels.font.size = Pt(14)
ch.plots[0].data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
ch.category_axis.tick_labels.font.size = Pt(11)
ch.value_axis.tick_labels.font.size = Pt(11)
ch.has_title = True
ch.chart_title.text_frame.text = f"Anforderungen nach Bewertung (gesamt {vm_z['gesamt']})"
ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(14)
rows = [["Bewertung", "Anzahl"]] + [[k, vm_z[k]] for k in reihe] + [["gesamt", vm_z["gesamt"]]]
tabelle(s, 8.4, 2.0, 4.6, rows, [4, 1], 12, rowh=0.4)
ann(s, 8.4, 5.3, 4.6, "Ziel der Kategorien: docs/17 (Bewertungsstufen). Tabelle und Diagramm aus docs/06, keine Handzählung.", 0.8)
tb(s, 0.5, 6.4, 12.3, 0.5, "Zielband im Diagramm: nicht anwendbar (Zählung). Zielzustand wäre „nachgewiesen“ oder „rechnerisch erfüllt“ je Anforderung.", 11, False, GRAU)

# ---------------- 11 Risiken ----------------
rows = [["Nr", "Risiko", "Folge", "Maßnahme", "B/A/E"]]
for r_ in ris[:5]:
    rows.append([r_["nr"], r_["fehler"], r_["folge"], r_["massnahme"], "/".join(r_["bew"]) if "–" not in r_["bew"] else "nicht bewertet (FMEA offen)"])
s = folie("Risiken: die fünf größten, mit Maßnahme",
          f"Die fünf im Risikoregister geführten Produktrisiken. Eine Bewertung nach Bedeutung, Auftreten und Entdeckung liegt nur für {sum(1 for r_ in ris[:5] if chr(8211) not in r_['bew'])} vor; die übrigen sind unbewertet (Entwurf).",
          "Sprechertext: Das sind die geführten Produktrisiken: thermisches Durchgehen, ungleiche Kühlung, überhitzte Verbinder und zwei Risiken der 4680-Zelle beim Schnellladen. "
          "Bewertungen (B/A/E) sind nur teilweise eingetragen; die Rangfolge der KI ist ausdrücklich keine Bewertung.\n"
          f"Quelle: {Q_RIS}; Befunde B-BAT-023 (4680). Die Auswahl „fünf größte“ ist die Zahl der geführten Produktrisiken, nicht eine Rangfolge nach RPZ (RPZ offen).")
tabelle(s, 0.5, 2.0, 12.3, rows, [1, 3.2, 2.2, 5, 1.5], 10.5, rowh=0.7)
ann(s, 0.5, 6.35, 12.3, "RPZ-Rangfolge nicht möglich: B/A/E bei drei Risiken nicht ausgefüllt (docs/05). Prozessrisiken der KI: RIS-K01 bis K05.", 0.5)

# ---------------- 12 Stückliste und Kostentreiber ----------------
def kurz(t, n):
    return t if len(t) <= n else t[:n].rsplit(' ', 1)[0] + ' …'


def top(v, n=6):
    ps = [p for p in v["positionen"] if isinstance(p.get("masse_ges_kg"), (int, float)) and p["masse_ges_kg"]]
    ps.sort(key=lambda p: -p["masse_ges_kg"])
    return ps[:n]
rows = [["Pos", "Benennung (LFP)", "Masse [kg]", "Menge"]]
for p in top(L):
    rows.append([p["pos"], kurz(p["benennung"], 46), f(p["masse_ges_kg"]), p["menge_LFP"]])
s = folie("Stückliste und Kostentreiber: die Zelle dominiert",
          f"Pack-Teilsumme mit Annahmepreisen: LFP {f(L['kosten_kwh'])} €/kWh, NMC {f(N['kosten_kwh'])} €/kWh; die Zelle ist mit {f(L['zelle_eur'] / L['kosten'] * 100, 0)} % (LFP) bzw. {f(N['zelle_eur'] / N['kosten'] * 100, 0)} % (NMC) der größte Posten. "
          "Offene Positionen machen die Werte zu Untergrenzen.",
          "Sprechertext: Die Stückliste hat je Variante 56 Positionen. Die Zelle trägt den größten Teil von Masse und Kosten. Die Preise sind Annahmen (Schätzungen), nur der Zellpreis hat einen Beleg (97 USD/kWh BEV-Pack 2024, W29). "
          "Ein Zielwert für die Kosten ist offen (REQ-P16).\n"
          f"Quellen: {L['q_sl']}, {N['q_sl']}, {L['q_kosten']}, {N['q_kosten']}; Bild pm/kosten/kosten_vergleich.png. ENT: ENT-096 bis ENT-103, Annahme ERW-KO1 (Opus).")
tabelle(s, 0.5, 2.0, 6.2, rows, [1, 5, 1.4, 1], 10.5, rowh=0.38)
tabelle(s, 0.5, 4.8, 6.2, [["", "LFP", "NMC"], ["Pack-Teilsumme [€]", f(L["kosten"], 0), f(N["kosten"], 0)], ["je kWh [€/kWh]", f(L["kosten_kwh"]), f(N["kosten_kwh"])],
                           ["Offene Positionen", L["offen"], N["offen"]], ["Positionen gesamt", L["sl"]["positionen_gesamt"], N["sl"]["positionen_gesamt"]]], [3, 1.3, 1.3], 10.5, rowh=0.36)
bild(s, "pm/kosten/kosten_vergleich.png", 7.0, 2.0, 6.0, 4.4, "Kostenvergleich, Zielband ERW-KO1 und Beleg W29 im Bild beschriftet.")
ann(s, 7.0, 6.4, 6.0, f"{f(L['anteil_schaetzung'], 1)} % der Kostensumme (LFP) beruhen auf geschätzten Preisen (Quelle {L['q_kosten']}, Feld anteil_schaetzung_an_summe_pct). Ziel für Kosten: keines (REQ-P16).", 0.5)

# ---------------- 13 Schutzrechtslage ----------------
s = folie("Schutzrechtslage: Stand der Technik, ohne rechtliche Bewertung",
          f"Die Recherche in {pat['themen']} Themen fand {pat['n']} Patentschriften, davon {pat['ohne_anspruch']} ohne abgerufenen Anspruchstext. "
          "Die KI macht keine Aussage zu Verletzung oder Handlungsfreiheit (REQ-D08).",
          "Sprechertext: Patente wurden nur als Stand der Technik gesammelt. Ob das Pack Schutzrechte verletzt, kann nur eine Fachperson (Freedom to Operate) beurteilen. "
          "Ein Teil der Schriften war nicht abrufbar; deren Aussagen sind nicht geprüft.\n"
          f"Quelle: {Q_PAT} (PI-Ergebnis, Zitate automatisch geprüft); Regel AGENTS.md (keine FTO-Aussage). Lizenz/Quellen docs/10.")
tabelle(s, 0.5, 2.1, 6.5, [["Kenngröße", "Wert"], ["Recherchethemen", pat["themen"]], ["Patentschriften (verschiedene Nummern)", pat["n"]],
                           ["davon ohne abgerufenen Anspruch", pat["ohne_anspruch"]], ["verschiedene Anmelder", len(pat["inhaber"])]], [4, 1.5], 12, rowh=0.5)
tb(s, 7.3, 2.1, 5.6, 3.0, [("Hinweis für Entscheider", 14, True), "Die Liste ist eine Sammlung, keine Prüfung. Sie ersetzt keine Recherche durch Patentanwälte.",
                           "Ungeprüft durch den Menschen (PI-Ergebnis, Stand dieses Entwurfs)."], 12)
ann(s, 0.5, 5.2, 12.3, "Keine rechtliche Bewertung (REQ-D08). Bild: keines nötig, Zielband nicht anwendbar.", 0.5)

# ---------------- 14 Arbeitsweise mit KI ----------------
s = folie("Arbeitsweise mit KI: Verteilung, Prüfung, gefundene Fehler",
          f"Das Einsatzprotokoll enthält {ki['zeilen']} Einträge, das Befundregister {ki['befunde']} Befunde. Opus leitet und prüft, Sonnet setzt um, Haiku erledigt Mechanisches, PI (lokal) recherchiert, der Mensch gibt frei.",
          "Sprechertext: Die Arbeit ist verteilt: Das stärkste Modell (Opus) legt Anforderungen und Erwartungen fest und prüft an den Rohdaten; Sonnet und Haiku erledigen den Fleiß; ein lokales Modell (PI) recherchiert ohne Werkzeuge. "
          "Gefunden wurden Fehler durch Erwartung vor der Rechnung, Kollisionsprüfung, Gegenprüfung und den Menschen. Beispiele: Zwischenlage 41,5 kg statt erwartet (B-BAT-035), Kühlplatte 75,5 statt 46,9 kg (B-BAT-033), ungültiger Crash-Erstlauf (X3 Nachtrag 3).\n"
          f"Quellen: {Q_KI}; praesentation/bausteine/KI_Integration.md; cad/baukasten/ausgabe/pruefung_LFP.txt. Die Zählung je Agent ist heuristisch nach Agentenspalte. Werkzeug- und Modellnamen: PyBaMM, Elmer, FluidX3D, FreeCAD, OpenCourant (SOFTWARE.md).")
je = ki["je"]
tabelle(s, 0.5, 2.1, 5.2, [["Akteur (Spalte Agent)", "Einträge"], ["Sonnet", je.get("Sonnet", 0)], ["PI (lokal)", je.get("PI", 0)], ["Opus", je.get("Opus", 0)],
                           ["Haiku", je.get("Haiku", 0)], ["Einträge gesamt", ki["zeilen"]]], [3, 1.3], 12, rowh=0.45)
tb(s, 6.0, 2.1, 7.0, 3.6, [("Was gefunden wurde (Beispiele aus den Befunden)", 14, True),
                           "• Zwischenlage mit 41,5 kg und 249 € statt erwartet (B-BAT-035)",
                           "• Kühlplatte 75,5 statt 46,9 kg (B-BAT-033)",
                           "• Ungültiger erster Crash-Dauerlauf, Zellreihen glitten frei (X3, Nachtrag 3)",
                           "• Beide Packs zuletzt kollisionsfrei, nach vielen Fehlerrunden (KI_Integration)",
                           "Gefunden durch: Erwartung vor der Rechnung, Kollisionsprüfung, Gegenprüfung, Mensch.",
                           "Werkzeuge: PyBaMM, Elmer, FluidX3D, FreeCAD, OpenCourant."], 12)
ann(s, 0.5, 5.9, 12.3, "Zählung je Akteur heuristisch aus der Agentenspalte von docs/08. Zielband nicht anwendbar (kein Diagramm).", 0.5)

# ---------------- 15 Nächste Schritte ----------------
offen = [(k, v["text"]) for k, v in lh.items() if v["status"].strip().lower() == "offen"]
rows = [["REQ", "Entscheidungsbedarf (Lastenheft-Status „offen“)"]] + [[k, t] for k, t in offen]
s = folie("Nächste Schritte: Entscheidungsbedarf",
          f"{vm_z['gesamt'] - vm_z['autor_gesamt']} von {vm_z['gesamt']} Anforderungen hängen an Kriterien, die die KI vorgeschlagen hat und der Autor bestätigen muss (docs/19). "
          "Aufwand: nicht erfasst (Vorgang B4 offen), nichts geschätzt.",
          "Sprechertext: Der nächste Schritt ist die Bestätigung der vorgeschlagenen Kriterien durch den Autor (Freigaberunde) und danach die Rechnungen für die offenen Anforderungen. "
          "Danach können Nachweise geführt werden. Aufwand und Zeit sind noch nicht geplant (B4); die Folie nennt dazu keine Zahl.\n"
          f"Quellen: {Q_LH} (Status offen), {Q_VM}, PLAN.md, pm/plan/kritischer_pfad.txt. Offener Widerspruch an Opus: Länge L (1950 / 2030 / 2373 mm, docs/06, B-BAT-045).")
tabelle(s, 0.5, 2.1, 7.4, rows, [1, 6], 12, rowh=0.4)
tb(s, 8.2, 2.1, 4.8, 3.5, [("Weitere offene Punkte", 14, True), "• Länge des Packs: Vorgabe 1950 mm, gerechnet 2373 / 2273 mm (docs/06)",
                           "• Zielwert Kosten (REQ-P16) offen",
                           "• Vorgaben zur Präsentation (B0) offen",
                           "• Freigabe aller Entwürfe nur durch den Menschen",
                           "• Aufwand: nicht erfasst"], 12)
ann(s, 0.5, 6.3, 12.3, "Keine Aufwandsschätzung ohne Quelle. Bild: keines, Zielband nicht anwendbar.", 0.5)

# ---------------- Anhang A1 ----------------
s = folie("Anhang A1: Annahmen, Quellen und Lizenzen",
          f"Das Lizenz- und Quellenverzeichnis führt {nlic} Einträge. Fremde Inhalte liegen nicht im Repo. Alle Preis-, Masse- und Grenzwerte ohne Beleg sind als Annahme gekennzeichnet.",
          "Sprechertext: Quellen und Lizenzen sind in einem Verzeichnis erfasst. Neu ist python-pptx (MIT) für diese Präsentation.\n"
          f"Quelle: {Q_LIC}; startwerte annahmen in pm/startwerte.json.")
ann_rows = [["Annahme (Startwerte)", "Wert"]] + [[k, str(v)] for k, v in list(sw["annahmen"].items())[:8]]
tabelle(s, 0.5, 2.1, 7.0, ann_rows, [4, 3], 11, rowh=0.38)
tb(s, 7.8, 2.1, 5.2, 3.5, [("Quellen und Lizenzen", 14, True), f"{nlic} Einträge in docs/10_lizenzen_und_quellen.md.", "Neu: python-pptx 1.0.2 (MIT) für diese Folien.", "Keine fremden Texte im Repo; Patente und Normen nur als Quellenhinweis."], 12)
ann(s, 0.5, 5.8, 12.3, "Quelle der Annahmen: pm/startwerte.json (alle Faktoren Annahmen bis Recherche-Bestätigung).", 0.5)

# ---------------- Anhang A2: X1/X2 ----------------
x1d, x1b, Q_X1 = D.x1()
s = folie("Anhang A2: Rahmen und Knautschzone (Crash X1, X1b)",
          f"Eine 20 mm breite Knautschzone hält die Kraft (mittel {f(x1b['kraft_mittel_bis_w_kN'])} kN), nimmt aber beim 5-kJ-Pfahlaufprall die Energie nicht auf, bevor die Zelle berührt wird "
          f"(Eindringung max. {f(x1b['eindringung_max_mm'])} mm, Energiefehler {f(x1b['energiefehler_proz_max'], 4)} %). Zwischenstand, Entwurf.",
          "Sprechertext: Vorstufe zum ganzen Pack: Rahmen und Knautschzone allein. Die Zahlen sind ein Zwischenstand (Probe LFP, Knautschbreite 20 mm). "
          f"Quellen: {Q_X1}; Bild sim/mechanik/x1b_knautschzone/kraft_eindringung_oc.png; Bausteine X1.md, X1b.md. Annahmen: Pfahl Ø254 mm, Restkraft 100 kN (kein Beleg). Hinweis: Hier OpenCourant (AGPLv3, intern genutzt).")
bild(s, "sim/mechanik/x1b_knautschzone/kraft_eindringung_oc.png", 0.4, 2.0, 5.0, 4.6, "Kraft über Eindringung, Zielband (Kraft ab 100 kN, Energie 5 kJ) im Bild (zu prüfen).")
bild(s, "sim/mechanik/x1_seitencrash/kraft_weg.png", 5.6, 2.0, 5.0, 3.3, "Kraft über Weg (quasistatisch), Zielband 30–80 kN im Bild (zu prüfen).")
tb(s, 10.7, 2.0, 2.4, 3.0, f"Spitzenkraft {f(x1b['kraft_max_kN'])} kN, mittlere Kraft {f(x1b['kraft_mittel_bis_w_kN'])} kN (LFP, w = {f(x1b['w'], 0)} mm).", 11, False, GRAU)
ann(s, 5.6, 5.5, 7.4, "Pfahl Ø254 mm und Restkraft 100 kN sind Annahmen ohne Beleg. Zwischenstand, nicht von Opus geprüft.", 0.55)

# ---------------- Anhang A3: Softwarestand ----------------
swl, Q_S = D.software()
rows = [["Aufgabe", "Programm", "Version"]]
for a_, p_, v_ in swl[:11]:
    rows.append([kurz(a_, 40), kurz(p_.replace("`", ""), 70), kurz(v_.replace("`", ""), 45)])
s = folie("Anhang A3: Softwarestand",
          "Alle Rechnungen laufen mit den hier gelisteten Programmen; der Stand wird in SOFTWARE.md und requirements.txt geführt (Reproduzierbarkeit, REQ-D09).",
          f"Sprechertext: Softwarestand für die Reproduzierbarkeit. Quelle: {Q_S}, requirements.txt. Die Zeile python-pptx in SOFTWARE.md ist veraltet (Eintrag lautet noch „nicht installiert“, Installation erfolgte mit B5, Version 1.0.2).")
tabelle(s, 0.5, 2.0, 12.3, rows, [3, 6, 3], 10.5, rowh=0.36)

out = D.P("praesentation", "unternehmenspraesentation.pptx")
prs.save(out)
print("geschrieben:", out, "Folien:", len(prs.slides))
