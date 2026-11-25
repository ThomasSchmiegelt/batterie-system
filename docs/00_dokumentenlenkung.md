| Dok.-Nr. | BAT-DOC-00        | Version   | 0.1              | Status | Entwurf          |
| -------- | ----------------- | --------- | ---------------- | ------ | ---------------- |
| Titel    | Dokumentenlenkung | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Entwurf, nicht vom Menschen freigegeben. Testprojekt „KI im Engineering“, kein Produkt.

## Zweck
Regelt, wie Dokumente in diesem Projekt entstehen, geprüft und freigegeben werden. Prüfbar ist so, wer (Mensch oder welches Modell) was erstellt hat.

## Statusstufen
| Status | Bedeutung | Wer setzt ihn |
|---|---|---|
| Entwurf | erstellt, ungeprüft | Ersteller (Modell oder Mensch) |
| geprüft (KI) | von einem zweiten Agenten an Rohdaten bzw. Quellen geprüft, Prüfung protokolliert | Opus |
| abgeschlossen mit Mängeln | vom Menschen gelesen; Stand einer Schleife abgeschlossen, bekannte Mängel offen und benannt, Arbeit geht weiter (Autor 2026-11-23) | nur der Autor |
| freigegeben | vom Menschen gelesen und angenommen | nur der Autor |

## Nummern
BAT-DOC-NN Projektdokumente · REQ-xxx Anforderungen · ENT-NNN Entscheidungen · RIS-NNN Risiken · B-BAT-NNN Befunde · VER-NNN Nachweise · AEN-NNN Änderungen.
Eine neue Nummer wird vorher mit grep geprüft (keine doppelten).

## Pflichtangaben
Dokumentkopf (Nummer, Version, Status, Ersteller, Prüfer), Hinweis „KI-generiert“ oben und in der Fußzeile, Quellen mit Fundstelle.

## Register
| Nr | Datei | Inhalt |
|---|---|---|
| BAT-DOC-00 | 00_dokumentenlenkung.md | dieses Dokument |
| BAT-DOC-01 | 01_lastenheft.md | Anforderungen des Auftraggebers (Was) |
| BAT-DOC-02 | 02_pflichtenheft.md | Umsetzung (Wie), entsteht mit der Auslegung |
| BAT-DOC-03 | 03_anforderungsverfolgung.md | Anforderung → Nachweis → Status |
| BAT-DOC-04 | 04_entscheidungen.md | Entscheidungen mit Begründung |
| BAT-DOC-05 | 05_risiken_fmea.md | Risiken Produkt und Prozess |
| BAT-DOC-06 | 06_verifikationsplan.md | wie jede Anforderung nachgewiesen wird |
| BAT-DOC-07 | 07_normen_und_vorschriften.md | einschlägige Normen (zu recherchieren) |
| BAT-DOC-08 | 08_ki_einsatz_protokoll.md | welcher Agent was gemacht hat, Prüfung |
| BAT-DOC-09 | 09_aenderungen.md | Änderungsverlauf |
| BAT-DOC-10 | 10_lizenzen_und_quellen.md | Software-Lizenzen, Fremdquellen |
| BAT-DOC-11 | prozess.md | Zusammenarbeit Mensch und KI (Erfahrungsbericht) |
| BAT-DOC-12 | 12_projektmanagement.md | Entscheidungsakten, Bauteilgespräch, Meilensteine |
| BAT-DOC-13 | 13_stueckliste.md | Grobe Stückliste (Baugruppen, Hauptkomponenten), erzeugt von pm/bauteile/stueckliste.py aus Startsatz und Annahmen |
| BAT-DOC-13 | ../video/STORYBOARD.md | Abschlussvideo |
| BAT-DOC-13b | ../video/begleittext_wissen.md | Zweites Abschlussvideo „Batterie und Wissensgraph“ (Begleittext; Video abschluss_wissen.mp4, Auftrag video/AUFTRAG_VIDEO_WISSEN.md), freigegeben (Autor 2026-11-23: „das video ist gut“); Zeitraffer 20 s für LinkedIn: video/abschluss_wissen_linkedin.mp4 |
| BAT-DOC-13c | ../video/begleittext_elektronik.md | Drittes Video „Batterie, Nachverfolgung, Normen, Elektronik“ (REQ-D13; Video elektronik_nachverfolgung.mp4, Auftrag video/AUFTRAG_VIDEO_ELEKTRONIK.md), Entwurf, KI-generiert, Prüfung Opus offen |
| BAT-DOC-14 | ../praesentation/STORYBOARD.md | Unternehmenspräsentation: Folienplan, Bausteine je Vorgang |
| BAT-DOC-15 | 15_foerdermoeglichkeiten.md | Recherche staatliche Förderung (KI/Open Source, Batterie, Wasserstoff), privat und KMU, Voraussetzungen |
| BAT-DOC-16 | 16_ergebnisbilder.md | Ergebnisbilder mit Lesehilfe, erzeugt von pm/plan/bilder.py |
| BAT-DOC-17 | ../bericht/bericht.tex (PDF: ../bericht/bericht.pdf) | Projektbericht Batteriesystem BT-000, Fassung 0.4 (DE, Stand 2026-11-18), Zwischenstand, Entwurf (KI-generiert) |
| BAT-DOC-18 | 18_kosten.md | Herstellkosten |
| BAT-DOC-19 | 19_freigaberunde.md | Freigaberunde (erzeugt von pm.py freigabe) |
| BAT-DOC-20 | 20_regelwerke_vergleich.md | Regelwerke EU/UN, USA, DoD, China im Vergleich |
| BAT-DOC-21 | 21_graph_luecken.md | Lücken aus dem Wissensgraphen (erzeugt) |
| BAT-DOC-22 | 22_qualitaetsnachweis.md | Qualitätsnachweis, Glaubwürdigkeit der Kernergebnisse |
| BAT-DOC-23 | 17_workflow_schleife.md | Workflow Schleife 2 (V-Modell, Tore T0–T6); Dateiname historisch, Nummer 17 ist der Bericht |
| BAT-DOC-24 | 24_gefahrenanalyse_hara.md | Gefahrenanalyse und Risikobewertung (HARA) ISO 26262-3, Sicherheitsziele, FSR (Entwurf) |
| BAT-PM-OPT | ../pm/optimierungen.md | Optimierungsliste (erst konservativ, Bewertung Kosten/Sicherheit/Effizienz) |
| BAT-KR-00 | ../pm/kreativ/METHODE.md | Kreativmethoden mit Paarvergleich (Werkzeug pm/kreativ) |
| BAT-DOC-25 | 25_loesungen_aus_kreativmethoden.md | Lösungen aus Kreativsitzungen und Opus-Abwägung, mit Zuschreibung und verworfenen Alternativen |
| BAT-DOC-26 | 26_modelltest_kolibri.md | Modelltest Kolibri 1: Einsatz, Monitoring, Bewertung |

---
*KI-generiert (Claude Opus, 2026-11-11). Status Entwurf. Freigabe nur durch den Autor.*
