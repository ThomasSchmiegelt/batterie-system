#!/usr/bin/env python3
"""KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Auftrag pm/graph/AUFTRAG_GRAPH.md Punkt 3.
Export der Anforderungen als ReqIF 1.2 -> pm/graph/anforderungen.reqif (aus pm/anforderungen.json und pm/graph/graph.json).
Attribute: Text, Wert, Methode, Ebene, Kriterium, Bewertung, Herkunft. Beziehungen: verifiziert_durch (Anforderung -> Ergebnis),
erfuellt_beitrag (Entscheidung -> Anforderung). Prüfung: gegen das OMG-XSD (wird in ein Temp-Verzeichnis geladen, nichts im Repo
abgelegt; der XHTML-Teil des Schemas wird durch einen Stub ersetzt, weil die Datei nur String-Attribute nutzt), sonst Wohlgeformtheit
plus Strukturprüfung (Referenzen, eindeutige IDs).     python3 pm/graph/reqif.py"""
import json, re, sys, tempfile, datetime, urllib.request
from pathlib import Path
from xml.sax.saxutils import quoteattr, escape

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(R / "pm/plan"))
import verifikation as V
NS = "http://www.omg.org/spec/ReqIF/20110401/reqif.xsd"
ANF = json.loads((R / "pm/anforderungen.json").read_text())["anforderungen"]
G = json.loads((R / "pm/graph/graph.json").read_text())
N = {n["id"]: n for n in G["nodes"]}
JETZT = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S%z"); JETZT = JETZT[:-2] + ":" + JETZT[-2:]


def xid(prefix, s): return prefix + "_" + re.sub(r"[^A-Za-z0-9_.-]", "_", s)
def q(s): return quoteattr(str(s))
def attr(o, defn, v): return f'<ATTRIBUTE-VALUE-STRING THE-VALUE={q(v)}><DEFINITION><ATTRIBUTE-DEFINITION-STRING-REF>{defn}</ATTRIBUTE-DEFINITION-STRING-REF></DEFINITION></ATTRIBUTE-VALUE-STRING>'

ATTR_REQ = ["Text", "Wert", "Methode", "Ebene", "Kriterium", "Bewertung", "Herkunft"]
ATTR_ENT = ["Titel", "Status"]
ATTR_ERG = ["Datei", "Schluessel"]
used_erg, used_ent = {}, {}
rels = []
for e in G["edges"]:
    if e["typ"] == "verifiziert_durch" and e["source"].startswith("REQ-"): used_erg[e["target"]] = 1; rels.append(("verifiziert_durch", e["source"], e["target"], "REQ"))
    if e["typ"] == "erfuellt_beitrag": used_ent[e["source"]] = 1; rels.append(("erfuellt_beitrag", e["source"], e["target"], "ENT"))

o = ['<?xml version="1.0" encoding="UTF-8"?>', f'<REQ-IF xmlns="{NS}" xml:lang="de">', "<THE-HEADER>",
     f'<REQ-IF-HEADER IDENTIFIER="hdr_batterie"><COMMENT>KI-generiert (Claude Sonnet, 2026-11-23), Entwurf. Nicht vom Menschen freigegeben. Erzeugt von pm/graph/reqif.py.</COMMENT>',
     f"<CREATION-TIME>{JETZT}</CREATION-TIME><REPOSITORY-ID>batterie-system</REPOSITORY-ID><REQ-IF-TOOL-ID>pm/graph/reqif.py</REQ-IF-TOOL-ID>",
     "<REQ-IF-VERSION>1.2</REQ-IF-VERSION><SOURCE-TOOL-ID>pm/anforderungen.json</SOURCE-TOOL-ID><TITLE>Anforderungen Batteriesystem BT-000 (Entwurf, KI-generiert)</TITLE></REQ-IF-HEADER>",
     "</THE-HEADER>", "<CORE-CONTENT><REQ-IF-CONTENT>",
     f'<DATATYPES><DATATYPE-DEFINITION-STRING IDENTIFIER="dt_string" LAST-CHANGE="{JETZT}" LONG-NAME="String" MAX-LENGTH="32000"/></DATATYPES>', "<SPEC-TYPES>"]
for tid, name, attrs in (("t_req", "Anforderung", ATTR_REQ), ("t_ent", "Entscheidung", ATTR_ENT), ("t_erg", "Ergebnis", ATTR_ERG)):
    o.append(f'<SPEC-OBJECT-TYPE IDENTIFIER="{tid}" LAST-CHANGE="{JETZT}" LONG-NAME="{name}"><SPEC-ATTRIBUTES>')
    for a in attrs: o.append(f'<ATTRIBUTE-DEFINITION-STRING IDENTIFIER="{tid}_{a}" LAST-CHANGE="{JETZT}" LONG-NAME="{a}"><TYPE><DATATYPE-DEFINITION-STRING-REF>dt_string</DATATYPE-DEFINITION-STRING-REF></TYPE></ATTRIBUTE-DEFINITION-STRING>')
    o.append("</SPEC-ATTRIBUTES></SPEC-OBJECT-TYPE>")
for rt in ("verifiziert_durch", "erfuellt_beitrag"): o.append(f'<SPEC-RELATION-TYPE IDENTIFIER="rt_{rt}" LAST-CHANGE="{JETZT}" LONG-NAME="{rt}"/>')
o.append(f'<SPECIFICATION-TYPE IDENTIFIER="st_anf" LAST-CHANGE="{JETZT}" LONG-NAME="Anforderungsspezifikation"/></SPEC-TYPES>')
o.append("<SPEC-OBJECTS>")
for r in ANF:
    b, ist, kt, _ = V.bewerte(r)
    kr = r.get("kriterium") or []; kr = [kr] if isinstance(kr, dict) else kr
    herk = "; ".join(f"{k.get('groesse')}: {k.get('herkunft_kriterium')}" for k in kr) or "nicht definiert"
    vals = dict(Text=r["text"], Wert=r.get("wert", ""), Methode=r.get("methode", ""), Ebene=r.get("ebene", ""), Kriterium=kt.replace("<br>", "; "), Bewertung=b, Herkunft=herk)
    o.append(f'<SPEC-OBJECT IDENTIFIER="{xid("o", r["id"])}" LAST-CHANGE="{JETZT}" LONG-NAME={q(r["id"])}><TYPE><SPEC-OBJECT-TYPE-REF>t_req</SPEC-OBJECT-TYPE-REF></TYPE><VALUES>'
             + "".join(attr(r, f"t_req_{a}", vals[a]) for a in ATTR_REQ) + "</VALUES></SPEC-OBJECT>")
for e in sorted(used_ent):
    n = N[e]; o.append(f'<SPEC-OBJECT IDENTIFIER="{xid("o", e)}" LAST-CHANGE="{JETZT}" LONG-NAME={q(e)}><TYPE><SPEC-OBJECT-TYPE-REF>t_ent</SPEC-OBJECT-TYPE-REF></TYPE><VALUES>'
                       + attr(n, "t_ent_Titel", n.get("name", "")) + attr(n, "t_ent_Status", n.get("status", "")) + "</VALUES></SPEC-OBJECT>")
for e in sorted(used_erg):
    d, _, s = e.partition("::"); o.append(f'<SPEC-OBJECT IDENTIFIER="{xid("o", e)}" LAST-CHANGE="{JETZT}" LONG-NAME={q(e[:200])}><TYPE><SPEC-OBJECT-TYPE-REF>t_erg</SPEC-OBJECT-TYPE-REF></TYPE><VALUES>'
                                          + attr(None, "t_erg_Datei", d) + attr(None, "t_erg_Schluessel", s) + "</VALUES></SPEC-OBJECT>")
o.append("</SPEC-OBJECTS><SPEC-RELATIONS>")
for i, (t, a, b, _) in enumerate(rels):
    o.append(f'<SPEC-RELATION IDENTIFIER="r{i}" LAST-CHANGE="{JETZT}"><TYPE><SPEC-RELATION-TYPE-REF>rt_{t}</SPEC-RELATION-TYPE-REF></TYPE><SOURCE><SPEC-OBJECT-REF>{xid("o", a)}</SPEC-OBJECT-REF></SOURCE><TARGET><SPEC-OBJECT-REF>{xid("o", b)}</SPEC-OBJECT-REF></TARGET></SPEC-RELATION>')
o.append(f'</SPEC-RELATIONS><SPECIFICATIONS><SPECIFICATION IDENTIFIER="spec_anf" LAST-CHANGE="{JETZT}" LONG-NAME="Anforderungen BT-000"><TYPE><SPECIFICATION-TYPE-REF>st_anf</SPECIFICATION-TYPE-REF></TYPE><CHILDREN>')
for r in ANF: o.append(f'<SPEC-HIERARCHY IDENTIFIER="{xid("h", r["id"])}" LAST-CHANGE="{JETZT}"><OBJECT><SPEC-OBJECT-REF>{xid("o", r["id"])}</SPEC-OBJECT-REF></OBJECT></SPEC-HIERARCHY>')
o.append("</CHILDREN></SPECIFICATION></SPECIFICATIONS></REQ-IF-CONTENT></CORE-CONTENT></REQ-IF>")
out = R / "pm/graph/anforderungen.reqif"; out.write_text("\n".join(o) + "\n")
print(f"geschrieben: {out.relative_to(R)}; {len(ANF)} Anforderungen, {len(used_ent)} Entscheidungen, {len(used_erg)} Ergebnisse, {len(rels)} Beziehungen")

# ---- Prüfung
from lxml import etree
doc = etree.parse(str(out)); print("wohlgeformt: ja")
ids = [e.get("IDENTIFIER") for e in doc.iter() if e.get("IDENTIFIER")]
refs = [e.text for e in doc.iter() if isinstance(e.tag, str) and e.tag.endswith("-REF")]
print(f"Strukturprüfung: IDs {len(ids)}, doppelt {len(ids) - len(set(ids))}, Referenzen {len(refs)}, ohne Ziel {len([x for x in refs if x not in set(ids)])}")
try:
    with tempfile.TemporaryDirectory() as td:
        t = Path(td)
        x = urllib.request.urlopen("https://www.omg.org/spec/ReqIF/20110401/reqif.xsd", timeout=20).read().decode()
        (t / "xml.xsd").write_bytes(urllib.request.urlopen("https://www.w3.org/2001/xml.xsd", timeout=20).read())
        (t / "stub.xsd").write_text('<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema" targetNamespace="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/xhtml" elementFormDefault="qualified">'
                                    '<xsd:group name="xhtml.BlkStruct.class"><xsd:choice><xsd:any namespace="##any" processContents="skip"/></xsd:choice></xsd:group></xsd:schema>')
        x = x.replace("http://www.w3.org/2001/xml.xsd", "xml.xsd").replace("http://www.omg.org/spec/ReqIF/20110402/driver.xsd", "stub.xsd")
        (t / "reqif.xsd").write_text(x)
        sch = etree.XMLSchema(etree.parse(str(t / "reqif.xsd")))
        # Das einzig abrufbare OMG-XSD (20110401) ist ReqIF 1.0.1 und fixiert REQ-IF-VERSION auf 1.0; ein 1.2-XSD ist unter omg.org nicht abrufbar.
        ok12 = sch.validate(doc); fehl = [e.message for e in sch.error_log if "REQ-IF-VERSION" not in e.message]
        d10 = etree.fromstring(out.read_text().replace("<REQ-IF-VERSION>1.2<", "<REQ-IF-VERSION>1.0<").encode()); ok10 = sch.validate(d10)
        print("XSD OMG 20110401 (ReqIF 1.0.1, XHTML-Teil Stub): Datei mit Version 1.2:", "gültig" if ok12 else f"nur Versionswert beanstandet ({len(fehl)} andere Fehler)", "; Kopie mit Version 1.0:", "gültig" if ok10 else "UNGÜLTIG")
        for e in list(sch.error_log)[:10]:
            if "REQ-IF-VERSION" not in e.message: print("  ", e.line, e.message[:200])
except Exception as e:
    print("XSD nicht abrufbar/prüfbar:", repr(e)[:200], "-> nur Wohlgeformtheit und Strukturprüfung")
