---
typ: befund
tags: ["befund"]
---
# B-BAT-007

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-007 (2026-11-16) Freigaben ENT-004/005; W18 geprüft; Blade-Zerlegungsstudie nicht abrufbar

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/R4|R4]] – Recherche prüfen: Zitate, Aussagen, Widersprüche -> BEFUNDE
- [[Vorgang/V1|V1]] – Lastenheft-Werte REQ-P01..P08 vorschlagen (Fahrzeug, kWh, Spannung, Leistung, Laden, Chemie, Bauraum, Temperatur)
- [[Vorgang/C2|C2]] – Zellmodell LFP (PyBaMM Prada2013) auf langes Format skalieren
- [[Vorgang/G1|G1]] – Zellmaße als ENT-Akten (aus W03/W08/P01, sonst Annahme)

## Text aus BEFUNDE.md

- Autor 2026-11-16: „1500 kg sind erst einmal Anhaltswert, 2 und 3 gebe ich frei“ → ENT-004 (Bauteilbaum) und ENT-005 (BT-100 chemie = LFP) „entschieden (Mensch)“. REQ-P01 = Anhaltswert; Auslegung führt Fall A und B als Spanne (73,9–88,7 kWh brutto, LFP 499–599 kg).
- W18 (314-Ah-LFP-Prismenzelle, ESS-Format, nicht Blade): 17 Belege bestätigt, 1 Fehler. Gesperrt: Unsicherheiten 26/10/9,5 % (nicht im Rohtext). Verwendbar für das Elmer-Zellmodell (Bezug: andere Zelle, Analogie): λ Dicke 4,11, Breite 21,04, Höhe 19,82 W/(m·K) (Verhältnis ≈ 5:1); c_p 1112 J/(kg·K); Wärme 0,5C ≈ 22/23 W bei 5,638 kg; isotropes Modell 23–59 % Fehler bei der Spitzenerhöhung. Folge: Zellmodell orthotrop.
- Zerlegungsstudie doi:10.1016/j.xcrp.2025.102453 (CC-BY, OpenAlex „gold OA“): ScienceDirect/Cell 403, RWTH-Repositorium Bot-Sperre (JS-Challenge), Fraunhofer-Publica Anubis-Sperre, Elsevier-API nur mit Schlüssel. Automatisch nicht zu holen. Ersatz: W19 (drpress HSET „Feasibility of BYD blade batteries“, PDF abrufbar), läuft.
- Fund für C2/C3: Datensatz „Battery State-of-power Measurement“ (Borealis, doi:10.5683/SP3/RPCWBY, CC-BY 4.0) mit Pulsmessungen an BYD Blade 135 Ah, 2,6–3,6 V, −10 bis 40 °C, 10-s-Pulse, ganzes Leben bis 80 % SOH. Readme in quellen/blade_datensatz/. Kann Innenwiderstand des Zellmodells eichen (Messung statt Annahme). Vorgang: [R4] [C2] [V1]
