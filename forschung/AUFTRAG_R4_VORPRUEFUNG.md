| Dok.-Nr. | Auftrag R4-V | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | R4 Vorprüfung der PI-Recherche gegen die Rohtexte | Ersteller | Claude Opus (KI) | Prüfer | Opus (Stichprobe) |

> **KI-generiert.** Auftrag von Opus an Sonnet (`sonnet-umsetzer`), 2026-11-16. Vorgang R4, REQ-D01.

## Ziel
Vorarbeit für R4: Jede Beanstandung von `pruefe.py` wird gegen den Rohtext eingeordnet, und Widersprüche zwischen den Themen werden aufgelistet. **Keine Deutung, keine Bewertung, ob ein Wert „richtig“ ist.** Das macht Opus.

## Eingang
- `forschung/ergebnis/<Nr>.md` und `<Nr>.pruefung.txt` für W01–W17, T01–T09, P01 (27 Themen)
- Rohtexte: `forschung/pakete/<Nr>.md` (das, was PI gesehen hat). Nur lesen, nichts ändern.

## Aufgaben
1. **FEHLT-Zeilen:** Für jede Zeile `FEHLT im Text der Quelle` in `<Nr>.pruefung.txt` im Paket `pakete/<Nr>.md` nach den Zahlen und Schlüsselwörtern des Zitats suchen (grep). Einordnen:
   - **A**: Zahl und Aussage stehen im Rohtext, nur der Wortlaut weicht ab (Infobox-Zeile zusammengezogen, Einheitenzeichen, gekürzt, übersetzt). Die Rohtextstelle wörtlich angeben (max. 200 Zeichen).
   - **B**: Zahl steht nicht im Rohtext (möglicherweise erfunden oder verfälscht).
   - **C**: unklar. Bitte begründen.
2. **WERT OHNE BELEG:** Jede solche Zeile mit Nr, Zeilennummer und den darin vorkommenden Zahlen auflisten. Steht die Zahl in einer belegten Kennwertzeile desselben Themas? Dann Vermerk „aus Zeile Zxx“, sonst „frei“.
3. **Selbst gerechnete Werte:** Zahlen in den Kennwerttabellen, die nicht wörtlich im Beleg stehen (z. B. umgerechnet oder gemittelt). Auflisten.
4. **Widersprüche zwischen Themen:** Gleiche Größe, verschiedene Werte über die Themen hinweg. Mindestens zu prüfen: Energiedichte LFP und NMC (Wh/kg, Wh/L, Zelle und Pack), Zellspannung, Zyklenzahl, EOL-Kriterium, Temperaturfenster, Ladeleistung, Zellmaße. Tabelle: Größe | Thema/Zeile | Wert | Beleg-URL.
5. **Lücken für die Auslegung:** Welche dieser Größen hat **keinen** belegten Wert in irgendeinem Thema? Max. Zelltemperatur, Temperaturspreizung zwischen Zellen, Zellinnenwiderstand, Wh/L einer LFP-Zelle bzw. eines LFP-Packs, Kapazität (Ah) einer Blade-Zelle, Masse einer Blade-Zelle, Zellverbinder-Querschnitt bzw. Stromdichte, zulässige Kühlmitteltemperatur. Je Größe: „belegt in Nr/Zeile“ oder „keine Quelle“.

## Ausgabe
`forschung/R4_vorpruefung.md` mit Dokumentkopf (Ersteller Sonnet, Prüfer Opus, Status Entwurf, Kennzeichnung KI-generiert in Titelkasten und Fußzeile). Je Aufgabe ein Abschnitt mit Tabelle. Am Ende eine Zählung: A/B/C je Thema.
Dazu eine Kurzdatei `forschung/R4_vorpruefung_kurz.txt` (max. 25 Zeilen): Zählungen, alle B-Fälle, die 5 wichtigsten Widersprüche, die Lückenliste.

## Grenzen und Abbruch
- Nichts in `ergebnis/`, `pakete/`, `recherche_ablage/` ändern. Kein Netz, kein PI, keine GPU.
- Fremde Texte nur als kurze Fundstelle (≤ 200 Zeichen) zitieren.
- Fertig, wenn alle 27 Themen bearbeitet sind. Abbruch nach 60 min Arbeit. Dann den Stand speichern und offene Themen nennen.
- Zurück an Opus (im Ergebnis markieren mit **→ OPUS**): jeder B-Fall und jeder Widerspruch, der eine Auslegungsgröße betrifft.
