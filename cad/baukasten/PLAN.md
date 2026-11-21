# G5 Geometrie-Überarbeitung: aus der Stückliste erzeugte Modelle

| Nummer | BAT-CAD-G5-PLAN | Version 0.1 | Status: Entwurf | Ersteller: Claude Opus (2026-11-19) | Prüfer: offen (Autor) |
|---|---|---|---|---|---|

Anforderungen: REQ-D11 (Maße nur aus Akten), REQ-D12 (Bauteil begründet Form), REQ-D13/D14 (Video, Präsentation), REQ-P13, REQ-P16.
Auslöser: Autor 2026-11-19: „Überarbeite die geometrie. vielleicht erst die stückliste und anhand der stückliste die Modelle generieren … geometrieerzeugungs code speichern und dokumentieren.“
Vorher: ENT-151 (keine Knautschzone, Seitenrahmen bleibt ein reines Rahmenprofil).

## 1 Grundsatz
**Die Stückliste ist die Quelle der Geometrie.** Jede Position der Stückliste v0.3 (SL3) trägt einen Generator. `montage.py` baut nur, was in der Stückliste steht, und prüft am Ende: Stückzahl CAD = Stückliste, Masse CAD gegen Stückliste, keine Kollisionen. Ein Teil im CAD ohne Stücklistenposition ist ein Fehler, ebenso eine Position ohne Generator (außer Art S oder `detailstufe: "-"`, z. B. Kühlmittel).

Der alte Code (`cad/pack/pack.py`, `pack_e2d.py`, 786 Zeilen am Stück) bleibt unverändert als Referenz liegen. Neu entsteht `cad/baukasten/`.

## 2 Ablauf
| Schritt | Inhalt | Wer | Ausgabe |
|---|---|---|---|
| G5.0 | Plan, Erwartung, Regeln der Stückliste (dieses Dokument) | Opus | PLAN.md, ERWARTUNG.md |
| G5.1 | SL3: Stückliste v0.3 mit Geometriefeldern, fehlende Positionen, Widersprüche nach §4 | Sonnet | pm/bauteile/stueckliste_v3.py, stueckliste_<V>.json v0.3 |
| G5.1p | Prüfung SL3 gegen struktur.json und parameter (BT vorhanden, Nummern, Stückzahlen) | Haiku | cad/baukasten/pruefung_sl3.txt |
| G5.2 | Kern und Montage (Parameterzugriff, Registry, Platzierung, Prüfungen, Export) | Opus | kern.py, montage.py |
| G5.3 | Komplexe Teile: Gehäuse (Wanne, Rahmen mit Kammern, Querträger, Deckel, Unterfahrschutz, Befestigung), Kühlplatte mit Kanälen, Schaltbox mit liegenden Schützen | Opus | teile/gehaeuse.py, teile/kuehlung.py, teile/schaltbox.py |
| G5.4 | Einfache Teile und Kaufteilformen: Zelle (Hülle mit Polen), Verbinder, Pads, Zwischenlagen, BMS/CMU/FPC, Schütz, Pyro, Shunt, Stecker, Ventile, Normteile | Sonnet (nach Vorlage aus G5.2) | teile/zelle.py, teile/verbinder.py, teile/elektronik.py, teile/kaufteile.py, teile/normteile.py |
| G5.5 | Formen der Kaufteile belegen: typische Bauformen und Maße (Schütz, Pyrosicherung, MSD, Druckausgleich, Entgasungsventil, HV-Stecker) | PI W34 | forschung/ergebnis/W34.md |
| G5.6 | Werte aus W31…W33 mit bestandener Zitatprüfung auflisten | Haiku | forschung/W31_W33_bestaetigt.md |
| G5.7 | Montage beider Varianten, Prüfbericht, Opus-Prüfung an den Rohdaten | Sonnet läuft, Opus prüft | cad/baukasten/ausgabe/*, ERGEBNIS.md |
| G5.8 | Renders (Cycles, entrauscht, Farben nach farben.json, keine Transparenz außer Schnitt), Explosionsbild, Katalog | Sonnet | render/, docs/15_geometrie_katalog.md |
| G5.9 | Stückliste, Kosten KO1 und Bericht neu, Folienbaustein | Sonnet | SL/KO neu, Bericht 0.5, praesentation/bausteine/G5.md |

Parallel ab sofort: G5.1 (Sonnet), G5.5 (PI), G5.6 (Haiku), G5.2 (Opus). G5.3/G5.4 starten nach G5.1 und G5.2.

## 3 Aufbau des Codes (cad/baukasten/)
```
kern.py         Parameterzugriff p(bt, merkmal), a(name) für Annahmen; Formhelfer (quader, profil, rundung, bohrung, fase, rohr, gewinde_symbol);
                Registry @teil("gehaeuse.wanne"); Teil-Objekt (name, bt, pos, shape, werkstoff, farbe, masse_kg, masse_quelle)
annahmen.json   Detailmaße ohne eigene Akte (Radien, Kaufteilmaße, Spiele), je Eintrag: wert, einheit, herkunft (ERW-…, Wxx, „Annahme“), varianten
farben.json     Farbe je Werkstoff/Funktion (Al blank, Al eloxiert, Cu, Kunststoff schwarz, HV-orange, Pad grau, Zelle blau/grün, Dichtung)
teile/*.py      ein Modul je Baugruppe; jede Funktion baut ein Teil in lokalen Koordinaten und gibt Liste[Teil] zurück
montage.py      liest stueckliste_<V>.json (SL3) → ruft Generatoren → platziert nach „lage“ → Prüfungen → FCStd (Gruppen je BT), STEP je BT, ergebnis_<V>.json
render.py       Blender (Cycles, Denoise), Ansichten: schräg, Explosion, Schnitt quer, Schaltbox nah
katalog.py      erzeugt docs/15_geometrie_katalog.md aus Registry und Docstrings (erzeugte Datei)
LIESMICH.md     Doku: Datenfluss, Konventionen, „ein neues Teil hinzufügen“ in 5 Schritten
```
**Konventionen:** mm; X Länge (0 = Vorderkante Gehäuse), Y Breite (Mitte = 0), Z Höhe (0 = Unterkante Unterfahrschutz). Maße nur über `p()` (Akten, `pm/bauteile/parameter_<V>.json`) oder `a()` (annahmen.json). Eine Zahl im Code ist nur erlaubt als 0, 1, 2, π oder Zähler. Jede Generatorfunktion hat einen Docstring: BT, Akten, verwendete Parameter und Annahmen, Detailstufe.
**Detailstufen:** K = Konstruktionsstand (Radien, Bohrungen, Fasen, Flansche, fertigungsgerecht), F = Kaufteilform (Grundkörper + Anschlüsse + Befestigung, gerundet), H = Hüllkörper (nur wenn keine Formangabe vorliegt, wird im Prüfbericht gezählt), „-“ = keine Geometrie (Flüssigkeit, außerhalb des Packs).
**Ziel:** H ≤ 5 % der Positionen. Kein sichtbares Teil bleibt ein scharfkantiger Quader.

### 3a Schnittstellen zwischen den Modulen (Opus, 2026-11-19)
- **Reihenfolge** (montage.MODULFOLGE): zelle → schaltbox → verbinder → elektronik → kaufteile → normteile → gehaeuse → kuehlung.
- **ctx.zellen / ctx.quertraeger_x / ctx.felder / ctx.endzone_*:** Zellanordnung, einmal in kern.Ctx.anordnung() (gleich wie G4/E2).
- **ctx.einbau[BT] = [Placement]:** Einbauorte der Kaufteile. Kaufteil-Generatoren bauen lokal (Ursprung = Mitte Befestigungsfläche, +z = Normale, +x = Anschlussrichtung) und setzen mit kern.setze() an jeden Einbauort; Stückzahl = Anzahl Einbauorte. Einbauorte setzen: schaltbox.py (BT-711, 712, 713, 340, 350, 310, 730, 740, 770), gehaeuse.py (BT-570, 750, 780), kuehlung.py (BT-640).
- **ctx.schaltbox:** hv_eingang {Plus, Minus: (x, y, z)}, innenraum (x0, y0, z0, x1, y1, z1), deckel_ausschnitt; verbinder.hv_leitung führt von der Pol-Lasche dorthin.
- **ctx.schneide(shape, [BT], von):** Ausschnitte (z. B. Lasche durch Pad, obere Kühlplatte, Deckel); montage.py schneidet sie am Ende, Masse neu aus Volumen.
- **menge_quelle "CAD":** Positionen, deren Stückzahl aus der Geometrie folgt (Normteile, Dichtungen, FPC-Detail); montage prüft dann nicht, die Stückliste übernimmt die Zahl.

## 4 Regeln für SL3 (Opus-Entscheidungen)
### 4.1 Neue Felder je Position
`geometrie: {generator, detailstufe, lage, farbe}`, `akten: [ENT-…]`, `masse_quelle` (Akte | CAD-Volumen×Dichte | Annahme | Wxx). „masse 0 bei masse_bekannt true“ (Schrauben, Kabelschuhe, Clips, Schrumpfschlauch, Dichtungen, FPC-Detail, Daisy) ist falsch: Masse = CAD-Volumen × Dichte des Werkstoffs, Herkunft „CAD-Volumen“.
### 4.2 Fehlende Positionen → Bauteile (struktur.json ergänzen, Merkmale masse_g, bauform, werkstoff)
| Teil aus dem CAD | Zuordnung |
|---|---|
| Plus-/Minus-Lasche, Stromschienen der Schaltbox | **neu BT-440 Stromschiene** (eltern BT-400) |
| Berührschutz über Verbindern (NMC) | **neu BT-450 Berührschutz** (eltern BT-400) |
| Service-Trennbrücke mit Schrauben (LFP) | BT-720, eigene Position 720.2 |
| Servicedeckel | BT-520, Position 520.2 |
| FPC-Halter, FPC-Detail, Daisy-Chain-Leitung | BT-360, Positionen 360.2/360.3 |
| Zellträger NMC | BT-240 (Variante NMC) |
| Verguss Zellfeld NMC | BT-220 (Variante NMC), eigene Position |
| Gruppenbrücke NMC | BT-420, Position 420.2 |
| Dichtungen (Deckel, Schaltbox, Servicedeckel) | **neu BT-580 Dichtungen** (eltern BT-500) |
| Schrauben, Kabelschuhe, Clips, Schrumpfschlauch | **neu BT-590 Verbindungs- und Normteile** (eltern BT-500), je Art eine Position |
### 4.3 Widersprüche CAD ↔ E1
| Widerspruch | Entscheidung | Begründung |
|---|---|---|
| LFP Zellverbinder CAD 130, E1 249 | **249** (s − 1) + 2 Pol-Laschen; CAD wird nachgezogen | 250 Zellen in Reihe brauchen 249 Verbindungen, unabhängig von der Lage |
| NMC Zellabgriff CAD 868, E1 1736 | **1736** (Plus und Minus je Zelle, 4680 beide Pole oben) | jeder Pol braucht einen Abgriff zum Gruppenverbinder |
| NMC Gruppenverbinder CAD 217 + 216 Brücken, E1 216 | **CAD gilt** (217 Sammelbleche + 216 Brücken); E1-Benennung „Gruppenverbinder“ = Brücke | 217 Gruppen brauchen je ein Sammelblech, dazwischen 216 Übergänge |
| HV-Leitung CAD 0,47/0,34 kg, E1 1,81/1,22 kg | **CAD-Verlegung gilt** (Box hinten, ENT-144, kurze Wege), aber Querschnitt aus E1 übernehmen; Sonnet vergleicht A_CAD mit A_E1 und meldet Abweichung | E1 hat 2 × Packlänge geschätzt, vor ENT-144 |
### 4.4 Überarbeitung E2 (aus 2026-11-18, Opus selbst)
1. Schütze liegend, Schaltbox-Turm ≤ 210 mm (Autor), Ziel Innenhöhe ≤ 90 mm → löst „Box innen 116 > 90“.
2. LFP-Pol mit M8-Flachkopfschraube (ISO 7380-Form) statt Sechskant → Höhe am Pol ≤ 130 mm (M0-Grenze).
3. Kaufteile in Stufe F (Formen aus W33/W34, sonst Annahme mit Vermerk).
4. Farben nach farben.json, Renders ohne Transparenz und ohne Rauschen.

## 5 Abbruch und Rückgabe an Opus
Zurück an Opus geht: neue Annahme ohne Herkunft, Kollision, die sich nicht durch Lage lösen lässt, Masse CAD gegen Stückliste > 3 %, Höhe über M0-Grenze, Widerspruch zu einer Akte.

---
*KI-generiert (Claude Opus, 2026-11-19).*
