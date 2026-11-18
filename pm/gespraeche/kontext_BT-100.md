# Kontext für das Bauteilgespräch: BT-100 Zelle

KI-generiert von pm.py aus Projektdateien (nur eigene Dokumente).

## Ich bin
Zelle (BT-100). Aufgabe: speichert Energie (Chemie, Elektroden, Gehäuse, Pole, Ventil). Teil von: BT-000. Meine Teile: –.

## Meine Merkmale (Wert und entscheidende Akte)
- chemie: noch nicht entschieden  (–)
- laenge_mm: noch nicht entschieden  (–)
- breite_mm: noch nicht entschieden  (–)
- dicke_mm: noch nicht entschieden  (–)
- kapazitaet_Ah: noch nicht entschieden  (–)

## Anforderungen an mich (Lastenheft)
| REQ-P06 | Zellchemie | offen (LFP wie Beispiel?) | Autor | Muss | offen |
| REQ-P10 | Lebensdauer (Zyklen, Jahre, Restkapazität) | offen | Autor | Soll | offen |
| REQ-P11 | Sicherheit: keine Ausbreitung des thermischen Durchgehens bzw. Warnzeit nach Norm | nach Norm (BAT-DOC-07) | Norm | Muss | offen |

## Entscheidungen, die mich betreffen (vollständig)
### ENT-002 Zellmodell mit PyBaMM (2026-11-11, vorgeschlagen, Opus)
Merkmal: - = None ; Anforderungen: REQ-P06, REQ-P10; Belege: –
## Frage
Zellmodell mit PyBaMM?
## Alternativen
| Alternative | dafür | dagegen |
|---|---|---|
| eigenes Ersatzschaltbild | schnell | keine Elektrochemie, keine Alterung |
## Entscheidung und Begründung
Quelloffen, validierte Parametersätze inklusive LFP (Prada2013); Probelauf auf diesem Rechner ok.
## Folgen
siehe docs/05_risiken_fmea.md

