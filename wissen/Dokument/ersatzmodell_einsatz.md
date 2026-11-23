---
typ: dokument
nr: ""
version: ""
status: ""
tags: ["dokument"]
---
# ersatzmodell_einsatz – Ersatzmodelle (Surrogate): wo und wie sie im Batterieprojekt helfen

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/ersatzmodell_einsatz`
- Version: –
- Status: –
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- –

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- –

## Vorgänge, die dieses Dokument nennen
- [[Vorgang/U1|U1]] – ERWARTUNG Ersatzmodell: Zielgröße, Gültigkeitsbereich, Mindestgüte (z. B. Rangkorrelation)

## Inhalt (Kopie aus `docs/ersatzmodell_einsatz.md`)

# Ersatzmodelle (Surrogate): wo und wie sie im Batterieprojekt helfen

> **KI-generiert** (Claude Opus, 2026-11-12). Status: Entwurf, Einschätzung von Opus, nicht freigegeben.
> Grundlage: Erfahrung aus dem Fusionsprojekt (Tragwerks-Ersatzmodell, Turbulenz-Proxy) und PLAN.md. Belege aus der Literatur folgen mit Recherche T07.

## Was ein Ersatzmodell ist

Ein Ersatzmodell ist eine schnelle Näherungsformel, die aus wenigen teuren Rechnungen gelernt wird. Beispiel: 40 Elmer-Läufe zur Kühlplatte, je 20 Minuten. Daraus lernt ein Gauß-Prozess (eine Interpolation, die zu jedem Wert auch ihre Unsicherheit angibt), wie die höchste Zelltemperatur von Durchfluss, Eintrittstemperatur und Ladestrom abhängt. Danach liefert er eine Antwort in Millisekunden statt in 20 Minuten.

Es lohnt sich nur, wenn ein einzelner Lauf teuer ist **und** sehr viele Läufe gebraucht werden, etwa für eine Optimierung oder eine Unsicherheitsrechnung.

## Einschätzung je Arbeitsgebiet

| Gebiet | Kosten je Lauf | Bedarf an Läufen | Nutzen Ersatzmodell | Begründung |
|---|---|---|---|---|
| Kühlung Schnellladen (Elmer, FluidX3D) | Minuten bis Stunden | hoch (Plattenmaß, Durchfluss, Ladeprofil) | **hoch** | teuerster Teil, viele Varianten; Plan U1–U4 |
| Ladeprofil gegen Erwärmung und Lithium-Abscheidung (PyBaMM mit Wärme) | Sekunden bis Minuten | hoch (Optimierung) | mittel | PyBaMM ist schnell genug; Parameterschätzung kann PyBOP direkt (T01 prüft das) |
| Alterung über Jahre (PyBaMM) | Minuten bis Stunden | mittel (Klima, Nutzung) | mittel | lange Simulationen; Ersatzmodell für Lebensdauer über Temperatur und Ladezustand |
| Pack mit vielen Zellen (liionpack) | Minuten | mittel | niedrig bis mittel | erst nach Werkzeugwahl R5 entscheiden |
| Steuerung/BMS im Fahrzeug | Echtzeit nötig | dauernd | **hoch, aber anders** | Das Ersatzschaltbild im BMS ist selbst ein Ersatzmodell des Zellmodells. Es wird aus PyBaMM-Läufen angepasst (T03) |
| Kabel, Verschaltung, Schutz | Millisekunden (Formel) | – | keiner | direkt rechnen |
| Mechanik (Verspannung, Eigenfrequenzen) | Minuten | gering (wenige Varianten) | niedrig | direkt rechnen |

## Regeln (aus dem Fusionsprojekt übernommen)

1. **Erwartung und Mindestgüte vorher festlegen**, z. B. Rangkorrelation ≥ 0,9 gegen zurückgehaltene Läufe. Im Fusionsprojekt erreichte der Turbulenz-Proxy nur 0,59 gegen GX und wurde deshalb nicht zum Vorsortieren verwendet.
2. **Versuchsplan statt Einzelwerten:** Latin Hypercube (gleichmäßig gestreute Stichprobe im Parameterraum). Im Fusionsprojekt waren es 150 Läufe je Anlage.
3. **Nur innerhalb des gelernten Bereichs verwenden**; der Gauß-Prozess zeigt außerhalb große Unsicherheit.
4. **Endwerte immer mit dem vollen Modell bestätigen.** Das Ersatzmodell sortiert nur, die Entscheidung trifft Elmer oder PyBaMM.
5. **Läufe losgelöst und pausierbar**, paketweise gespeichert (Regel „Pausierbar“).

## Nächster Schritt

Recherche T07 (Ersatzmodelle, Versuchsplanung) läuft mit. Erster Einsatz ist im Projektplan nach der Kühlungsrechnung vorgesehen (U1–U4, `pm/plan/`).

