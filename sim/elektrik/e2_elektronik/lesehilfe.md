| Dok.-Nr. | LH-E2 | Version | 0.3 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Lesehilfe Schaltbilder, Bilder und Kabelplan E2 (Elektronik) | Ersteller | Claude Sonnet (KI) | Prüfer | Opus (offen) |

> **KI-generiert** (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben.

## schaltbild_LFP.png und schaltbild_NMC.png
- **Was man sieht:** Den Strompfad der Batterie (rot) und die Messleitungen (blau). Der Strom verlässt die Zellen über die Sicherung, die beiden Schütze (elektrische Schalter) und den Shunt (Messwiderstand für den Strom) zum HV-Stecker. Die Vorladung (Schütz mit Widerstand) lädt vor dem Einschalten die Kondensatoren des Fahrzeugs langsam an.
- **Was die Kästen mit Zahlen bedeuten:** Die Zahlen (Zellzahl, Zahl der Überwachungsplatinen CMU, Sicherungsstrom) stammen aus den Akten ENT-110 bis ENT-143 (Status „vorgeschlagen“, Annahmen aus ERW-E2).
- **Service-Trennstecker:** Teilt die Zellkette in zwei Hälften mit je unter 400 V, damit man sicher am Pack arbeiten kann. Beim LFP-Pack sitzt er vorn in einer Öffnung im Deckel (von oben erreichbar), beim NMC-Pack hinten bei der Schaltbox.
- **Wichtig:** Die Reihenfolge der Bauteile im Strompfad ist nur eine Darstellung, keine Auslegung. Es gibt kein Zielband, weil es ein Schaltbild ist.
- **Nicht dargestellt:** NV-Verdrahtung im Detail (NV-Stecker 26-polig, Belegung offen).

## e2_<V>_gesamt.png, e2_<V>_draufsicht.png, e2_<V>_schnitt.png, e2_<V>_detail.png (V = LFP, NMC)
- **Was man sieht:** Das Pack als graues, teils durchsichtiges Gehäuse. Farbig sind nur die E2-Teile: rot = Überwachungsplatinen (CMU, stehen hochkant an den Stirnseiten), gelb = flache Messleitungen (FPC), magenta = Hochvolt-Leitungen, grün = Schaltbox (Turm hinten, unter der Rücksitzbank), blau = Stecker, Sensor und Service-Trennstecker.
- **Draufsicht:** Deckel und obere Kühlplatte sind weggelassen. Die gelben Linien zeigen, wie die Messleitung von der Platine zu den Zellen läuft. Maßstab 200 mm unten links.
- **Schnitt:** Die gestrichelte rote Linie ist die Höhengrenze 130 mm (Annahme M0). Die blaue Linie ist die Packhöhe mit Turm (210 mm LFP, 204 mm NMC). Die Box steht bewusst über der roten Linie, das erlaubt ENT-144 nur unter der Rücksitzbank.
- **Detail:** Nahaufnahme einer Ecke ohne Deckel. LFP: die Messleitung liegt im schmalen Spalt zwischen Zelle und Rahmen. NMC: sie liegt flach auf den Zellverbindern, der HV-Leiter (magenta) steigt von der Zelle senkrecht nach oben und biegt mit 60 mm Radius ab.
- **Wichtig:** Die Zellen sind Hüllkörper, die Teile vereinfacht. Farben dienen nur der Unterscheidung. LFP: Die Kette läuft in einer Schleife (hinten Plus, vorn die Mitte mit dem Trennstecker, hinten Minus). Plus und Minus gehen als magenta Leitung zur Schaltbox, die Mitte liegt als graue Flachschiene quer vorn auf den Zellen.
- **Nicht dargestellt:** NV-Verdrahtung, Stichleitungen zu jedem Abgriff (NMC nur gerechnet), Anschlusslaschen von den Zellverbindern zu den HV-Leitungen.

## kabelplan_LFP.png, kabelplan_NMC.png
- **Was man sieht:** Von oben auf das Pack: rote Rechtecke = CMU in den Endzonen, gelbe Linien = Messleitung je CMU mit Länge, magenta = HV-Leitung mit Länge, grün = Schaltbox, blau = Trennstecker, feine Linien = Stichleitungen zu den Abgriffen (NMC).
- **Zielband:** keines, weil es ein Plan ist. Zur Einordnung: Erwartung für die Messleitung insgesamt 25–40 m (ERW-E2, Punkt 1), Ergebnis NMC 30.7 m, LFP 11.8 m (kurze Zellreihen). Beim LFP-Plan zeigt die graue Linie vorn den Querverbinder der Mitte.

---
*KI-generiert (Claude Sonnet, 2026-11-18), Entwurf, nicht freigegeben.*
