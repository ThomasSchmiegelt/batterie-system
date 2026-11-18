| Dok.-Nr. | ERG-X1b | Version | 0.1 | Status | geprüft (KI) |
|---|---|---|---|---|---|
| Titel | Ergebnis X1b/X2: Knautschzone, CalculiX abgebrochen, OpenCourant LFP w15/20/30 und NMC w20 | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert.** Claude Sonnet, 2026-11-18. Entwurf, nicht freigegeben. Zahlen aus `ergebnis_oc.json` (Fall `LFP_w20`, Läufe `lauf_oc/LFP_w20/`) und `ergebnis.json` (CalculiX, `laeufe.<V>_w<w>`). Erwartung: `ERWARTUNG.md` mit Nachtrag 1. Pfahl Ø254, 1500 kg, 5 kJ (v = 2,582 m/s) und Werkstoff sind **Annahmen** aus ERW-X1/X1b.

## Stand
- **CalculiX (X1b quasistatisch):** alle fünf Läufe divergierten (`ergebnis.json`, `fertig: false`), Pfahlweg bei Abbruch LFP w15 5,39 mm, LFP w20 3,01 mm, LFP w30 2,43 mm, NMC w15 5,39 mm, NMC w20 1,73 mm. Nur als Gegenprüfung der Anfangssteifigkeit brauchbar. `auswerten.py` ist repariert und wertet Teilläufe aus.
- **OpenCourant (explizit), Probe LFP w20: gelaufen, Normalende.** 10 Abschnitte à 5 ms (Wiederaufsetzpunkt je Abschnitt), 380 709 Zyklen, Laufzeit 750 s mit 4 Threads (`laufzeit_s_summe`). Auf Freigabe von Opus wurden danach LFP w15, LFP w30 und NMC w20 gerechnet (alle mit Normalende, je 10 Abschnitte, Energiefehler max 0,0065 bis 0,0095 %).

## Probe LFP w20 (ergebnis_oc.json, `LFP_w20`)
| Größe | Wert |
|---|---|
| Energiebilanz | Summe 5000,0 J am Anfang, 4999,64 J am Ende, Fehler max 0,0072 % (`energiefehler_proz_max`), Grenze 5 %: erfüllt |
| Hourglass | 0,0 J (`hourglass_max_J`). Das Schalenelement (Ishell 24) meldet keine Hourglass-Energie, das heißt nicht, dass sie null ist. Grenze 10 %: formal erfüllt |
| Zeitschritt | min 1,296e-4 ms (`zeitschritt_min_ms`), Kontaktenergie max 0,44 J |
| Eindringung max | 50,1 mm bei 36,0 ms (`eindringung_max_mm`, `zeit_max_ms`); Pfahl kommt zum Stillstand |
| Kraft | max 131,7 kN, mittlere Kraft bis w (20 mm) 80,1 kN (`kraft_max_kN`, `kraft_mittel_bis_w_kN`). Erwartung 60 bis 120 kN: im Band |
| Zellberührung | Spalt 1 mm (Zellverbinder): Eindringung 1,6 mm, 34,5 kN, **35 J**. Spalt 4 mm (Zellkörper): Eindringung 8,3 mm, 81,5 kN, **466 J** (`zellberuehrung`) |
| Innenwand Mitte | 26,3 mm am Ende (`innenwand_dy_max_mm_TH`), größter Wert über alle Innenknoten 39,8 mm (`..._Anim`) |
| PEEQ | Knautschprofil max 68,6 %, Rahmen max 13,4 % (Bruchdehnung 10 %, Annahme) |
| Gegenprüfung CalculiX | Kraft bei 2 mm Eindringung: OpenCourant 39,9 kN gegen CalculiX 37,1 kN, Abweichung +7,6 % (Grenze 30 %: erfüllt) |
| Energieverlust im Pack | 2,35 % (`energieverlust_proz`, aus `energieverlust.json`, Annahme Energie proportional zur Zelllänge) |

Der Wiederaufsetzpunkt wurde geprüft: Ein einzelner Lauf und derselbe Lauf in 10 Abschnitten liefern bei 2,5, 5, 10, 15, 20, 30, 35, 40 ms dieselbe Pfahlposition und innere Energie (Abweichung 0 bei den gezeigten Stellen, Vergleich mit der ersten Probe `/home/cae/cae_projekte/batterie/x2_lauf/probe1_alt/X2T01`).

## Trend über w (ergebnis_oc.json, `zellberuehrung` und `zerlegung_bei_zellberuehrung`, Bild `energie_bis_zellberuehrung_ueber_w.png`)
| Fall | Energie bei Spalt 1 mm | Energie bei Spalt 4 mm | Eindringung bei 4 mm | max. Eindringung bei 5 kJ | Kraft mittel bis w / Spitze | Kraft bei 2 mm gegen CalculiX |
|---|---|---|---|---|---|---|
| LFP w15 | 45 J | 416 J | 7,1 mm | 49,7 mm | 77 / 138 kN | +6,7 % |
| LFP w20 | 46 J | 455 J | 8,1 mm | 50,1 mm | 80 / 132 kN | +7,6 % |
| LFP w30 | 47 J | 568 J | 11,5 mm | 52,1 mm | 75 / 134 kN | +14,0 % |
| NMC w20 | 58 J | 523 J | 9,0 mm | 49,4 mm | 80 / 135 kN | +13,5 % |
(Energie und Eindringung aus `zerlegung_bei_zellberuehrung`, bestimmt an allen Animationsbildern; die TH-Zeile der Probe aus dem Abschnitt oben nutzt einen einzelnen Knoten und weicht deshalb geringfügig ab, 466 gegen 455 J.) Hinweis: Die Spalte „4 mm“ ist der LFP-Zellkörper-Spalt; für NMC (Spalt 0 mm gerade Reihen) ist sie nur ein Vergleichsmaß.
- **Trend:** w von 15 auf 30 mm erhöht die Energie bis Zellberührung (4 mm) von 416 auf 568 J, also um 37 %. Das Ziel 5 kJ liegt beim Zehnfachen. Eine lineare Fortschreibung erreicht 5 kJ erst bei w von mehreren Hundert Millimetern (Schlussfolgerung, nicht gerechnet).
- **Herkunft der Innenwand-Verschiebung (Spalt 4 mm):** Von der Verschiebung der Profil-Außenwand (7,8 bis 11,8 mm) entfallen bei LFP w15 4,0 mm (52 %), w20 4,0 mm (45 %), w30 4,0 mm (34 %) auf die Verschiebung der Innenwand selbst, also des ganzen Rahmenquerschnitts nach innen. Nur 0,2 bis 0,4 mm (NMC 1,3 mm) kommen aus dem Stauchen der Rahmenkammern, der Rest ist Stauchung des Profils (3,4, 4,5, 7,5 mm). Der Innenwandknoten 150 mm neben der Pfahlmitte bewegt sich um etwa die Hälfte (1,9 bis 2,2 mm) gegenüber 4 mm in der Mitte. Das stützt die Vermutung globaler Rahmenbiegung zwischen den Querträgern: Der Rahmen weicht als Ganzes nach innen aus, während das Profil zusammengedrückt wird. Mit größerem w wächst der Anteil Profilstauchung, der Anteil der Rahmenbewegung sinkt, absolut bleibt er bei 4 mm (das ist der Spalt, an dem gemessen wird).
- Gemessen ist Verschiebung an drei Knoten (Pfahlmitte Innenwand, Rahmenaußenwand, Profil-Außenwand) plus einem Innenwandknoten 150 mm daneben, nicht eine Zerlegung in starre Verschiebung und Biegung. Eine saubere Trennung bräuchte den Verlauf der Innenwand über x (Frames liegen in lauf_oc/<Fall>/X2A*.gz).
- Die Gegenprüfung gegen CalculiX liegt bei w30 und NMC w20 bei 14 und 13,5 % (Grenze 30 %).

## Abgleich mit der Erwartung
- Kraftband 60 bis 120 kN: **erfüllt** (80 kN mittel bis w, 131 kN Spitze am Ende).
- Eindringung bei 5 kJ kleiner als w, keine Zellberührung: **VERFEHLT.** Der Pfahl dringt 50 mm ein, das ist mehr als w = 20 mm plus Rahmenbreite 30 mm. Die Innenwand bewegt sich schon ab etwa 1,6 mm Eindringung, weil Profil und Rahmen gemeinsam nachgeben, und erreicht den Zellkörper-Spalt bei 0,47 kJ, nicht erst bei 5 kJ. Das Ziel (Zellberührung erst ab ≥ 5 kJ) wird um den Faktor 10 verfehlt.
- Energiebilanz, Hourglass, Laufzeit < 2 h: erfüllt.
- w 30: Eindringung bei 5 kJ 52 mm, Zellkörper-Spalt bei 568 J: Erwartung ebenfalls verfehlt. Das Ziel „ab w ≈ 20 keine Zellberührung bei 5 kJ“ ist für w 15, 20 und 30 verfehlt.

## Modellgrenzen (Opus prüfen)
1. Pfahl als Starrwand (Zylinder Ø254, Höhe über den ganzen Rahmen) greift an den Knoten der Mittelfläche der Außenwand: erste Berührung nach 1,5 mm Pfahlweg (0,5 mm Anfangsabstand plus halbe Wanddicke 1 mm plus Rest). Eindringung ist ab erster Knotenberührung gezählt.
2. Wandstärken 2 mm Profil, 2,5 mm Rahmen als Schalen (linear, QEPH, 4 mm Netz im Pfahlbereich). Selbstkontakt TYPE7 auf dem Profil, Gap 1,0 mm. Rahmen (außer Profil) ohne Selbstkontakt: bei starker Faltung des Rahmens nicht verlässlich.
3. Werkstoff bilinear (260 MPa, ab 10 % PEEQ 310 MPa, danach flach), kein Versagen, keine Dehnrate. PEEQ 68,6 % im Profil bedeutet in Wirklichkeit Rissbildung, im Modell nicht abgebildet.
4. Einspannung wie X1 (Rahmenenden, Querträger-Ende fest), Boden nur als 300-mm-Streifen, keine Zellen, keine Kühlplatte, keine Deckel.
5. Kraft aus der Ableitung der Wandimpuls-Ausgabe, geglättet 1 ms. Die Anzeige der Zellberührung (Innenwand-Mitte) verwendet einen Knoten, das Maximum über alle Innenknoten (Animationsdateien, Abstand 0,5 ms) liegt höher.
6. Die Restart-Zwischendateien `/RFILE` (I/J) lassen sich in dieser Version nicht lesen (Speicherzugriffsfehler). Wiederaufsetzpunkte entstehen deshalb als 10 normal beendete Abschnitte (`X2_<k>_0001.rst`). Das ist ein Werkzeugbefund für BEFUNDE.md.

## Befund Werkzeug: /RFILE-Zwischendateien nicht lesbar (OpenCourant latest-20261011)
Mit `/RFILE/2` und Zyklusabstand 2000 bis 5000 schreibt die Engine `X2_0001_0001_I.rst` und `_J.rst`. Die Fortsetzung (`engine -i X2_0002.rad`, Datei nach `X2_0001_0001.rst` kopiert, dazu Varianten mit `/RFILE`-Karte „0 1“, „1 0“, „0 2“ und mit nur `/RUN`) endet jedes Mal mit Speicherzugriffsfehler und der Meldung „Error opening file:“ (Engine öffnet die Datei, dann SIGSEGV; Nachweis mit strace). Die Option `-r` gibt es nicht. Ohne `/RFILE` schreibt ein normal beendeter Lauf `X2_<k>_0001.rst`, und die Fortsetzung damit funktioniert (Test an einem 2-ms-Lauf, danach Probe in 10 Abschnitten gegen Einzellauf: 0 Abweichung). Maßnahme: Wiederaufsetzpunkte als Abschnitte (`x2.py`, `lauf_oc.sh`). Zwischenstände innerhalb eines Abschnitts gehen bei Absturz verloren (höchstens 1 bis 2 min). Offen: ob die I/J-Dateien eine andere Fortsetzungskarte brauchen; nicht weiter untersucht (keine Referenz im Repo gefunden). Gehört nach BEFUNDE.md.

## Offene Fragen an Opus
- Verfehlt-Fall in allen vier Läufen: Auslegung ändern (Rahmenbiegung zwischen den Querträgern, Profilform, Wandstärke, Weg) oder Ziel prüfen?
- Starrwand-Offset: Soll die Wandberührung an der Außenfläche (Dicke berücksichtigen) statt an der Mittelfläche liegen? Das verschiebt die Eindringung um 1 mm.

Dateien: `energie_bis_zellberuehrung_ueber_w.png`, `x2.py` (Netz und Deck), `lauf_oc.sh`, `neustart.sh` (OpenCourant), `neustart_ccx.sh`, `auswerten_oc.py`, `auswerten.py` (CalculiX), `energieverlust.py`, `ergebnis_oc.json`, `kraft_eindringung_oc.png`, `energiebilanz_oc.png`, `verformung_oc_LFP_w20.png`, `lesehilfe.md`, `LIESMICH_NEUSTART.md`.

*KI-generiert, Entwurf. Dokument ERG-X1b, Version 0.1.*

## Prüfung Opus (2026-11-18, am Deck x2.py und an ergebnis_oc.json)
| Punkt | Befund | Wirkung auf die Aussage |
|---|---|---|
| Pfahl | /RWALL/CYL mit Masse 1500 kg und v0, Kontakt auf Profil und Rahmen | richtig |
| Elemente | Schale Ishell 24 (QEPH), Dreiecke Ish3n 2, /DT 0,9 ohne Massenskalierung, Energiefehler 0,007 % | richtig |
| Selbstkontakt | TYPE7 nur im Knautschprofil; Rahmenkammern ohne Selbstkontakt, sie stauchen nur 0,2–1,3 mm | ausreichend |
| Randbedingungen | Rahmenenden und Streifenende bei y = 300 voll eingespannt | eher zu steif → reale Energie bis zur Zellberührung **kleiner** |
| Werkstoff | bilinear ohne Versagen, PEEQ im Profil 69 % gegen 10 % Bruchdehnung | Profil würde reißen → reale Energie **kleiner** |
| Zellen | nicht modelliert, Kriterium ist die Berührung | richtig für die Frage |
| Hauptunsicherheit | 5 kJ Restenergie und Pfahl Ø 254 sind Annahmen (W30 ohne Normwerte) | ändert den Maßstab, nicht den Trend über w |
**Urteil:** Die Studie ist methodisch tragfähig für den Variantenvergleich. Die beiden Vereinfachungen (Einspannung, kein Versagen) wirken in dieselbe Richtung, die reale Reserve ist also eher noch kleiner. Die Empfehlung „keine Knautschzone im Pack, der Schweller trägt“ ist damit **robust**. Kein Nachweis: Ausschnittmodell, ohne Fahrzeug. Status: geprüft (KI).
