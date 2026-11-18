| Dok.-Nr. | Auftrag Q-C2 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Quellensuche Parametersätze 4680 und LFP-Blade; Blade-Pulsdatensatz beschaffen | Ersteller | Claude Opus (KI) | Prüfer | Opus |

> KI-generiert, Opus → Sonnet, 2026-11-17. Autor: „der richtige parametersaz ist wichtig. erst den“.
1. WebSearch (standard): offen zugängliche Quellen für elektrochemische Parameter (DFN/P2D) der **Tesla 4680** (Elektrodendicken, Porosität, Partikelgröße, Diffusion, OCV) und **LFP-Prismatik/Blade** (oder großformatige LFP mit Dicken ~ 70 µm je Seite). Bevorzugt: Open-Access-Artikel, PyBaMM-Parametersätze (GitHub), Datensätze. Je URL `curl -s -o /dev/null -w "%{http_code}"`, nur 200, keine Bezahlschranke, keine gefälschten User-Agents.
2. Neue Zeile `W28` in `forschung/themen_wissen.tsv` (Suchbegriffe eng: µm, porosity, particle, radius, diffusivity, m2/s, conductivity, S/m, OCV, mol/m3, exchange, Ah, mΩ), max. 6 URLs; dann `setsid nohup bash -c 'while pgrep -f "[l]auf.sh" >/dev/null; do sleep 20; done; bash forschung/lauf.sh wissen W28' > forschung/lauf_W28.log 2>&1 < /dev/null &`.
3. Blade-Pulsdatensatz (Readme `quellen/blade_datensatz/0_readme.txt`, Chen/Emadi/Kollmeyer, CC BY 4.0): Ablageort (DOI/Repository) finden. Wenn Test#5 (BYD Blade) einzeln oder das Ganze ≤ 3 GB ladbar ist: nach `/home/cae/cae_projekte/batterie/blade_datensatz/` laden, Link `quellen/blade_datensatz/daten` setzen, Lizenzzeile in `docs/10_lizenzen_und_quellen.md`. Größer → nur URL und Größe melden.
Abbruch 20 min. Rückgabe ≤ 4 Zeilen.
