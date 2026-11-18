"""KI-generiert (Claude Sonnet, 2026-11-18). Minimaler ASCII-frd-Leser (Knotenergebnisse)."""
import numpy as np
def lies(fn):
    nodes = {}; frames = []; cur = None; mode = None; step = None
    for ln in open(fn):
        if ln.startswith("    1PSTEP") or ln.startswith("    1P"): pass
        if ln.startswith("    2C"): mode = "n"; continue
        if ln.startswith("    3C") : mode = "e"; continue
        if ln.startswith("  100CL"):
            t = float(ln[12:24]); cur = {"t": t}; frames.append(cur); mode = None; continue
        if ln.startswith(" -4"):
            name = ln[5:13].strip(); cur[name] = {}; mode = ("r", name); continue
        if ln.startswith(" -3"): mode = None; continue
        if ln.startswith(" -1"):
            if mode == "n" or (mode is None and False): pass
            if mode == "n":
                nodes[int(ln[3:13])] = (float(ln[13:25]), float(ln[25:37]), float(ln[37:49]))
            elif isinstance(mode, tuple):
                v = [float(ln[13 + 12 * i:25 + 12 * i]) for i in range((len(ln.rstrip()) - 13) // 12)]
                cur[mode[1]][int(ln[3:13])] = v
    return nodes, frames
