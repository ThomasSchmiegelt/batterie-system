| Dok.-Nr. | Auftrag B1-b | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Projektbericht Fassung 0.2: Stand 2026-11-17 abends nachziehen | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> KI-generiert, Opus → Sonnet. Autor: „zieh als erstes den bericht nach“. Regeln wie AUFTRAG_BERICHT.md (jede Zahl mit Fundstelle, Lesehilfe je Bild, Bilder kopieren, keine eigene Rechnung). Version 0.2.
Neu bzw. zu ändern in `bericht/bericht.tex`:
1. Kap. 2 Vorgaben: REQ-P05 (LFP 20 min, NMC 30 min), REQ-P09 festgelegt, Breite fest (Autor), Gehäuse je Variante (ENT-102/103), Kühlplatte oben+unten (ENT-088 ersetzt ENT-081).
2. Kap. 8 Wärme erweitern: K0-Bilder durch Cycles-Bilder ersetzen (`sim/kuehlung/k0_zelle/bilder/tafel_L2.png`, je ein cycles_*_t1200); neuer Abschnitt K1 Schnellladen (Tabelle aus `sim/kuehlung/TABELLEN_TEMPERATUR.md`, landkarte.png, profile.png, verlauf_kuehlung_*.png, Deutung aus DEUTUNG.md als Opus gekennzeichnet) und K1b.
3. Neues Kap. „Gehäuse und Pack“: Recherche W21/W22 (Bauweise, Querträgerprofil, Seitenlast; gesperrter SSAB-Wert erwähnen), Herstellervergleich Rundzellen (`forschung/vergleich_rundzellen.md`), M0 (Höhe/Länge, Bilder draufsicht/schnitt), G4 (Freigabestand: Massen, Kollisionen; Bilder pack_*_gesamt, _explosion, _schnitt, _ecke beider Varianten, pack_massen.png).
4. Neues Kap. „Elektrik E1“: Querschnitte, Verluste, Methodenkorrektur (Bilder querschnitte.png, verluste.png).
5. Kap. 9 Fehler: Zeilen ergänzen – NMC-K3 Luftspalt statt Tab-Scheibe (Opus-Vorgabe fehlte); E1 voller Strom über Gruppenlänge (Sonnet, Methode, Opus fand es am Band); G4 Vollmaterial-Massen; Opus-Schätzung Gehäuseersparnis 15–25 kg statt 7 kg; W22 Paketgrenze schnitt Maßstellen ab; Monitor-Wartebefehl fand sich selbst.
6. Kap. 10 Entscheidungen aus docs/04 neu (103 Akten), Kap. 11 offene Punkte: ≈ 30 vorgeschlagene Werte je Variante (ENT-014…080), Kühlplatte BT-610 Kanäle, Crash X, Zellmodell C1–C3, Bericht EN.
7. Zusammenfassung neu (½ Seite, beide Varianten mit Masse, Schnellladezeit, Kühlung).
Zweimal kompilieren, 0 Fehler; 3 neue Seiten als Bild ansehen. ≤ 45 min. Rückgabe ≤ 4 Zeilen.
