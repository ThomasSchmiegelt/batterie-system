---
typ: dokument
nr: "BAT-DOC-07"
version: "0.2"
status: "Entwurf"
tags: ["dokument"]
---
# BAT-DOC-07 – Normen und Vorschriften: Anwendbarkeit und Recherche

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Datei: `docs/07_normen_und_vorschriften`
- Version: 0.2
- Status: Entwurf
- Typ: Projektdokument (Dokumentenlenkung [[Dokument/00_dokumentenlenkung]])

## Genannte Anforderungen (Textvorkommen)
- [[Anforderung/REQ-P15|REQ-P15]]
- [[Anforderung/REQ-P17|REQ-P17]]
- [[Anforderung/REQ-P19|REQ-P19]]
- [[Anforderung/REQ-P20|REQ-P20]]

## Genannte Entscheidungen, Befunde, Bauteile (Textvorkommen)
- –

## Vorgänge, die dieses Dokument nennen
- –

## Inhalt (Kopie aus `docs/07_normen_und_vorschriften.md`)

| Dok.-Nr. | BAT-DOC-07 | Version | 0.2 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Normen und Vorschriften: Anwendbarkeit und Recherche | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

Frage des Autors (2026-11-23): „Ist es auch sinnvoll maschinensicherheitsrichtlinien zu integrieren. Wie sieht es mit gesetzlichen anforderungen und anforderungen seitens des vda aus. wenn die nicht verfügbar sind, gibt es was ich china?“

**Wichtig:** Die Spalten „anwendbar“ und „Zugang“ sind eine Einschätzung von Opus aus dem Gedächtnis. Diese Einschätzung ist **nicht belegt**. Grenzwerte werden erst dann zu Anforderungen (REQ-G), wenn die Recherche (W35 ff.) mit bestandener Zitatprüfung vorliegt. Zahlen aus dieser Tabelle werden nicht verwendet.

## 1 Anwendbarkeit (Einschätzung, zu belegen)

| Regelwerk | Thema | anwendbar auf das Pack? | Zugang | Recherche |
|---|---|---|---|---|
| UN-Regelung Nr. 100 (Rev. 3) | Sicherheit des elektrischen Antriebs, Batterie (REESS): Schwingung, Stoß, Quetschung, Feuer, Kurzschluss, Über- und Tiefentladung, Übertemperatur, Ausbreitung | ja, Kern der Typgenehmigung | frei (UNECE) | W35 |
| UN GTR Nr. 20 | weltweite Regel Elektrofahrzeugsicherheit, thermische Ausbreitung | ja, als Bezug | frei (UNECE) | W35 |
| UN-Regelungen Nr. 94, 95, 135 | Frontal-, Seiten- und **Pfahlaufprall** im Fahrzeug, elektrische Sicherheit danach | ja, über das Fahrzeug (Lastfall Pfahl X3) | frei (UNECE) | W36 |
| EU-Batterieverordnung (EU) 2023/1542 | Kennzeichnung, CO₂-Fußabdruck, Batteriepass, Recyclinganteil, Sorgfaltspflicht, Entnehmbarkeit | ja, gesetzlich | frei (EUR-Lex) | W37 |
| UN-Handbuch Prüfungen und Kriterien 38.3 | Transport | ja, für Versand und Muster | frei (UNECE) | W35 |
| GB 38031 (Ausgabe 2025) | Sicherheit von Traktionsbatterien in China, Ausbreitung ohne Feuer und Explosion, Bodenstoß | ja, wenn China Markt ist; sonst als strengere Referenz | Pflichtnormen GB im Netz lesbar (openstd.samr.gov.cn), Download eingeschränkt | W38 |
| GB/T 31467, 31484, 31486 | Pack-Prüfverfahren, Lebensdauer, elektrische Leistung (China, empfohlen) | als Prüfverfahren | teils lesbar | W38 |
| ISO 6469-1/-3, ISO 12405-4, IEC 62660-1/-2/-3 | elektrische Sicherheit, Prüfverfahren für Pack und Zelle | ja, Stand der Technik | **kostenpflichtig** | nur Titel und Umfang |
| ISO 26262, ISO/SAE 21434, UN R155/R156 | funktionale Sicherheit und Cybersicherheit des BMS | ja, sobald BMS ausgelegt wird (REQ-P15) | ISO kostenpflichtig, UN frei | später |
| CISPR 25, ISO 11452-2/-4, ISO 7637-2/-3, ISO 10605, UN R10 | EMV der Elektronik (REQ-P17) | ja, E3 | ISO/IEC kostenpflichtig; Pegel aus Gedächtnis sind Annahmen |
| IEC 60664-1 | Luft- und Kriechstrecken (REQ-P19) | ja, E3 Platinen | kostenpflichtig |
| ISO 16750-1…5, AEC-Q100/Q101/Q200, IPC-A-610, IPC-2152 | Umwelt, Bauteilqualifikation, Fertigung (REQ-P20) | ja, E3 | AEC-Q frei verfügbar |
| Maschinenrichtlinie 2006/42/EG, ab 20.01.2027 Maschinenverordnung (EU) 2023/1230 | Sicherheit von Maschinen | **für das Pack im Pkw nein**: Straßenfahrzeuge mit Typgenehmigung sind ausgenommen (zu belegen, W37). **Ja** für Montageanlage, Prüfstände und Batterien in Maschinen (z. B. Flurförderzeuge) | frei (EUR-Lex) | W37 |
| ISO 12100 | Risikobeurteilung für Maschinen | Methode übertragbar auf die FMEA (BAT-DOC-05) | kostenpflichtig | – |
| VDA-Bände (VDA 6.3, Reifegradabsicherung, AIAG-VDA-FMEA, VDA 2) | Qualitätsprozesse der Lieferkette | ja, für den Prozess, nicht für Grenzwerte | **kostenpflichtig** (VDA QMC) | nur Titel und Gliederung |
| Automotive SPICE (PAM) | Prozessreife Software und System, V-Modell | ja, für den Prozess (BAT-DOC-23) | nach Wissen von Opus kostenfrei bei VDA QMC (zu prüfen) | W39 |
| EU-KI-Verordnung (EU) 2024/1689 | Pflichten beim KI-Einsatz | Prozess, vermutlich kein Hochrisiko-Fall | frei (EUR-Lex) | W37 |

## 2 Vorgehen (Vorschlag Opus)
1. Was frei zugänglich ist, wird belegt und als REQ-G übernommen: UN R100, GTR 20, R135, 2023/1542 und GB 38031. Diese Regelwerke decken die Prüffälle für das Pack weitgehend ab.
2. Bei kostenpflichtigen Normen (ISO, IEC, VDA) werden nur Titel, Umfang und Gliederung erfasst. Der Inhalt kommt in die Akte, wenn der Autor die Norm beschafft. In diesem Fall wird die Anforderung „blockiert (Norm nicht vorhanden)“.
3. Die Maschinenrichtlinie wird nicht als Produktanforderung übernommen. Ein Vermerk in REQ-G hält fest, warum sie nicht anwendbar ist. Die Methode nach ISO 12100 fließt in die FMEA ein.
4. China (GB 38031) dient als Zweitmaßstab. Wo die Regel strenger ist als R100, wird beides ausgewiesen.

---
*KI-generiert (Claude Opus, 2026-11-23). Status Entwurf. Freigabe nur durch den Autor.*

