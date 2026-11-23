---
typ: befund
tags: ["befund"]
---
# B-BAT-020

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

B-BAT-020 (2026-11-17) Fixierung, Kontaktierung, Kühlung der 4680 nach Herstellervergleich

Quelle: [[Dokument/BEFUNDE]]

## Vorgänge
- [[Vorgang/R3|R3]] – Patente P01-P10
- [[Vorgang/G4|G4]] – Pack: Zellanordnung, Querträger, Kühlplatte, Deckel
- [[Vorgang/K1|K1]] – ERWARTUNG Kühlung Schnellladen (max. Zelltemperatur, Spreizung)

## Text aus BEFUNDE.md

- Autor: „du musst aber auch fixierung sowie kontaktierung der rundzellen vorsehen“; „schau mal erst wie andere hersteller das ... machen“; „verteile die rechereche“. PI W24 (24/0), W25 (10/0), W26 (14/0), P14 leer; Sonnet Quellensuche; Haiku Tabelle forschung/vergleich_rundzellen.md.
- Belegt: einseitige Kontaktierung (Lucid, Rivian, Tesla), Al-Verbinder (Lucid), Verguss zwischen Zelle und Kühlung (Tesla), Ableiterscheiben Al 400 µm / Cu 260 µm, DCIR 4680 5,4–7 mΩ (bestätigt K0-Annahme 6,5).
- **Widerspruch:** Becherwand 4680 laut W24/W25 (batterydesign.net, Sammelseite) 0,5–0,6 mm, ENT-029 0,4 mm aus W20 (eigene Zerlegung, Primärquelle). Opus: ENT-029 bleibt, W24-Wert als Band in der Akte nennen; Unterschied evtl. Zellgeneration.
- Nicht belegt: wo Hersteller Rundzellen kühlen (Seite/Boden/oben) – nur Vorab-Websuche (Tesla Seitenbänder), nicht zitatgeprüft.
- Vorschlag ENT-092…095 [NMC]: Träger unten + Verguss, Al-Verbinder einseitig oben, Laserschweißen (Annahme), isolierendes Pad zwischen Verbindern und oberer Kühlplatte. K1b (h_eff 214 oben): NMC 20 min 42,8 °C/8,1 K ✗, 25 min 36,8/5,4 ✗ (knapp), 30 min 33,3/3,8 ✓; 25 min erfüllt bei Bedeckung φ ≥ 0,7. Erwartung Opus 1–3 K zu hoch (Pad-Widerstand überschätzt bzw. Verguss/Boden trägt mehr). - Autor: „30 minuten“ → REQ-P05: NMC-4680 schnellladen 10→80 % in 30 min (LFP 20 min). Erster bewusster Spezifikationsunterschied der Varianten. Verbinder schmal genügt (φ 0,5), Auslegung E.
- **G4 Pack-CAD (Entwurf):** 0 Kollisionen; LFP 611 kg (C0b 616), NMC 480 kg (C0b 411): Packfaktor 0,64 statt 0,75, weil NMC das auf LFP ausgelegte Gehäuse (2030 mm), zwei Kühlplatten und Verguss trägt. Folge Opus: „gleiche Spezifikation“ kostet NMC ≈ 70 kg; NMC-eigenes Gehäuse (1950 mm) wäre leichter – Autor: „2 kürzer und eigenes gehäuse“ → ENT-102 (LFP 2030), ENT-103 (NMC 1950); ENT-096…101 freigegeben („1 ja“). G4 neu: NMC 1950 mm → 473 kg (−7 kg, Opus-Schätzung 15–25 kg zu hoch: Länge betraf nur Wanne/Platten-Enden). Restlicher Mehrbedarf gegen C0b: zwei Kühlplatten, Verguss, Träger.
- Werkzeug: Monitor-/Warte-Befehle mit `pgrep -f "…lauf.sh…"` fanden den eigenen Befehl (Sonnet bei W26 bemerkt, Opus vorher bei W-Läufen) → Muster mit `^bash` bzw. `[l]auf.sh` verankern.
- Bericht 0.2 (43 S.) nutzt ergebnis.json; Rundung K1b P3 dort 36,8/5,4 (abgeschnitten) statt 36,9/5,5.
- Autor: „Wie setzten a und b auf ok. Bei B weiß ich auch nichts besseres.“ → alle 67 vorgeschlagenen Akten entschieden (Mensch); 103/103 entschieden. Abgeleitete Werte (ENT-015/018/020/032/038/044/074) und unsichere Lesarten (ENT-028/029/037/043/062/068) bleiben im Text als solche benannt.
Vorgang: [G4] [K1]
