| Dok.-Nr. | BAT-DOC-13 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Stückliste Konstruktionsstand (SL3) – Variante LFP | Ersteller | Claude Sonnet (KI), pm/bauteile/stueckliste_v3.py | Prüfer | Opus (Stichprobe), Mensch offen |

> **KI-generiert.** (KI-generiert (Claude Sonnet, 2026-11-19), Auftrag G5.1, ergänzt SL3.1 (Auftrag KO2).) Nicht von Hand bearbeiten: `python3 pm/bauteile/stueckliste_v3.py --variante LFP` schreibt die Datei neu. Entwurf, nicht freigegeben.
> Quelle der Geometrie (cad/baukasten/PLAN.md §1): jede Position trägt einen Generator `<modul>.<funktion>`. Preise sind eine Anzeige aus `pm/kosten/eingaben.json` (SL3.1), gerechnet wird in `pm/kosten/kosten.py`. Hersteller/Typ und Datenblatt aus `pm/bauteile/kaufteile_datenblatt.json` (Quelle `forschung/datenblaetter.md`).

**Positionen:** 56 (Stufe K/F/H/-: 18 / 28 / 4 / 6), Stufe H 7.1 %. **Masse gesamt:** 626.77 kg (CAD e2d 620.57 kg, +1.00 %). **Zellen:** 250, 73.92 kWh. Positionen mit Masse „offen“: 10.

Art: K Kaufteil, E Eigenteil, S Systemteil außerhalb. Stufe: K Konstruktionsstand, F Kaufteilform, H Hüllkörper, - keine Geometrie. Masse „offen“: keine CAD-Geometrie, keine Akte.

## BT-100 Zelle

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 100.1 | BT-100 Zelle | Zelle (prismatisch, Blade-Querschnitt, verkürzt, LFP) | – | 250 | 1,850 | 462,500 | Akte (BT-100 masse_g) | 50,000 €/kWh | Schätzung (Annahme Opus, ERW-KO1) | K | zelle.zelle_prismatisch | F | ENT-002, ENT-005, ENT-012, ENT-014, ENT-015, ENT-016, ENT-017, ENT-018, ENT-019, ENT-020 |  |

## BT-200 Zellstack

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 200.1 | BT-210 Zellreihe | Zellreihe zwischen Querträgern (Anordnung, kein Eigenteil) | – | offen | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | – | - | – | Anordnung der Zellen, keine eigene Geometrie; Masse steckt in 100.1. Opus bestätigen. |
| 200.2 | BT-220 Zwischenlage | Zwischenlage zwischen Zellen (Schaum, je Spalt eines Feldes) | – | 242 | 0,018 | 4,450 | Annahme (Opus 2026-11-19: Menge, Werkstoff Schaum_Zwischenlage 300 kg/m3; Masse = Zellfläche x Dicke x Dichte, noch nicht CAD) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | K | zelle.zwischenlage | K | ENT-012 | Menge 242 = 250 - 2 x 4 (Opus). Masse aus Zellfläche (Länge x Breite) x A_zellabstand_LFP_mm x Dichte Schaum_Zwischenlage; CAD-Stufe folgt in zelle.py. |
| 200.3 | BT-230 Wärmeleitmaterial | Wärmeleitmaterial / Pad Zelle-Kühlplatte | – | 2 | 6,765 | 13,529 | CAD-Volumen x Dichte | 20,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | K | zelle.pad | F | – |  |
| 200.4 | BT-240 Verspannung | Verspannung der Zellreihen: entfällt als Teil | – | offen | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 0 (entfällt) | entfällt | E | – | - | ENT-012 |  |

## BT-300 Regelung (BMS)

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 300.1 | BT-310 BMS-Hauptsteuergerät | BMS-Platine | – | 1 | 0,400 | 0,400 | Annahme (ERW-E2 N1) | 120,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | elektronik.bms_platine | F | ENT-138, ENT-139, ENT-140, ENT-141 |  |
| 300.2 | BT-320 Zellüberwachung | Zellüberwachung CMU (Platine) | – | 14 | 0,080 | 1,120 | Annahme (ERW-E2 N1 A_e2_cmu_masse_kg) | 15,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | elektronik.cmu | F | ENT-111, ENT-112, ENT-114, ENT-115 |  |
| 300.3 | BT-330 Temperaturfühler Zelle | Temperaturfühler Zelle (NTC) | Vishay NTCS0603E3 (10 kΩ, Typ 0603) (BT-330_vishay_NTCS0603E3.pdf, S. 1, 2) | 56 | 0,000 | 0,000 | CAD-Volumen x Dichte | 0,130 €/Stück | abgeleitet aus Distributorpreis | K | elektronik.ntc | F | ENT-116 | NTC-Volumen aus A_e2d_ntc_mm x Anzahl; CAD-Gruppe E2_FPC_Detail fasst Tabs, NTC und Stecker zusammen und wird dafür geteilt. Datenblattmasse 0.000336 kg weicht von der Annahmemasse 6.9e-05 kg ab (CAD zieht nach Freigabe nach). |
| 300.4 | BT-340 Strommessung | Shunt (Strommessung) | Isabellenhütte IVT-S (Shunt, 100–2500 A) (BT-340_isabellenhuette_IVT-S.pdf, S. 1, 2) | 1 | 0,100 | 0,100 | Annahme (ERW-E2 N1) | 40,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | elektronik.shunt | F | ENT-118, ENT-119 |  |
| 300.5 | BT-350 Isolationswächter | Isolationswächter | Bender iso1685 (Typ für 800 V, Datenblatt auf Autorliste) () | 1 | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 20,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | elektronik.isolationswaechter | H | ENT-120 | Menge 1 (Opus 2026-11-19). Keine Formangabe in W33, Akte oder Annahme: Stufe H bis W34. |
| 300.6 | BT-360 Messleitungen | Flexleiterplatte FPC Zelle -> CMU | – | 14 | 0,042 | 0,590 | Annahme (ERW-E2 N1 A_e2_fpc_masse_kg_m) | 8,000 €/m | Schätzung (Annahme Opus, ERW-KO1) | K | elektronik.fpc | F | ENT-121, ENT-149 |  |
| 360.3 | BT-360 Messleitungen | FPC-Detail (Tabs, FPC-Stecker an der CMU) | – | 265 | 0,000 | 0,022 | CAD-Volumen x Dichte | 0,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | elektronik.fpc_detail | F | ENT-121, ENT-149 | Mischteil (Cu-Tab 0,2 mm, Kunststoffstecker) mit Kunststoffdichte gerechnet; Masse klein, Opus bestätigen. |
| 360.4 | BT-360 Messleitungen | Daisy-Chain-Leitung mit Steckern | – | 12 | 0,004 | 0,054 | CAD-Volumen x Dichte | 3,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | elektronik.daisy_kette | F | ENT-121, ENT-149 | PLAN §4.2 nennt 360.2/360.3 für drei Teile; hier 361.1 Halter, 360.3 Detail, 360.4 Daisy. Menge = Kabelzahl, Masse inkl. Stecker. |
| 361.1 | BT-361 FPC-Halter | FPC-Halter | – | 2 | 0,068 | 0,136 | CAD-Volumen x Dichte | 0,300 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | elektronik.fpc_halter | F | – |  |

## BT-400 Verkabelung und Zellverbinder

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 400.1 | BT-410 Zellverbinder | Zellverbinder (Zellabgriff, Plus und Minus je Zelle): LFP nicht vorhanden | – | offen | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 8,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | – | - | – | LFP hat keinen Zellabgriff; Reihenverbinder stehen in 400.2 (BT-420). Position nur aus Altliste v0.2, Opus: streichen? |
| 400.2 | BT-420 Reihenverbinder | Zellverbinder = Reihenverbinder (s - 1) | – | 249 | 0,008 | 1,921 | CAD-Volumen x Dichte | 8,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | verbinder.zellverbinder_lfp | K | ENT-096, ENT-097, ENT-098 | Widerspruch CAD 130 / E1 249: 249 gilt (PLAN §4.3), CAD zieht nach. A_CAD 25 x 3 = 75 mm2, A_E1 75 mm2. |
| 400.3 | BT-430 HV-Hauptleitung | HV-Leitung im Pack (Leiter Cu) | – | 2 | 0,237 | 0,475 | CAD-Volumen x Dichte (Länge x A_CAD x Dichte Cu) | 25,000 €/m | Schätzung (Annahme Opus, ERW-KO1) | K | verbinder.hv_leitung | F | ENT-100, ENT-142 | A_CAD 50.0 mm2 = A_E1 50 mm2 (sim/elektrik/e1_querschnitte/ergebnis.json). Masse CAD 0.475 kg (Länge gesamt 1.080 m, ergebnis e2d e2.hv_laenge_gesamt_m), E1 1.814 kg (2 x 2024 mm). CAD-Verlegung gilt (PLAN §4.3). |
| 440.1 | BT-440 Stromschiene | Plus-/Minus-Anschlusslasche (Pol) | – | 2 | 0,028 | 0,057 | CAD-Volumen x Dichte | 8,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | verbinder.pol_lasche | K | – |  |
| 440.2 | BT-440 Stromschiene | Stromschienen der Schaltbox (Cu) | – | 6 | 0,102 | 0,613 | CAD-Volumen x Dichte | 8,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | verbinder.stromschiene | K | – | Stückzahl aus CAD: 12 Verbindungen nach ctx.schaltbox[schienen] (SL3 hatte 6 aus E2d, Sonnet G5.4). |

## BT-500 Struktur und Gehäuse

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 500.1 | BT-510 Gehäusewanne | Gehäusewanne (im CAD: Boden) | – | 1 | 23,715 | 23,715 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | gehaeuse.wanne | K | – |  |
| 520.1 | BT-520 Deckel mit Dichtung | Deckel | – | 1 | 15,777 | 15,777 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | gehaeuse.deckel | K | – |  |
| 520.2 | BT-520 Deckel mit Dichtung | Servicedeckel (Senkschrauben bündig) | – | 1 | 0,051 | 0,051 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 0,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | E | gehaeuse.servicedeckel | K | – |  |
| 500.3 | BT-530 Querträger | Querträger | – | 3 | 1,380 | 4,139 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | gehaeuse.quertraeger | K | ENT-082, ENT-083, ENT-084, ENT-085, ENT-086 |  |
| 500.4 | BT-540 Seitenrahmen | Seitenrahmen (Rahmenprofil, keine Knautschzone nach ENT-151) | – | 4 | 3,509 | 14,035 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | gehaeuse.seitenrahmen | K | ENT-087, ENT-151 |  |
| 500.5 | BT-550 Unterfahrschutz | Unterfahrschutz | – | 1 | 23,715 | 23,715 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 6,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | gehaeuse.unterfahrschutz | K | – |  |
| 500.6 | BT-560 Befestigungspunkte | Befestigungspunkte am Fahrzeug (Stahlhülse) | – | 12 | 0,205 | 2,465 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 1,500 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | E | gehaeuse.befestigung | K | – | Menge 12 = 6 je Längsseite, Annahme Opus A_g5_befestigung_n_je_seite (Vorgabe Opus 2026-11-19, noch nicht in annahmen.json, da A-Blöcke e2d sie nicht enthalten). |
| 500.7 | BT-570 Druckausgleichselement | Druckausgleichselement (atmend, wasserdicht) | Gore PolyVent AVS 70 (High Airflow) (BT-570_gore_auto-batteries-snapfit.pdf, S. 2) | 1 | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 5,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.druckausgleich | F | – | Ø20 mm stammt aus ERW-E2 N3 für die Schaltbox (Annahme); Übertragung auf das Pack-Element und Masse offen, W34 abwarten. |
| 580.1 | BT-580 Dichtungen | Dichtungen (Deckel, Schaltbox, Servicedeckel) | – | 3 | 0,006 | 0,018 | CAD-Volumen x Dichte | 4,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | normteile.dichtung | F | – |  |
| 590.1 | BT-590 Verbindungs- und Normteile | Schrauben (M4/M5/M8, Stahl) | – | 84 | 0,001 | 0,125 | CAD-Volumen x Dichte | 0,100 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | normteile.schraube | F | – |  |
| 590.2 | BT-590 Verbindungs- und Normteile | Kabelschuhe (Hülse + Palme) | Pfisterer Kabelschuh DIN 46235 M8, 50 mm² (Art. 300 013 260) / 35 mm² (Art. 300 010 010) (BT-590_pfisterer_300013260.pdf, S. 1, 2; BT-590_pfisterer_300010010.pdf, S. 1, 2) | 8 | 0,035 | 0,283 | CAD-Volumen x Dichte | 1,500 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | normteile.kabelschuh | F | – |  |
| 590.3 | BT-590 Verbindungs- und Normteile | Kabelclips | – | 4 | 0,002 | 0,007 | CAD-Volumen x Dichte | 0,100 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | normteile.clip | F | – |  |
| 590.4 | BT-590 Verbindungs- und Normteile | Schrumpfschlauch 0,5 mm | – | 6 | 0,004 | 0,022 | CAD-Volumen x Dichte | 0,200 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | normteile.schrumpfschlauch | F | – |  |

## BT-600 Kühlung

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 600.1 | BT-610 Kühlplatte | Kühlplatte (Blech 1/4/1 mm, Mäander 8 Bahnen laengs, Teilkanal 8 mm) | – | 2 | 23,723 | 47,445 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 12,000 €/kg | Schätzung (Annahme Opus, ERW-KO2) | E | kuehlung.kuehlplatte | K | ENT-089, ENT-090, ENT-104, ENT-105, ENT-106, ENT-152, ENT-153, ENT-154, ENT-155, ENT-156, ENT-158, ENT-159 |  |
| 600.2 | BT-620 Verteiler und Sammler | Verteiler und Sammler | – | 4 | 0,252 | 1,007 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 12,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | kuehlung.verteiler | K | – | Menge 4 = je Mäander ein Eintritts- und ein Austrittsblock (ENT-158, G5.9; Sonnet, Opus prüft). |
| 600.2b | BT-620 Verteiler und Sammler | Verteilerrohr und Sammelrohr (Al, Innen-Ø 25 mm) | – | 2 | 0,247 | 0,493 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 12,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | kuehlung.verteilerrohr | K | – | Neu G5.9 (Sonnet, Opus prüft): Rohr Ø25 innen, Wand 1,5 mm (Annahme), Masse nur Al ohne Kühlmittel. |
| 600.3 | BT-630 Kühlmittelanschlüsse | Kühlmittelanschlüsse Ein/Aus | – | 2 | 0,011 | 0,022 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 10,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kuehlung.anschluss | K | – | Generator kuehlung.anschluss, Menge 2, Stufe K (Opus-Vorgabe 2026-11-19). |
| 600.4 | BT-640 Temperaturfühler Kühlmittel | Temperaturfühler Kühlmittel | Kyocera AVX 94082 (NTC M12×1,5, Einschraub) (BT-640_kyocera-avx_94082.pdf, S. 3) | 2 | 0,017 | 0,034 | Datenblatt | 3,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.temperaturfuehler_kuehlmittel | H | – | Menge 2 (Opus 2026-11-19). Keine Formangabe: Stufe H bis W34. |
| 600.5 | BT-650 Kühlmittel | Kühlmittel Wasser-Glykol | – | offen | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 3,000 €/L | Schätzung (Annahme Opus, ERW-KO1) | K | – | - | – | Flüssigkeit, keine Geometrie (PLAN §3: Detailstufe -). |
| 600.6 | BT-660 Schnittstelle Fahrzeugkreis | Pumpe, Wärmetauscher/Kältemittelkühler | – | offen | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 0 (entfällt) | entfällt | S | – | - | ENT-107, ENT-157 | Art S; Kühlkreis wird seit Opus-Zusatz 2026-11-19 als Positionen 660.1…660.5 modelliert (Detailstufe -). |
| 660.1 | BT-661 Kühlmittelpumpe (elektrisch) | Kühlmittelpumpe (elektrisch) | Pierburg CWA100-3 (12 V PWM) (BT-661_pierburg_CWA100-3.pdf, S. 1) | 1 | 1,000 | 1,000 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 60,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | kuehlung.pumpe | F | – | Opus-Zusatz 2026-11-19 (Autor: Kühlkreis modellieren). Masse aus G5-CAD (folgt). |
| 660.2 | BT-662 Chiller (Kältemittel-Wasser-Wärmetauscher) | Chiller (Kältemittel-Wasser-Wärmetauscher) | – | 1 | 1,200 | 1,200 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 70,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | kuehlung.chiller | F | – | Opus-Zusatz 2026-11-19 (Autor: Kühlkreis modellieren). Masse aus G5-CAD (folgt). |
| 660.3 | BT-663 3/2-Wege-Ventil | 3/2-Wege-Ventil | Pierburg 3/2-Wege (Broschüre F0001) (BT-663_pierburg_CoolantValves.pdf, S. 1) | 1 | 0,400 | 0,400 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 35,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | kuehlung.ventil | F | – | Opus-Zusatz 2026-11-19 (Autor: Kühlkreis modellieren). Masse aus G5-CAD (folgt). |
| 660.4 | BT-664 Kühlmittelschläuche | Kühlmittelschläuche | EPDM DN19 (Gates 4175EC, Autorliste) () | 1 | 0,350 | 0,350 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 15,000 €/Satz | Schätzung (Annahme Opus, ERW-KO2) | K | kuehlung.schlauch | F | – | Opus-Zusatz 2026-11-19 (Autor: Kühlkreis modellieren). Masse aus G5-CAD (folgt). |
| 660.5 | BT-665 Ausgleichsbehälter | Ausgleichsbehälter | – | 1 | 0,300 | 0,300 | G5-CAD (cad/baukasten/ausgabe/ergebnis_LFP.json) | 8,000 €/Stück | Schätzung (Annahme Opus, ERW-KO2) | K | kuehlung.ausgleichsbehaelter | F | – | Opus-Zusatz 2026-11-19 (Autor: Kühlkreis modellieren). Masse aus G5-CAD (folgt). |

## BT-700 Zusatzkomponenten

| Pos. | BT | Benennung | Hersteller / Typ (Datenblatt, Seite) | Menge | Masse je [kg] | Masse ges. [kg] | Masse-Quelle | Preis | Preis-Status | Art | Generator | Stufe | Akten | Hinweis an Opus |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 700.1 | BT-710 Schaltbox | Schaltbox (Gehäuse) | – | 1 | 1,369 | 1,369 | CAD-Volumen x Dichte | 8,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | schaltbox.gehaeuse | K | ENT-144 |  |
| 700.1b | BT-710 Schaltbox | Schaltbox-Deckel | – | 2 | 0,299 | 0,598 | CAD-Volumen x Dichte | 8,000 €/kg | Schätzung (Annahme Opus, ERW-KO1) | E | schaltbox.deckel | K | ENT-144 |  |
| 700.2 | BT-711 Hauptschütze | Hauptschütz | GLVAC GLFX250/…-HC5 (12–800 VDC, 250 A) (BT-711_glvac_GLFX250.pdf, S. 1, 2, 6) | 2 | 0,400 | 0,800 | Datenblatt (cad/baukasten/annahmen_g5.json, Opus 2026-11-19) | 45,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.schuetz_haupt | F | ENT-123, ENT-124 |  |
| 700.3 | BT-712 Vorladung | Vorladeschütz und Vorladewiderstand (Widerstandsmasse 0 gesetzt) | Gigavac GV200 (Vorladeschütz) + Vishay RH050 (Vorladewiderstand) (BT-712_gigavac_GV200.pdf, S. 2, 3; BT-712_vishay_RH050.pdf, S. 1, 2) | 2 | 0,205 | 0,410 | Datenblatt (cad/baukasten/annahmen_g5.json, Opus 2026-11-19) | 25,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.schuetz_vorlade | F | ENT-125, ENT-126 |  |
| 700.4 | BT-713 Hauptsicherung | Pyrosicherung und Schmelzsicherung | Sensata PyroFuse STPS500 (Pyro) + Eaton EKC14-40 (Schmelzsicherung) (BT-713_sensata_pyrofuse.pdf, S. 1, 2; nicht geladen (Eaton EKC14-40, nur Händlerangabe Digi-Key), –) | 2 | 0,165 | 0,330 | Annahme (ERW-E2 N1) | 44,040 €/Satz | Schätzung (Annahme Opus, ERW-KO2) | K | kaufteile.sicherungen | F | ENT-127, ENT-128 |  |
| 720.2 | BT-720 Service-Trennstecker | Service-Trennbrücke mit Schrauben (LFP, ENT-150) | – | 2 | 0,039 | 0,078 | CAD-Volumen x Dichte | 15,000 €/Satz | Schätzung (Annahme Opus, ERW-KO1) | K | verbinder.trennbruecke | K | ENT-130, ENT-150 | Menge = Brückenteile laut CAD-Gruppe; Schrauben (6) in der Masse enthalten. |
| 700.6 | BT-730 HV-Steckverbinder | HV-Steckverbinder 250 A und 40 A | TE HVP 800 (250 A) / TE HVA 280 (40 A) (BT-730_te_HVP800_katalog.pdf, S. 2, 3; BT-730_te_HVA280_katalog.pdf, S. 2, 7) | 2 | 0,275 | 0,550 | Annahme (ERW-E2 N1) | 80,000 €/Satz | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.hv_stecker | F | ENT-132, ENT-133 |  |
| 700.7 | BT-740 NV-Steckverbinder | NV-Steckverbinder 26-polig | TE AMPSEAL (26-polig offen, Autorliste) () | 1 | 0,050 | 0,050 | Annahme (ERW-E2 N1) | 15,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.nv_stecker | F | ENT-134 |  |
| 700.8 | BT-750 Pack-Entgasung | Entgasungsventil mit Entgasungskanal | Vernay VoltaVent (BT-750_vernay_VoltaVent.pdf, S. 3) | 1 | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 8,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.entgasungsventil | H | – | Menge 1 (Opus 2026-11-19). Keine Formangabe (W34 läuft): Stufe H bis W34. |
| 700.9 | BT-760 Heizung | Heizung (Kälte, −20 °C laut REQ-P08) | – | offen | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 0,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | – | - | ENT-135, ENT-136 | Heizung im Fahrzeug-Kühlkreis, keine Pack-Geometrie. Opus bestätigen. |
| 700.10 | BT-770 Gas- und Drucksensor | Gas- und Drucksensor | Amphenol SGX Sensortech TRDU5 (BT-770_amphenol_SGX_TRDU5.pdf, S. 3) | 1 | 0,015 | 0,015 | Annahme (ERW-E2 N1) | 25,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.gassensor | F | ENT-137 |  |
| 700.11 | BT-780 Kennzeichnung | Kennzeichnung (Typschild, HV-Warnung) | – | 1 | offen | offen | offen (keine CAD-Geometrie, keine Akte) | 2,000 €/Stück | Schätzung (Annahme Opus, ERW-KO1) | K | kaufteile.typschild | H | – | Menge 1 (Opus 2026-11-19). Keine Formangabe: Stufe H bis W34. |

## Masse je Baugruppe

| Baugruppe | Masse [kg] |
|---|---|
| BT-100 Zelle | 462,500 |
| BT-200 Zellstack | 17,979 |
| BT-300 Regelung (BMS) | 2,422 |
| BT-400 Verkabelung und Zellverbinder | 3,065 |
| BT-500 Struktur und Gehäuse | 84,352 |
| BT-600 Kühlung | 52,252 |
| BT-700 Zusatzkomponenten | 4,199 |

## Dichten (kg/m3) und neue Annahmen

| Werkstoff | Wert | Herkunft |
|---|---|---|
| Al | 2700 | cad/pack/entwurf/ergebnis_LFP_e2d.json annahmen.A_alu_dichte_kg_m3 |
| Cu | 8960 | sim/elektrik/e2_elektronik/eingaben.json stoffe.rho_Cu_kg_m3 (Opus 2026-11-18) |
| Pad | 2500 | cad/pack/entwurf/ergebnis_LFP_e2d.json annahmen.A_dichte_pad_kg_m3 |
| Zelltraeger | 1200 | cad/pack/entwurf/ergebnis_LFP_e2d.json annahmen.A_dichte_zelltraeger_kg_m3 (PC) |
| Verguss | 300 | cad/pack/entwurf/ergebnis_LFP_e2d.json annahmen.A_dichte_verguss_kg_m3 (PU-Schaum) |
| Stahl | 7850 | cad/baukasten/farben.json werkstoffe.Stahl (Annahme Opus (Handbuchwert)) |
| Kunststoff | 1200 | cad/baukasten/farben.json werkstoffe.Kunststoff (wie A_dichte_zelltraeger_kg_m3 (SL3 G5.1, von Opus bestätigt 2026-11-19)) |
| Dichtung | 1150 | cad/baukasten/farben.json werkstoffe.EPDM (Annahme Opus (Handbuchwert)) |
| Mica | 300 | cad/baukasten/farben.json werkstoffe.Schaum_Zwischenlage (Opus 2026-11-19: Zwischenlage BT-220 als komprimierbares Schaumpad (Quellausgleich, Wärmeschutz), Dichte wie A_dichte_verguss_kg_m3 (PU-Schaum, Annahme); ersetzt Mica-Vollmaterial (41,5 kg, Opus-Fehler)) |

---
*KI-generiert (Claude Sonnet, 2026-11-19), Auftrag G5.1, ergänzt SL3.1 (Auftrag KO2). Entwurf, nicht freigegeben. 56 Positionen. Dokument BAT-DOC-13, Version 0.3.*
