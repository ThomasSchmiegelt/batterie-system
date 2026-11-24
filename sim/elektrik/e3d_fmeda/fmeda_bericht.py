#!/usr/bin/env python3
"""E3d: erzeugt ERGEBNIS.md v0.2 aus ergebnis.json. KI-generiert (Claude Sonnet, 2026-11-24), Entwurf."""
import json, pathlib
H = pathlib.Path(__file__).resolve().parent; E = json.load(open(H / "ergebnis.json")); alt = json.load(open("/home/cae/cae_projekte/batterie/e3/e3d_ergebnis_v01.json")); Z = E["ziel"]
f = lambda x, n=2: f"{x:.{n}f}".replace(".", ",")
c = E["cmu"]["LFP"]; n = E["cmu"]["NMC"]; assert all(abs(c[s][k] - n[s][k]) < 1e-12 for s in Z for k in ("SPFM", "LFM")), "LFP und NMC verschieden"
def zeile(sg): x = c[sg]; return f"| {sg} (ASIL {Z[sg]['ASIL']}) | {f(x['lambda_SR_FIT'])} FIT | {f(x['lambda_SPF_RF_FIT'],3)} FIT | {f(x['lambda_MPF_latent_FIT'],3)} FIT | {f(x['SPFM']*100)} % | {Z[sg]['SPFM']*100:.0f} % {'ok' if x['SPFM']>=Z[sg]['SPFM'] else '**verfehlt**'} | {f(x['LFM']*100)} % | {Z[sg]['LFM']*100:.0f} % {'ok' if x['LFM']>=Z[sg]['LFM'] else '**verfehlt**'} | {f(x['PMHF_Beitrag_FIT'],3)} FIT |"
def top(v, sg): return "; ".join(f"{d['posten']} (x{d['anzahl_Teile']}) {f(d['SPF_RF_FIT']+d['MPF_latent_FIT'],3)}" for d in E["top"][v][sg])
a = alt["cmu"]["LFP"]; m2 = E["massnahmen"]; k2 = list(m2)[0] if m2 else None
t = f"""| Dok.-Nr. | ERG-E3d | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Ergebnis E3d: grobe FMEDA der CMU-Platine (ISO 26262-5, Grobentwurf) | Ersteller | Claude Sonnet (KI), Auftrag Opus | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-24), Entwurf, nicht vom Menschen freigegeben, Prüfung Opus offen. Anforderung: REQ-P18. v0.2 ersetzt v0.1: Die Stückliste ist die überarbeitete (ERW-E3 Nachtrag 7, B-BAT-055, ENT-192/193). Alle FIT-Werte, Ausfallartenanteile und Diagnosedeckungen sind weiter **Annahmen Opus (ERW-E3d)**. Zahlen aus `ergebnis.json` (Ordner `sim/elektrik/e3d_fmeda/`).

## Was geändert wurde gegenüber v0.1
- Eingabe: `sim/elektrik/e3_platine/cmu_<V>_bom.csv` neu, je {E['cmu']['LFP']['Teile']} Teile. Neu: 18 Doppel-N-FET SOT-363 mit zwei Schaltern in Reihe statt Einzel-FET (**M1 ist jetzt Ist-Stand**, in `fmeda.py` automatisch aktiv, sobald die Klasse `Doppel_NMOS_generisch` in der Stückliste steht) und 3 × 6-Zellen-Überspannungsschutz statt 1 × Summenschutz (Klasse `OVP6_generisch`, Einstufung wie bisher „Sekundärschutz“, FIT je Gehäuse 5, also 3 × 5 FIT).
- Der FIT-Ansatz je Gehäuse bleibt (MOSFET klein 1 FIT je Gehäuse, 18 Gehäuse), wie in ERW-E3 N7 („FETs bleiben 18 Gehäuse“). Keine neuen Annahmen. Das Was-wäre-wenn M1/M1+M2 aus v0.1 entfällt (M1 steckt in den Zahlen); M2 bleibt als Was-wäre-wenn.
- Die Einstufungsregeln sind unverändert (siehe v0.1: Zellabgriff, Ausgleichs-FET, AFE, Sekundärschutz, Stecker J1 als gemeinsame Ursache).

## Ergebnis (je CMU, `ergebnis.json` Block `cmu`; LFP = NMC)
| SG | λ_SR | λ_RF | λ_MPF,latent | SPFM | Ziel | LFM | Ziel | PMHF-Beitrag |
|---|---|---|---|---|---|---|---|---|
{zeile('SG-01')}
{zeile('SG-02')}

Vorher (v0.1): SG-01 SPFM {f(a['SG-01']['SPFM']*100)} %, LFM {f(a['SG-01']['LFM']*100)} %; SG-02 SPFM {f(a['SG-02']['SPFM']*100)} %, LFM {f(a['SG-02']['LFM']*100)} % (Ziel verfehlt). Ziele jetzt: {'alle erreicht' if not E['verfehlt'] else 'verfehlt: ' + ', '.join(E['verfehlt'])}.
Pack (Block `pack`, nur CMU-Platinen): PMHF-Beitrag SG-01 LFP {f(E['pack']['LFP']['SG-01']['PMHF_Beitrag_FIT'],3)} FIT ({E['pack']['LFP']['anzahl_CMU']} CMU), NMC {f(E['pack']['NMC']['SG-01']['PMHF_Beitrag_FIT'],3)} FIT ({E['pack']['NMC']['anzahl_CMU']}); SG-02 LFP {f(E['pack']['LFP']['SG-02']['PMHF_Beitrag_FIT'],2)} FIT, NMC {f(E['pack']['NMC']['SG-02']['PMHF_Beitrag_FIT'],2)} FIT.
Top-5 SG-02 (FIT je CMU, Rest + latent): {top('LFP','SG-02')}.
Top-5 SG-01: {top('LFP','SG-01')}.
{('Was-wäre-wenn (nicht umgesetzt) ' + k2 + ': SG-02 SPFM ' + f(m2[k2]['SG-02']['SPFM']*100) + ' %, LFM ' + f(m2[k2]['SG-02']['LFM']*100) + ' %.') if k2 else 'Kein Ziel verfehlt, daher kein Was-wäre-wenn (Block `massnahmen` leer).'}

## Abgleich ERW-E3 Nachtrag 7
| Erwartung | Befund | Urteil |
|---|---|---|
| SG-02 SPFM 97,85 % (Ziel ≥ 97 %) | {f(c['SG-02']['SPFM']*100)} % | {'ok' if abs(c['SG-02']['SPFM']*100-97.85)<0.01 else 'abweichend'} |
| SG-01 weiter ≥ 99 % / ≥ 90 % | SPFM {f(c['SG-01']['SPFM']*100)} %, LFM {f(c['SG-01']['LFM']*100)} % | ok; LFM sinkt von {f(a['SG-01']['LFM']*100)} auf {f(c['SG-01']['LFM']*100)} %, weil 3 statt 1 Sekundärschutz-IC latent ausfallen können (0,75 statt 0,25 FIT) |

## Offene Fragen an Opus
1. Der Doppel-N-FET wird mit 1 FIT je Gehäuse gerechnet (wie der Einzel-FET). Ein Gehäuse mit zwei FETs könnte höher liegen; keine FIT-Annahme dafür in der ERWARTUNG.
2. Die Einstufung „Kurzschluss eines der beiden FETs = latenter Zweitfehler, DC 90 %“ übernimmt die Annahme aus v0.1 (M1). Gleichzeitiger Kurzschluss beider FETs und gemeinsame Ursache im Gehäuse sind nicht betrachtet.
3. Der zweite Gate-Ausgang je Kanal ist am AFE ein generischer Pin (kein Bauteilbeleg); „AFE Ausgleich hängt an“ bleibt mit vollem IC-Anteil angesetzt (0,40 FIT).
4. Weitere offene Fragen 2 bis 6 aus v0.1 (konservative Einstufungen, Kommunikationsausfall sicher, PMHF nur RF-Term, SG-07 und SG-03 nicht Umfang, Pack nur CMU) gelten unverändert.

## Dateien
`fmeda.py` (neu geschrieben und ersetzt, `e3c` liest nur), `fmeda_bericht.py`, `bild.py`, `fmeda_LFP.csv`, `fmeda_NMC.csv`, `ergebnis.json`, `e3d_fmeda.png`, `lesehilfe.md`, Folienbaustein `praesentation/bausteine/E3d.md`.

*KI-generiert (Claude Sonnet, 2026-11-24), Entwurf.*
"""
(H / "ERGEBNIS.md").write_text(t); print(t[1400:2600])
