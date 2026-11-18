| Dok.-Nr. | Auftrag X1b/X2-OC | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Knautschzone explizit mit OpenCourant | Ersteller | Claude Opus (KI) | Prüfer | Opus (Rohdaten) |

> KI-generiert, Opus → Sonnet, 2026-11-18. Grundlage ist ERWARTUNG.md Nachtrag 1. AGENTS.md → Rechnen → Wiederaufsetzpunkt gilt.
1. Netz aus x1b.py übernehmen (Schalen, w-Varianten), Starter-Deck mit Selbst- und Pfahlkontakt (Kontakttyp der Wahl, z. B. TYPE7/TYPE24), Werkstoff 6082 T6 bilinear wie ERW-X1, Pfahl starr 1500 kg mit v aus 5 kJ. Restart-Dateien einschalten.
2. Zuerst LFP w20 als Probe: Energiebilanz, Hourglass < 10 %, Zeitschritt, Laufzeit. Erst danach die übrigen (LFP 15/30, NMC 20).
3. `neustart.sh` und `LIESMICH_NEUSTART.md` auf OpenCourant umstellen (alte CalculiX-Fassung als `neustart_ccx.sh` behalten), Scope `hermes-batterie-x2-<fall>`, pausierbar.
4. Auswertung: Eindringung–Zeit, Kraft–Eindringung, Innenwand-Verschiebung gegen Spalt, Energie. Gegenprüfung CalculiX: Kraft bei 2 mm aus den abgebrochenen ccx-Läufen. Bilder mit Zielband und Lesehilfe. ERGEBNIS.md, Baustein X1b.
5. Vorher `auswerten.py` (CalculiX) so reparieren, dass Teilläufe bis zum Abbruch ausgewertet werden.
Abbruch → OPUS: Energiebilanz > 5 %, Probe läuft länger als 2 h, Verfehlt-Fall. Rückgabe höchstens 5 Zeilen.
