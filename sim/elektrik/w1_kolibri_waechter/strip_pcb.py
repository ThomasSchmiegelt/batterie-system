# KI-generiert (Claude Sonnet, 2026-11-25), Entwurf. W1: entfernt aus einer .kicad_pcb (Text) alle Footprints mit Referenz MH* und alle Sperrflächen (zone ... keepout). Aufruf: strip_pcb.py <ein> <aus>
import sys
def bloecke(t, kopf):
    """Liefert (start, ende) aller Top-Level-Blöcke, die mit '(kopf' beginnen und passende Klammer haben."""
    res = []; i = 0
    while True:
        i = t.find("\n\t(" + kopf, i)
        if i < 0: return res
        j = i + 1; d = 0; ins = False
        while True:
            c = t[j]
            if ins:
                if c == "\\": j += 1
                elif c == '"': ins = False
            else:
                if c == '"': ins = True
                elif c == "(": d += 1
                elif c == ")":
                    d -= 1
                    if d == 0: break
            j += 1
        res.append((i + 1, j + 1)); i = j
def strip(src, dst):
    t = open(src).read(); weg = []
    for a, e in bloecke(t, "footprint"):
        if '(property "Reference" "MH' in t[a:e]: weg.append((a, e))
    for a, e in bloecke(t, "zone"):
        if "(keepout" in t[a:e]: weg.append((a, e))
    for a, e in sorted(weg, reverse=True): t = t[:a] + t[e:]
    open(dst, "w").write(t); return len(weg)
if __name__ == "__main__": print("entfernt", strip(sys.argv[1], sys.argv[2]))
