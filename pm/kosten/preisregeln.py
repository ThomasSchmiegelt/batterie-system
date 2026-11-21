"""preisregeln.py -- gemeinsame Preis-Zuordnung Position -> Eintrag in eingaben.json (KO2, REQ-P16).

KI-generiert (Claude Sonnet, 2026-11-19), Auftrag KO2. Entwurf.
Eine Stelle für die Zuordnung, damit Stückliste (zeigt den Preis an) und kosten.py (rechnet) denselben Eintrag lesen. Keine Preise im Code.
"""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
EIN = json.loads((ROOT / "pm/kosten/eingaben.json").read_text())
num = lambda x: isinstance(x, (int, float)) and not isinstance(x, bool)


def schluessel(pos, bt):
    """-> Schlüssel in eingaben.eur_je (BT oder BT:Art, Positionsabbildung pos_zu_preis)."""
    return EIN["pos_zu_preis"].get(pos, bt)


def stufe(status):
    """Status-Text -> eine der 3 Stufen aus eingaben.status_werte (verifiziert / abgeleitet / Schätzung) oder 'offen'."""
    s = (status or "").lower()
    if s.startswith("verifiziert"): return "verifiziert"
    if s.startswith("abgeleitet"): return "abgeleitet"
    if s.startswith("schätzung"): return "Schätzung"
    return "offen"


def preis_je(pos, bt, V):
    """-> dict(wert, einheit, status, herkunft[, teile]) für die Anzeige in der Stückliste. Rechnet nichts."""
    k = schluessel(pos, bt)
    if bt in EIN["entfaellt"] and k == bt:
        return dict(wert=0.0, einheit="–", status="entfällt", herkunft=EIN["entfaellt"][bt])
    p = EIN["eur_je"].get(k)
    if p is None: return dict(wert=None, einheit=None, status="offen (kein Eintrag in eingaben.json)", herkunft="pm/kosten/eingaben.json")
    w = p["wert"]; w = w.get(V) if isinstance(w, dict) else w
    d = dict(wert=w, einheit=p["einheit"], status=p["status"], herkunft=p["herkunft"] + " (Schlüssel " + k + ")")
    if "teile" in p: d["teile"] = p["teile"]
    return d
