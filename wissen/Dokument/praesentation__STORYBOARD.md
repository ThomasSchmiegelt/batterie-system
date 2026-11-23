---
typ: dokument
datei: "praesentation/STORYBOARD.md"
tags: ["dokument", "kopie"]
---
# STORYBOARD

> KI-generiert, erzeugt aus pm/plan/wissensnetz.json – nicht von Hand bearbeiten

- Kopie von `praesentation/STORYBOARD.md` (Quelle im Repo, hier nur Lesekopie)

## Inhalt

| Dok.-Nr. | BAT-DOC-14 | Version | 0.1 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Unternehmenspräsentation: Folienplan | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Plan der Präsentation. Sie wird am Schluss von einem Skript aus den Projektdaten erzeugt, nicht frei geschrieben. Entwurf, nicht freigegeben.

## Zweck
Vorgabe des Autors vom 2026-11-12: „das batterieprojekt muss auch so geplant sein das am ende eine Präsentation mit raus springt. Das ist eine Unternehmenspräsentation“ (Anforderung REQ-D14).
Die Präsentation entsteht nicht am Ende in einem Zug. Jeder Vorgang liefert unterwegs seinen **Folienbaustein**: ein Kernbild mit Zielband, eine Kernaussage in einem Satz und die Quelle der Zahlen. Am Schluss setzt Vorgang B5 die Bausteine zusammen.

## Vorgaben des Autors (offen, Vorgang B0)
| Vorgabe | Vorschlag (nur Vorschlag) |
|---|---|
| Zielgruppe | Geschäftsleitung bzw. Entscheider eines Fahrzeug- oder Zulieferunternehmens |
| Ziel der Präsentation | Entscheidung über den nächsten Schritt (Prototyp, Versuch, Partner) |
| Firmenvorlage | eigene .potx des Unternehmens, sonst neutrale Vorlage |
| Sprache | DE, EN als zweite Fassung |
| Länge | 15 Folien plus Anhang, 20 min |
| Format | PowerPoint (.pptx, bearbeitbar) und PDF |

## Folien (Reihenfolge = Argumentation, nicht Entstehung)
| Nr | Folie | Kernaussage (Art) | Folienbaustein aus Vorgang | Datenquelle |
|---|---|---|---|---|
| 1 | Titel | Projekt, Datum, Autor, Hinweis „KI-generiert“ | – | – |
| 2 | Aufgabe | Was soll das System leisten, für welches Fahrzeug | V1, V2 | docs/01_lastenheft.md, pm/startwerte.json |
| 3 | Kennzahlen auf einen Blick | Energie, Spannung, Leistung, Ladezeit, Masse: Ziel und erreicht | V2, E1, C3, K5 | docs/03_anforderungsverfolgung.md |
| 4 | Lösung im Überblick | Gesamtsystem, Explosionsdarstellung | G4, G5 | cad/pack/*, Bild aus FreeCAD |
| 5 | Zelle | Chemie, Format, Entladekurven mit Zielband | C2, C3, C4 | sim/chemie/ERGEBNIS.md |
| 6 | Pack und Struktur | Cell-to-Pack, Bauraum, Masse | G3, G4 | pm/bauteile/parameter.json |
| 7 | Elektrik und Steuerung | Verschaltung, Schutzkonzept, BMS-Umfang | E1–E4 | sim/elektrik/ |
| 8 | Kühlung beim Schnellladen | Zelltemperatur und Spreizung im Auslegungsfall, mit Grenze | K3–K5, U4 | sim/kuehlung/ |
| 9 | Sicherheit | thermisches Durchgehen, Seitencrash | E2, X1, X2 | sim/mechanik/, BEFUNDE |
| 10 | Nachweisstand | jede Anforderung: erfüllt / offen / Annahme | F1 | docs/03, docs/06 |
| 11 | Risiken | die fünf größten Risiken mit Maßnahme | F1 | docs/05_risiken_fmea.md |
| 12 | Stückliste und Kostentreiber | Hauptkomponenten, Kauf/Eigen | SL2 | docs/13_stueckliste.md |
| 13 | Schutzrechtslage | relevante Patente, ohne rechtliche Bewertung (REQ-D08) | R3 | forschung/PATENTE.md |
| 14 | Arbeitsweise mit KI | Arbeitsteilung, Aufwand, Prüfungen, gefundene Fehler | B1 | docs/08_ki_einsatz_protokoll.md, Ereignisprotokoll |
| 15 | Nächste Schritte | Entscheidungsbedarf, Aufwand und Zeit | B4 | PLAN.md, Netzplan |
| A | Anhang | Annahmen, Quellen, Lizenzen, Softwarestand | – | docs/10, SOFTWARE.md |

## Regeln
- **Jede Zahl** auf einer Folie stammt aus einer Projektdatei (REQ-D01). Der Generator liest sie, niemand tippt sie ab. Annahmen sind als „Annahme“ gekennzeichnet.
- **Jede Grafik** zeigt das beschriftete Zielband bzw. die Grenze. Unbelegte Grenzen heißen „Annahme“.
- **Kennzeichnung:** Titelfolie und Fußzeile jeder Folie „KI-generiert“.
- **Sprache:** für Entscheider, ohne Fachjargon. Fachbegriffe in einem Halbsatz erklärt. Werkzeug- und Modellnamen nur auf Folie 14 und im Anhang.
- **Sprechertext** steht in den Notizen jeder Folie, mit Verweis auf Entscheidungen (ENT-…).
- **Folienbaustein je Vorgang:** Wer einen Vorgang der Spalte „Folienbaustein“ abschließt, legt `praesentation/bausteine/<Vorgang>.md` ab: Kernaussage (1 Satz), Bilddatei, Zahlen mit Quellpfad. B5 prüft vor dem Zusammensetzen, dass alle Bausteine da sind, und meldet fehlende.
- Nach außen geht die Präsentation nur nach Freigabe durch den Autor (REQ-D05).

## Technik
`praesentation/erzeuge.py` (Vorgang B5): liest Bausteine, `docs/03`, `pm/bauteile/parameter.json`, `docs/13`, `docs/08` → `praesentation/unternehmenspraesentation_de.pptx` (python-pptx, Firmenvorlage falls vorhanden) → PDF mit LibreOffice. EN-Fassung aus denselben Daten.
python-pptx ist noch nicht installiert (Installation mit B5, MIT-Lizenz, Eintrag in docs/10).

---
*KI-generiert (Claude Opus, 2026-11-12). Status Entwurf. Freigabe nur durch den Autor.*

