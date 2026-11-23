---
typ: befund
tags: ["befund"]
---
# B-BAT-019

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-019 (2026-11-17) Schnellladen in den Griff bekommen (K1); Gehäuserecherche W21

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/K1|K1]] – ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung)
- [[Vorgang/M1|M1]] – Mechanik: Zellverspannung, Eigenfrequenzen, Lagerung

## Text aus BEFUNDE.md

- Autor: „Ja das schnellladen müssen wir in den griff bekommen. man läd schwellenartig könnte auch sein, oder nur bestimmte zellen im wechsel, kühlen kann man auch und dann natürlcih begrenzen. mach die renderings neu. bei der gesamtbatterie müssen verstrebungen vorgehalten werden du kannst mal eine recherche machen wie ein batteriegehäuse aufgebaut ist.“
- Opus vorab: Bei fester Ladezeit erzeugt konstanter Strom die wenigste Joulewärme; Stufen +9 %, Puls/Zellen im Wechsel +100 %. In Reihe führen alle Zellen denselben Strom → Wechsel einzelner Zellen nur bei Parallelgruppen und dann wärmer. Spreizung hängt am Wärmeweg: nur beidseitige Kühlung oder kleinerer Strom (LFP ≤ 1,29C, NMC ≤ 1,02C stationär) bringt 5 K. Prüfung durch Rechnung K1.
- Autor (Nachtrag): „bei der Breite sind wir nicht so variabel letzten endes von straßenbreite begrenzt, länge ist etwas einfacher.“ → Breite 1430 mm gilt als fest, Länge darf wachsen. Folge Opus: Querträger quer zur Fahrtrichtung kosten Länge (zulässig); ein Längsträger zwischen den zwei LFP-Zellreihen und breitere Seitenrahmen kosten Breite (Reserve 8 mm) → kritisch, Seitenrahmenbreite aus W22 gegen den angenommenen Rand prüfen.
- Verstrebungen: struktur.json hat BT-530 Querträger, BT-540 Seitenrahmen, BT-550 Unterfahrschutz; W21 soll Werte liefern. Wichtig für Bauraum: Querträger kosten Länge/Breite (G1-Reserve LFP 16/8 mm!). - W21 (12/0): Bauweise CTP, Wanne/Deckel/Rahmen Alu; keine Maße. W22 (Lauf 3, 13/1): Querträger-Profil 54 × 26 mm, Wand 2–3 mm, Oberprofil 19 × 30 mm (US9045030, Pack 2,7 × 1,5 m); Seitenlast ≈ 600 kN bei > 2600 kg, Alu-Strangpress > 20 % leichter als Stahl (US20200148066). **Gesperrt:** SSAB „1,8 mm“ (Zitat zweimal nicht im Text). Seitenrahmenbreite weiter ohne Beleg. Lehre: Suchbegriffe zu breit → Paketgrenze 8000 Zeichen je Quelle schnitt die Maßstellen ab.
- **K1 Ergebnis:** LFP mit Kühlung oben+unten erfüllt REQ-P09 bei 20 min (33,8 °C/4,6 K). Stufen ≈ wirkungslos, Puls/Wechsel schlechter, h/Vorkühlung nur T_max. NMC K3 mit Tab-Scheibe: 20 min 38,9 °C/5,8 K (knapp), 25 min 34,0 °C/3,8 K (erfüllt). Annahme Spalt-k_z 31 W/mK. DEUTUNG.md.
- **M0:** LFP 121 mm hoch, 2024 mm lang (3 Querträger); NMC 111 mm, 1120 Plätze für 868. Akten ENT-082…091 vorgeschlagen (u. a. ENT-088 ersetzt ENT-081, ENT-091 2030 mm ersetzt ENT-013). Offen: Seitencrash über Schweller (Autor), NMC-Zellen gleichmäßig auf Felder verteilen (G4).
- Autor: „ja gehen wir ersteinmal so ins rennen. du musst aber auch fixierung sowie kontaktierung der rundzellen vorsehen“ → ENT-082…091 entschieden (Mensch), Seitencrash über Schweller akzeptiert. **Konflikt (Opus):** 4680 hat Plus- und Minuspol oben (Minus am Becherrand) → Zellverbinder liegen oben, wo K1/ENT-088 die obere Kühlplatte annimmt. Kühlung oben nur über isolierte Verbinderebene oder Kühlung unten + Seite. Recherche P14/W24 läuft.
Vorgang: [K1] [M1]
