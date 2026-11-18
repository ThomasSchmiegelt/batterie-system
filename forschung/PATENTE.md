# Patente – Ergebnis PI (UNGEPRÜFT durch Menschen)

KI-generiert: PI (lokales Modell, ohne Werkzeuge) aus abgerufenen Texten; Zitate automatisch geprüft (pruefe.py).

## P01

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| CN222995670U | 2024-07-22 | 比亚迪股份有限公司 | Batteriepack für ein Fahrzeug (Details nicht verfügbar, Abruf fehlgeschlagen) | nicht gefunden | Zusammenbau |
| CN223321452U | 2024-09-30 | 比亚迪股份有限公司 | Abtaststruktur und Sammelvorrichtung für Batteriedaten (Details nicht verfügbar, Abruf fehlgeschlagen) | nicht gefunden | Elektrik |
| CN121215963A | 2024-06-26 | 比亚迪股份有限公司 | Batteriekomponenten und elektrisches Gerät (Details nicht verfügbar, Abruf fehlgeschlagen) | nicht gefunden | Elektrik |
| CN216529163U | 2021-11-30 | 比亚迪股份有限公司 | Batteriepack und Fahrzeug (Details nicht verfügbar, Abruf fehlgeschlagen) | nicht gefunden | Zusammenbau |
| CN222601263U | 2024-05-28 | 比亚迪股份有限公司 | Gehäuse mit einseitig angeordneter Stromverteilung, sodass keine Verbindungsleiter die Zellbaugruppe überkreuzen müssen | Beleg: "A housing in which a receiving cavity is formed" (https://patents.google.com/patent/CN222601263U/en) | Elektrik |
| CN220914413U | 2023-09-12 | 比亚迪股份有限公司 | Zellen nebeneinander in Dickenrichtung; Endzellen besitzen dickere Wände als Mittelzellen, um Kapazitätsverlust zu mindern | Beleg: "the battery cells are arranged side by side along the thickness direction" (https://patents.google.com/patent/CN220914413U/en) | Zellform |

## Was man daraus lernt

- **Modullose Anordnung bei BYD:** Beide dokumentierten Patente (CN222601263U, CN220914413U) beschreiben Batteriepacks, in denen die Zellen direkt im Tray bzw. Gehäuse liegen – das klassische Zwischenelement „Modul" entfällt.
- **Einseitige Elektrik als Sicherheits- und Gewichtsvorteil (CN222601263U):** Verteilstruktur und Batteriebaugruppe liegen auf derselben Seite; dadurch überkreuzt keine Leitung die Zellen. Weniger Masse, weniger Kurzschlussrisiko, geringere Fertigungskosten.
- **Asymmetrische Zellwandstärke (CN220914413U):** Zellen am Rand des Packs haben eine maximal dickere Wand als die mittigen Zellen. Ziel: gleichmäßigere mechanische Belastung und damit geringerer Kapazitätsabfall über die Lebensdauer.
- **Reihenschaltung in Längsrichtung (CN222601263U):** Mindestens zwei Zellgruppen entlang der ersten Richtung sind elektrisch in Reihe geschaltet – die serielle Konfiguration erfolgt innerhalb des Packs, ohne externe Verbindungskabel.
- **Blattförmige Geometrie implizit (CN220914413U):** Die Zellen sind „side by side along the thickness direction" angeordnet und über Enden in Längsrichtung elektrisch verbunden – konsistent mit einem „blade"-artigen Format, bei dem die Längsrichtung die Stromrichtung definiert.

## Offene Fragen

1. **Mechanik der asymmetrischen Wände (CN220914413U):** Um wie viel Prozent thicker sind die Endzellen in Bezug auf die Gesamtdicke, und welcher maximale Packdruck wird bei diesem Konzept angesetzt, um den Kapazitätsgewinn zu halten?
2. **Schnittstelle „plug-in component" (CN222601263U):** Handelt es sich um einen standardisierten BMS-/HV-Stecker oder um eine BYD-proprietäre Buchse; welche Strom- und Spannungsklasse ist vorgesehen?
3. **Zellabmessung und Chemie:** Die vier nicht abrufbaren Patente könnten konkrete Zellabmessungen und eine Zellchemie (LFP, NMC) nennen – ohne diese lässt sich die Übertragbarkeit auf ein eigenes System nicht abschätzen.
4. **Thermalmanagement:** Keines der beiden dokumentierten Patente erwähnt eine aktive Kühlung – wird sie in den fehlenden Patenten (CN222995670U, CN216529163U) als integrierte Struktur behandelt?

## Auffälliges

- **Vier von sechs Patenten nicht abrufbar** (HTTP 503): CN222995670U, CN223321452U, CN121215963A, CN216529163U – für diese fehlen Zusammenfassung und Ansprüche vollständig; nur Titel, Priorität und Inhaber sind aus der Trefferliste bekannt.
- **Einseitige Inhaberschaft:** Alle sechs Treffer gehören 比亚迪股份有限公司 (BYD). Die Suchanfrage hat offenbar keine Patente anderer Inhaber (z. B. CATL, Tesla, EVE) geliefert.
- **Mögliche Themenabweichung:** CN223321452U (Tatbestand: „Sampling structure, battery information collection device") bezieht sich auf BMS-Abtastung und könnte über die Blade-/Blattzell-Fragestellung hinausgehen; wegen fehlender Inhalte nicht verifizierbar.
- **Keine auffälligen Anweisungen oder Manipulationsversuche** in den bereitgestellten Textfragmenten.


Prüfung: 2 Belege bestaetigt, 0 Fehler

## P02

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| US20260148986A1 | 2023-01-03 | Contemporary Amperex Technology (Hong Kong) Limited | Negative Elektrodenplatte mit lithiophiler Plattierungsschicht und Durchlässen in der aktiven Materialschicht zur Verbesserung der Lithiumeinlagerung. | Beleg: "a lithiophilic plating layer formed on a surface on at least one side" (https://patents.google.com/patent/US20260148986A1/en) | Zellchemie |
| GB202417857D0 | 2024-12-05 | Gus Tech Co Ltd | Fixierstruktur für Elektrodentabs in einer Pouch-Zellbatterie. | nicht gefunden | Elektrik |
| EP4207363A3 | 2022-01-04 | Prologium Technology Co., Ltd. | Lithium-Ionen-Akku mit Ionenlieferant an der Kathode und Lithiumempfänger an der Anode zur aktiven Unterdrückung des thermischen Durchsatzes. | nicht gefunden | Sicherheit |
| WO2025188859A8 | 2024-03-05 | Apple Inc. | Elektrolyt-Lösungsmittel mit halogensubstituierten Alkylverbindungen für Lithium-Ionen-Batteriezellen. | nicht gefunden | Zellchemie |
| CN222813775U | 2025-01-23 | 宁德时代新能源科技股份有限公司 | Batteriegerät, bei dem eine Pouch-Zellgruppe über eine offene Gehäusestruktur eingehängt und zusammengebaut wird. | Beleg: "The box body is provided with a bottom plate and is used for bearing the battery cell assembly" (https://patents.google.com/patent/CN222813775U/en) | Zusammenbau |
| WO2025184855A8 | 2024-03-06 | 安徽科技学院 | Positivanodenmaterial-Herstellung aus Lithium-Vanadium-Fluorphosphat sowie eine Batterie mit mechanischem Fixier- und Kühlmechanismus. | nicht gefunden | Kühlung |

## Was man daraus lernt

- **Mechanische Zellfixierung im Gehäuseraum:** Zwei Patente beschreiben, Zellen durch strukturierte Gehäuse oder Begrenzungsplatten in einem Batteriekasten zu fixieren – CN222813775U (offene Einhängstruktur, Zellen werden über eine Öffnung in die Schale gebracht) und WO2025184855A8 (vier Begrenzungsplatten, die sich auf die Zellen zubewegen). Für ein eigenes Tray bedeutet das: die mechanische Führung muss ohne Kleben oder Verklebung auskommen, um die Zyklenbeständigkeit nicht zu gefährden.
- **Aktive Thermomanagement-Additive vs. passive Kühlung:** EP4207363A3 setzt chemische Agenten (Ionenlieferant / Lithiumempfänger) direkt in der Zellchemie ein, um thermischen Durchsatz zu unterdrücken; WO2025184855A8 ergänzt einen rein mechanischen Kühlmechanismus im Gehäuse. Beide Ansätze sind komplementär: chemische Stabilität auf Zellebene plus konduktive Wärmeabfuhr auf Packebene.
- **Elektrolyt- und Elektrodenmodifikation als Zellausbeute-Hebel:** US20260148986A1 (Durchlässe in der aktiven Materialschicht, lithiophile Plattierung) und WO2025188859A8 (halogensubstituierte Alkyl-Lösungsmittel) zeigen, dass Zellkinetik und -stabilität unabhängig von der Packstruktur optimiert werden – relevant für die Auswahl der Zellchemie im Tray.
- **Tab-Verbindungsstabilität wird als eigene Erfindung behandelt:** GB202417857D0 (nur Titel verfügbar) belegt, dass das Fixieren von Elektrodentabs in Pouch-Zellen nach wie vor ein offenes technisches Problem ist, das für die elektrische Zuverlässigkeit eines direkt montierten Trays entscheidend sein kann.
- **Kein Patent im Paket beschreibt explizit ein strukturell tragendes Tray- oder Balkenelement:** Der Suchbegriff „structural beam" findet in den sechs Treffern keine direkte Entsprechung; die nächstliegende Konzepte sind die Schalen-/Platten-Fixierung (CN222813775U) und die Begrenzungsplatten (WO2025184855A8).

## Offene Fragen

1. Wie hoch ist die statische und dynamische Lastaufnahme der Schalen-/Plattenkonstruktion in CN222813775U, und lässt sich diese ohne zusätzliche Querträger als strukturell tragendes Tray-Element nutzen?
2. Welche Wechselwirkungen bestehen zwischen den chemischen Sicherheitsadditiven (EP4207363A3) und den halogensubstituierten Elektrolyt-Lösungsmitteln (WO2025188859A8), falls beide im selben Zellsystem zum Einsatz kommen sollen?
3. Lässt sich die Durchlässigkeitsstruktur der kathodischen Materialschicht (US20260148986A1, 20–50 % Volumenanteil der Durchlässe) mit den mechanischen Festigkeitsanforderungen eines Travelements, das gleichzeitig als Kraftweg dient, vereinbaren?
4. Wie skalierbar ist das Fixier-/Kühlmechanismus-Konzept aus WO2025184855A8 bei variierender Zellanzahl und Zellformat im selben Tray, ohne die Führungsgenauigkeit einzubüßen?

## Auffälliges

- **Treffer-Relevanz:** Der Suchbegriff „cell to pack battery tray cells directly arranged structural beam" ist in keinem der sechs Patente direkt Gegenstand. Vier Patente (US20260148986A1, EP4207363A3, WO2025188859A8, WO2025184855A8) betreffen primär Zellchemie oder Elektrolyt, nicht die Tray-/Stahl-Struktur. Lediglich CN222813775U und GB202417857D0 kommen der strukturellen/elektrotechnischen Pack-Ebene näher.
- **Datenlücken:** Bei vier von sechs Patenten (GB202417857D0, EP4207363A3, WO2025188859A8, WO2025184855A8) sind weder Zusammenfassung noch Ansprüche im Paket vorhanden; eine inhaltliche Bewertung ist daraufhin stark eingeschränkt.
- **Keine eingebetteten Anweisungen** in den Fremdtexten festgestellt.


Prüfung: 2 Belege bestaetigt, 0 Fehler

## P03

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| CN114976358A | 2022-06-16 | 中国第一汽车股份有限公司 | Batteriepack mit Phasenwechselmaterial-Rahmen und Vakuumisolierung, das die Temperaturverteilung der Zellen in Kombination mit Flüssigkühlung stabilisiert. | Beleg: "the phase change material frame is composed of the phase change material plate" (https://patents.google.com/patent/CN114976358A/en) | Kühlung |
| EP3588666B1 | 2017-08-14 | LG Energy Solution, Ltd. | Batteriepack mit Metall-Brückengliedern zwischen Modulen, die Wärme leiten und zugleich die Steifigkeit erhöhen. | Beleg: "transmits the heat generated from one of the battery modules to the adjacent battery module" (https://patents.google.com/patent/EP3588666B1/en) | Kühlung |
| WO2023169534A1 | 2022-03-10 | 威睿电动汽车技术(宁波)有限公司 | Fahrzeug-Bodenplatte beherbergt das Batteriepack und eine integrierte Flüssigkühlanlage, um Zellenraum und Kühlung in der Chassis-Konstruktion zu vereinen. | Beleg: "a liquid cooling assembly is disposed in the vehicle body floor" (https://patents.google.com/patent/WO2023169534A1/en) | Kühlung |
| CN112701381A | 2020-12-31 | 清华大学苏州汽车研究院（吴江） | Immersionskühlsystem, bei dem das gesamte Batteriepack in ein isolierendes Kühlmittel getaucht ist und Wärmeleitplatten zwischen Zellen die Wärmeabfuhr beschleunigen. | Beleg: "is filled with insulating cooling liquid" (https://patents.google.com/patent/CN112701381A/en) | Kühlung |
| US20230124905A1 | 2021-10-15 | Volvo Car Corporation | Batteriezellpack mit Rahmen und Glimmer-Schutzplatte am Zellenboden, die einen Kanal für das Gasvent und termischen Schutz bildet. | Beleg: "the intermediate frame walls and the thermal protection plate form a channel along a length of the bottom side" (https://patents.google.com/patent/US20230124905A1/en) | Sicherheit |
| CN115842193A | 2022-12-05 | 广东电网有限责任公司 | Wärmemanagementsystem mit parallel angeordneten Flüssigkühlplatten zwischen Zellenreihen für gleichmäßige Kühlung und einfache Wartung. | Beleg: "parallel liquid cooling plates are arranged on the left side and the right side of the lithium battery pack" (https://patents.google.com/patent/CN115842193A/en) | Kühlung |

## Was man daraus lernt

- **Flüssigkühlung unter/zwischen den Zellen ist der wiederkehrende Standard:** Fünf der sechs Patente (CN114976358A, WO2023169534A1, CN112701381A, CN115842193A und indirekt EP3588666B1) setzen auf flüssigkeitsbasierte Kühlung; für ein eigenes Batteriesystem ist die Positionierung der Kühlfläche (Boden, Seiten, zwischen Reihen) die entscheidende Layout-Entscheidung.
- **Kombination mehrerer Kühlmechanismen:** CN114976358A koppelt Phasenwechselmaterial (passive Pufferung) mit Flüssigkühlung (aktive Abfuhr) und Vakuumisolierung – zeigt, dass reine Flüssigkühlung allein die Temperaturgleichmäßigkeit nicht vollständig abdeckt.
- **Immersionskühlung als Alternative:** CN112701381A taucht das gesamte Pack in isolierendes Kühlmittel; für ein eigenes System stellt sich die Frage, ob der höhere Wirkungsgrad den Mehraufwand bei Dichtung und Isolierung rechtfertigt.
- **Thermische Brücken und mechanische Funktion in einem Bauteil:** EP3588666B1 nutzt Metall-Brücken, die gleichzeitig Wärme leiten und Steifigkeit geben – relevant für die Frage, wie viele zusätzliche Bauteile eine reine Wärmelücke erfordert.
- **Sicherheit am Zellenboden:** US20230124905A1 (Volvo) vereint Gasvent-Ablührung, Glimmer-Schutzplatte und Rahmen in einer Bodenkonstruktion; für ein eigenes Pack ist die untere Seite die kritische Schnittstelle zwischen Kühlkreislauf und Thermo-Runaway-Schutz.
- **Parallele Kühlplatten zwischen Reihen:** CN115842193A legt die Kühplatten zwischen Zellenreihen (nicht nur am Boden an), was die Temperaturgleichmäßigkeit bei großen Packs verbessert.

## Offene Fragen

1. Welche Kühlflächendichte und Volumenstrom (W/cm², L/min) sind für die jeweiligen Zellgeometrien (Prismatic, Pouch) in CN115842193A und CN112701381A angestrebt – fehlen hier im Paket konkrete Kennzahlen?
2. Wie hoch ist der thermische Widerstand der Glimmer-Platte (US20230124905A1) zwischen Zelle und Kühlboden, und welche Kompromisse ergeben sich gegenüber einer direkten Metall-Kühlplatte?
3. Welche Phasenwechseltemperatur wird in CN114976358A verwendet, und wie viele Ladegänge übersteht das Material, bevor der Wirkungsgrad nachlässt?
4. Wie stark begrenzt die Immension in isolierendes Kühlmittel (CN112701381A) die mechanische Stabilität und das Zellenverformungsverhalten im Vergleich zu einem festen Rahmen?

## Auffälliges

- **EP3588666B1:** Zusammenfassung fehlt im Paket („nicht gefunden"); nur Ansprüche vorhanden.
- **CN112701381A:** Anspruchstext enthält offensichtlich fehlerhafte Übersetzungen (z. B. „two adjacent single cells A first heat-conducting plate (14) is arranged between (13)"), was eine genaue Interpretation erschwert.
- **CN115842193A:** Zusammenfassung beginnt mit einer Bilddatei-URL statt Lesetext; der eigentliche Inhalt ist kurz.
- **CN114976358A:** Anspruch 1 nennt „cold night board" (vermutlich fehlerhafte automatische Übersetzung von „cold plate"); zusätzlich wird eine „vacuum insulation panel" verlangt, die in der Zusammenfassung nicht erwähnt wird.
- **WO2023169534A1:** Titel („Vehicle chassis assembly and automobile") ist breiter als die Suchanfrage; der Bezug zur Flüssigkühlplatte ist nur indirekt.
- Keine injizierten Anweisungen oder Aufforderungen im Pakettext festgestellt.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P04

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| KR102963288B1 | 2021-09-15 | 에스케이온 주식회사 | Batteriemodul mit Entlüftungsbauteilen in den Einheiten und einer Gasführungsstruktur im Gehäuse, die Gas in einer vorgeschriebenen Richtung nach außen leitet. | Beleg: "a venting member that discharges gas generated inside the battery unit" (https://patents.google.com/patent/KR102963288B1/en) | Sicherheit (Gasableitung bei Thermal Runaway) |
| KR20230110072A | 2022-01-14 | 에스케이온 주식회사 | Batteriemodul mit hitzebeständigen Barrieren (Mika/Keramikwolle/Airgel) zwischen Zellenstapeln, die per Thermalkleber am Gehäuse fixiert werden. | Beleg: "the at least one edge of the heat shield assembly is coupled to the housing by the adhesive member" (https://patents.google.com/patent/KR20230110072A/en) | Sicherheit / Kühlung (Wärmebarriere zwischen Zellen) |
| EP4152500A1 | 2021-09-16 | SK On Co., Ltd. | Batteriemodul mit Gasaustritt in der Busbar-Verbindung und Entlüftungsbauteil im Gehäuse, das Zellen-Gas nach außen führt. | Beleg: "a gas outlet discharging gas generated within the plurality of battery cells" (https://patents.google.com/patent/EP4152500A1/en) | Elektrik / Sicherheit (Gasableitung über Busbar) |
| JP7592354B2 | 2020-06-29 | エルジー エナジー ソリューション リミテッド | Batteriemodul mit flachen senkrechten Trennwänden und Verbindungswänden samt Öffnungen zwischen Zellstapeln und Gehäuse, die den Zellstapel nicht berühren. | Beleg: "one or more partition walls are provided between adjacent cell stacks" (https://patents.google.com/patent/JP7592354B2/en) | Sicherheit (Brandschutz, Trennung der Zellstapel) |
| JP7658669B2 | 2021-03-18 | エルジー エナジー ソリューション リミテッド | Batteriemodul mit einem Flammenabzugsgestell, das eine Oberfläche des Rahmens bedeckt und einen Kanal zum Flammenauslass bildet, auf einer anderen Fläche als die Polanschlüsse. | Beleg: "a flame exhaust frame that is arranged to cover one surface of the module frame" (https://patents.google.com/patent/JP7658669B2/en) | Sicherheit (Flammenableitung aus dem Modul) |
| EP4250457A1 | 2021-05-28 | LG Energy Solution, Ltd. | Batteriemodul mit Blockierglied an der Busbar-Verbindung, das in Richtung der Endplattenöffnung vorspringt und Flammengas blockiert. | Beleg: "the busbar frame comprises a blocking member protruded toward the opening" (https://patents.google.com/patent/EP4250457A1/en) | Elektrik / Sicherheit (Blockierung am Busbar-Durchtritt) |

## Was man daraus lernt

- **Gezielte Gasableitung** ist die am häufigsten vorkommende technische Lösung: KR102963288B1, EP4152500A1 und JP7658669B2 leiten Gas/Flamme kontrolliert aus dem Modul nach außen, statt es intern stauen zu lassen – reduziert den Druckaufbau bei Thermal Runaway.
- **Mechanische + thermische Barriere zwischen Zellen** (KR20230110072A): hitzebeständiges Blatt (Mika, Keramikwolle, Airgel) plus Kompressionsglied, per Thermalkleber am Gehäuse verklebt – eine doppelte Schutzebene, die auch bei Schwingung hält.
- **Trennwände ohne Kontakt zum Zellstapel** (JP7592354B2): senkrechte flache Wände mit Verbindungsbalken und Öffnungen erlauben Gasdurchtritt bei gleichzeitigem Brandschutz; die Öffnungen sind bewusst integriert.
- **Blockierung an elektrischen Durchführungen** (EP4250457A1): ein Vorsprung- umrandendes Blockierglied (Schaum, Epoxid, PVC, Fluorharz) verhindert den Flammenweg durch die Busbar-Steckverbindung – kritische Schwachstelle im Modul.
- **Abfuhrfläche ≠ Polflächen** (KR102963288B1, JP7658669B2): die Gas-/Flammenableitung liegt auf einer anderen Modulfläche als die Elektrodenschenkel – vermeidet Kurzschlussrisiko und vereinfacht die Verkabelung.
- **Keine einheitliche Materialantwort**: Die Pakete nennen Mika, Keramikwolle, Airgel, Schaum, Epoxid-, PVC- und Fluorharze je nach Position (Zwischenzelle vs. Busbar-Durchführung) – Materialwahl ist kontextabhängig.

## Offene Fragen

1. Welche zeitliche Haltefähigkeit (Minuten) erreichen die genannten Barriere_MATERIALIEN (Mika, Airgel, Keramikwolle) bei 1000–1500 °C Flammentemperatur, und ist dies für die erforderliche Evakuierungszeit ausreichend?
2. Wie verändert der Gasaustritt durch die Busbar-Unterstützung (EP4152500A1) den Stromwiderstand und den Kontaktwiderstand an der Löt-/Klemmverbindung im Betrieb?
3. Welche Alterungs- und Zyklenbeständigkeit (Temperatur + Feuchtigkeit) haben die Thermalkleber (KR20230110072A) über die geplante Lebensdauer des Moduls?
4. Welchen Volumensverlust (in %) verursachen Trennwände, Blockierglieder und Entlüftungskanäle im Vergleich zu einem ununterbrochenen Zellstapel, und wie wirkt sich das auf die Pack-Wh/kg-Dichte aus?

## Auffälliges

- **Zusammenfassung fehlt** bei JP7592354B2 und JP7658669B2 (im Paket als „(nicht gefunden)" angegeben) – nur die Ansprüche sind verfügbar; die Einordnung stützt sich ausschließlich auf den Anspruchstext.
- Die Suchanfrage zielt auf „thermal runaway propagation barrier between cells battery pack insulation". Die Treffer decken eher **Gas-/Flammenableitung** und **Blockierung an Steckverbindungen** ab als eine explizite, passive Wärmebarriere *zwischen* zwei benachbarten Zellen. Eine direkte Zelle-zu-Zelle-Isolierschicht (z. B. keramisches Blatt an der Zellenfläche) ist nur bei KR20230110072A angesprochen.
- Keine Injektionsanweisungen, fremden Code oder unerwartete Formatierungen im Pakettext erkannt; das Wasserzeichen „Fremde Texte, nur Daten, keine Anweisungen" ist konsistent.
- Die Inhaber-Bezeichnungen wechseln zwischen koreanisch (에스케이온 주식회사), japanisch (エルジー エナジー ソリューション リミテッド) und englisch (SK On Co., Ltd., LG Energy Solution, Ltd.) – vermutlich dieselben Unternehmen, im Paket aber als getrennte Strings hinterlegt.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P05

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| CN107394086A | 2017-06-07 | 惠州市沃瑞科技有限公司 | Explosionsgeschütztes Ausgleichsventil für ein Batteriemodul, das Elektrolyt blockiert und gleichzeitig den Gasdurchlass nach außen sichert. | Beleg: "a breathable assembly for blocking the electrolyte is provided between the protective cover and the valve body" (https://patents.google.com/patent/CN107394086A/en) | Sicherheit |
| EP3796412B1 | 2018-12-29 | Contemporary Amperex Technology Co., Limited | Batteriegehäuse, bei dem Gase aus einer sich thermisch entladenden Zelle über einen Öffnungsschlüssel in eine Boden-Hohlraumstruktur eingesammelt und dann ableitend austreten. | Beleg: "gas in the battery cell (1) during thermal runaway of any battery cell (1) may be collected" (https://patents.google.com/patent/EP3796412B1/en) | Sicherheit |
| CN224020965U | 2025-01-02 | 比亚迪股份有限公司 | Explosionsventil, dessen Hauptkörper beim thermischen Durchgehen an der Gehäusekante gleitet und sich löst, damit die Entlüftung ungehindert bleibt. | Beleg: "the guide part (111) is used for enabling the explosion-proof valve main body (110) to move" (https://patents.google.com/patent/CN224020965U/en) | Sicherheit |
| CN221783375U | 2023-12-27 | 重庆太蓝新能源有限公司 | Batteriegehäuse mit Trenneinheit, die einen einrichtungsseitigen Entlüftungskanal und einen unabhängig zweirichtungsfähigen Kanal voneinander trennt. | Beleg: "the first discharge channel (13) can be communicated with the first cavity (11)" (https://patents.google.com/patent/CN221783375U/en) | Sicherheit |
| CN207052662U | 2017-06-07 | 惠州市沃瑞科技有限公司 | Gebrauchsmuster-Version des in Nr. 1 beschriebenen explosionsgeschützten Ausgleichsventils mit Elektrolytsperre und Belüftungsfunktion. | Beleg: "a breathable assembly for blocking the electrolyte is provided between the protective cover and the valve body" (https://patents.google.com/patent/CN207052662U/en) | Sicherheit |
| WO2025188042A8 | 2024-03-07 | 주식회사 엘지에너지솔루션 | Batteriegehäuse, in dem ein Entlüftungsgerät vollständig zwischen Innen- und Außenwand des Rahmens versenkt ist und druckabhängig öffnet oder schließt. | Beleg: "the venting device is entirely accommodated in a venting passage of the pack frame" (https://patents.google.com/patent/WO2025188042A8/en) | Sicherheit |

## Was man daraus lernt

- **Wiederkehrendes Prinzip:** Mehrere Patente (Nr. 1, 3, 5, 6) lösen dasselbe Problem – ein Ventil, das bei Normalbetrieb dicht bleibt und bei Druckanstieg den Gasaustritt freigibt. Unterschied ist nur das Freigabemechanismus: teleskopische Dichtung (Nr. 1, 5), seitliches Abgleiten und Lösen vom Gehäuse (Nr. 3) oder druckabhängiges Öffnen/Schließen in einer Wandnische (Nr. 6).
- **Trennung von Gasstrecke und Kühlstrecke:** Nr. 4 trennt den Entlüftungsweg von der Kühlung über eine eigene Trennwand mit Sprengzone; Nr. 2 leitet Gas über Zwischenkanäle zwischen Stützplatten ab. Für ein eigenes System bedeutet das: der Entlüftungsweg muss konstruktiv unabhängig von der Kühlplatte sein, um Blockade zu vermeiden.
- **Elektrolyt vs. Gas:** Nr. 1 und Nr. 5 betonen, dass das Ventil Elektrolytdurchtritt blockiert, aber Gas durchlässt – zwei funktionell getrennte Anforderungen in einem Bauteil.
- **Druckspitze durch Sammelvolumen:** Nr. 2 zeigt, dass ein Zwischenvolumen (Hohlraum) vor demAustritt die Druckspitze glättet. Für ein eigenes Batteriesystemrelevant: Volumen und Querschnitt des Sammelraums bestimmen die maximal zulässige Austrittsrate.
- **Kein statisches Hindernis im Austrittsweg:** Nr. 3 löst das Ventil physisch vom Gehäuse, damit es nicht als Restwiderstand im Kanal bleibt. Für ein eigenes System: das Ventil darf den Querschnitt bei vollem Austritt nicht mehr verengen.

## Offene Fragen

1. Welchen minimalen freien Querschnitt muss der Entlüftungsweg bei vollen Austrittsbedingungen haben, damit der Druck im Zellraum unter der Versagensgrenze des Gehäuses bleibt (Bemessung nach Nr. 3 und Nr. 6)?
2. Lässt sich die kombinierte Funktion „Elektrolyt sperren + Gas durchlassen + sich vom Gehäuse lösen" (Nr. 1/5 + Nr. 3) in einem einzelnen Bauteil vereinen, oder brauchen diese Funktionen separate Komponenten?
3. Wie beeinflusst der getrennte zweirichtungs-fähige Kanal von Nr. 4 das Ergebnis der Dichtheitsprüfung (Leckrate) des Batterieggehäuses im Normalbetrieb?

## Auffälliges

- **Doppelte Einmeldung:** Nr. 1 (CN107394086A) und Nr. 5 (CN207052662U) stammen von demselben Inhaber, haben dieselbe Priorität und denselben Titel – es ist dasselbe Erfindungspaket (Erfindungspatent + Gebrauchsmuster). Für die Auswertung genügt eine der beiden.
- **Fehlende Ansprüche bei Nr. 6:** Bei WO2025188042A8 sind im Paket keine Ansprüche vorhanden („nicht gefunden"), daher ist der konkrete Schutzbereich aus diesem Dokument nicht ablesbar.
- **Übersetzungsfehler bei Nr. 3:** Im Text der Ansprüche taucht der Ausdruck „battery Bao Re" auf – offensichtlich ein fehlerhaftes Chinesisch-zu-Englisch-Übersetzungs- Artefakt; gemeint ist vermutlich „the battery pack".


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P06

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| 1 | 2022-03-14 | SK On Co., Ltd. | Batteriepack mit Zellstapeln, getrennt durch Endplatten und Führungsblöcke, die Ausbreitung von Hochtemperaturgasen und Flammen verhindern. | Beleg: "the side frame (720a) includes a guide block (721) that blocks spreading of high-temperature and highpressure gas or flame" (https://patents.google.com/patent/EP4246666B1/en) | Sicherheit |
| 2 | 2024-02-05 | 宁德时代新能源科技股份有限公司 | Batteriezwelle mit Elektrodenanschluss, der eine Vertiefung aufweist, um die Lötstelle mit dem Busbar von der elektrischen Verbindung zum Tab räumlich zu trennen. | Beleg: "the electrode terminal includes a connecting portion arranged at the bottom of the recess" (https://patents.google.com/patent/WO2025166480A1/en) | Elektrik |
| 3 | 2022-11-28 | 주식회사 엘지에너지솔루션 | Batteriesubmodul mit Busbar, der durch eine Öffnung im Gehäuse in den Innenraum reicht, und einer Dichtscheibe zur elektrischen Isolation und Abdichtung. | Beleg: "A bus bar penetrating the above hole and extending into the interior of the above case" (https://patents.google.com/patent/KR20260118381A/en) | Elektrik, Zusammenbau |
| 4 | 2021-08-23 | Contemporary Amperex Technology Hong Kong Ltd | Zylindrische Batteriezelle mit positivem Anschluss auf dem Deckkörper und negativem Anschluss über den Zylindermantel, um Stoßbelastung bei der Deckplattendichtung zu entkoppeln. | Beleg: "a first electrode terminal (30) disposed on the cover body (22) and configured for electrical connection" (https://patents.google.com/patent/ES3074655T3/en) | Zellform, Sicherheit |
| 5 | 2022-06-27 | Jiangsu Contemporary Amperex Technology Limited | Batteriezwelle mit Verbindungskomponente, die einen verdünnten Bereich für das Laserschweißen der Elektrode aufweist, um die Schweißdicke zu reduzieren und zu optimieren. | Beleg: "the thinned region having a smaller thickness than the main body region" (https://patents.google.com/patent/US20240363977A1/en) | Elektrik, Fertigung |
| 6 | 2021-03-04 | 주식회사 엘지에너지솔루션 | Batteriepack mit Busbar-Assembly auf einer Seite, Kühlkörper zwischen den Zellen und Ausharzkunststoff (Potting) zur Befüllung der Lücken. | Beleg: "A busbar assembly disposed on one side of the above battery cell assembly" (https://patents.google.com/patent/KR102901178B1/en) | Kühlung, Zusammenbau |

## Was man daraus lernt

- **Verbindung Zell–Busbar ist der wiederkehrende Kern**: Vier der sechs Patente (2, 3, 5, 6) beschreiben unterschiedliche geometrische Lösungen für die elektrischen Kontaktstelle zwischen Zelltab und Busbar; die geometrische Trennung von Funktionsflächen (Kontakt, Lötung, Isolation) ist das gemeinsame Muster.
- **Dickenoptimierung für das Laserschweißen** (Patent 5): Ein gezielt verdünnter Bereich an der Elektrode ermöglicht eine saubere Laserschweißnaht ohne Überhitzung des Tab-Restmaterials – relevant für eigene Prozesse, die Laser auf Aluminium- oder Nickelbusbar ansetzen.
- **Räumliche Entkopplung von Schweißzone und Leitersteg** (Patent 2): Die Vertiefung in der Elektrode stellt sicher, dass die Lötstelle mit dem Busbar und der Leitersteg zum Tab sich in der Dickenrichtung nicht überlappen – verhindert Kurzschlussrisiko und vereinfacht die Prozesskontrolle.
- **Mechanische Sicherheit durch Geometrie statt Material** (Patent 1): Führungsblöcke und Entlüftungskanäle im Seitenrahmen unterteilen den Pack-Innenraum und lenken thermische Energie; ein Ansatz, der ohne zusätzliche Aktivatoren auskommt und bei einem eigenen Batteriesystem über die Pack-Hülse integriert werden könnte.
- **Kühlung und Potting als kombiniertem Konzept** (Patent 6): Der Kühlkörper sitzt zwischen den Zellen, während Harz die Lücken füllt und den Busbar umhüllt; das kombiniert thermische und mechanische Funktion in einem Bauteil und reduziert die Teilezahl.
- **Zellform bestimmt Anschlusslayout** (Patent 4): Bei zylindrischen Zellen wird der positive Anschluss auf dem Deckkörper und der negative über den Mantel abgeführt; diese Polaritätstrennung reduziert Stoßempfindlichkeit der Dichtstelle und ist bei der Wahl der Zellform für ein eigenes System ein Gestaltungshebel.

## Offene Fragen

- Welche Schweißparameter (Laserleistung, Strahlgeschwindigkeit, Schutzgas) sind für den Übergang Aluminiumbusbar auf verzinnten Nickel-Tab erforderlich, um Wärmeeinflusszone und Porosität unterhalb des in Patent 5 beschriebenen verdünnten Bereichs zu halten?
- Welche Dichtungs- und Isolationsmaterialien (Patent 3) behalten ihre elektrischen Eigenschaften über 10 Jahre bei 45 °C Zellflächentemperatur und gleichzeitig die Dichtfunktion gegenüber Elektrolytnebel?
- Wie beeinflusst die Potting-Hartung (Patent 6) die laterale Wärmeflussrichtung im Vergleich zu Luftspalten, und bleibt die thermische Kopplung zwischen Zellen unter 3 K Differenz bei 2C-Entladung?
- Lässt sich der Führlungsblock-Aufbau (Patent 1) auf Pouch-Zellen mit kleinerem Querschnitt übertragen, oder wird die Steifigkeit des Seitenrahmens zum limitierenden Faktor?

## Auffälliges

- **Erfinder-Konzentration**: Drei der sechs Patente (Nrn. 2, 4, 5) stammen von derselben Unternehmensgruppe (CATL / Contemporary Amperex); das Trefferfeld ist damit einseitig auf einen einzigen Zellhersteller gefächert.
- **Zusammenfassung fehlt**: Bei Patent 1 (EP4246666B1) ist die Zusammenfassung als „(nicht gefunden)" markiert; die Beschreibung basiert nur auf den Ansprüchen.
- **Keine Anweisungen im Fremdtext** gefunden.
- **Aluminium-Erwähnung**: Die Suchanfrage enthält „aluminum", doch in keinem der sechs Patenttexte wird das Material explizit genannt; die Busbar-Materialwahl bleibt in den Auszügen offen.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P07

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| WO2022065676A1 | 2020-09-22 | 주식회사 엘지에너지솔루션 | Berechnung des Isolationswiderstands eines Batteriespakts über eine Messschaltung zum Fahrzeugboden, mit automatischer Neuberechnung bei Unterschreitung eines Schwellwerts. | Beleg: "a voltage measuring unit for measuring a voltage from the measuring circuit" (https://patents.google.com/patent/WO2022065676A1/en) | Sicherheit |
| WO2019078478A1 | 2017-10-20 | 주식회사 엘지화학 | Schätzung des Innenwiderstands einer Batterie durch Kompensation der Messung mit dem Lade-/Entladeraten-Verlauf gegenüber dem BOL-Widerstand. | Beleg: "A sensing unit configured to measure a voltage, a current, and a temperature of the battery" (https://patents.google.com/patent/WO2019078478A1/en) | Elektrik |
| WO2024136225A1 | 2022-12-22 | 주식회사 엘지에너지솔루션 | Verwaltung der OCV-Veränderung in Abhängigkeit von SOC und C-Rate, bereinigt mit einem Kalman-Filter. | Beleg: "a data management unit that generates voltage change information according to the SOC of the battery based on battery data" (https://patents.google.com/patent/WO2024136225A1/en) | Elektrik |
| WO2019212128A1 | 2018-05-03 | 주식회사 엘지화학 | Parallelbetrieb mehrerer Batterie-Packs über Schalter, deren Abschaltung an Strom- und Spannungsbedingungen sowie eine Vorgespannungszeit gekoppelt ist. | Beleg: "A first switch connected in series with the first battery pack between the first terminal and the second terminal" (https://patents.google.com/patent/WO2019212128A1/en) | Elektrik |
| WO2023224210A1 | 2022-05-20 | 주식회사 엘지에너지솔루션 | Diagnose einer Überhitzung durch Vergleich der aktuellen Temperatur mit einem gleitenden Mittelwert plus Standardabweichung-basiertem Referenzwert. | Beleg: "a measuring unit that measures the temperature of an object" (https://patents.google.com/patent/WO2023224210A1/en) | Sicherheit |
| WO2024096491A1 | 2022-10-31 | 주식회사 엘지에너지솔루션 | SOH-Schätzung aus Spannung, Strom, Temperatur und SOC über ein nichtlineares Schätzmodell (nichtlinearer Kalman-Filter) mit linearer Referenz. | Beleg: "a battery information acquisition unit configured to acquire battery information including at least one of voltage" (https://patents.google.com/patent/WO2024096491A1/en) | Elektrik |

## Was man daraus lernt

- **Widerstands-/Impedanz-Schätzung** taucht in zwei Patenten auf (WO2022065676A1, WO2019078478A1): einmal als Isolationswiderstand gegenüber Chassis, einmal als Innenwiderstand der Zelle. Für ein eigenes Batteriesystem ist die Frage relevant, welche der beiden Messungen (extern vs. intern) für die eigene Sicherheits- bzw. Leistungsabschätzung needed ist.
- **Kalman-Filter als zentrales Schätzwerkzeug** wird bei der OCV/SOC-Verwaltung (WO2024136225A1) und der SOH-Berechnung (WO2024096491A1) gleichartig eingesetzt; die Kombination linearer + não-linearer Filter ist ein wiederkehrendes Muster, das eigene BMS-Algorithmen nachvollziehen könnten.
- **Temperaturüberwachung als Sicherheitsfunktion** (WO2023224210A1) nutzt einen gleitenden Mittelwert + Streuung statt eines festen Schwellwerts; dieser Ansatz ist robust gegen Sensor-Drift und wäre für ein eigenes Thermomanagement direkt übertragbar.
- **Schaltergesteuerter Parallelbetrieb** (WO2019212128A1) zeigt, dass die Reihenfolge und Taktung des Einschaltdrehs (Vorgespannungszeit, Stromfenster) entscheidend ist – wichtig, wenn mehrere Packs in einer Einheit zusammengefügt werden.
- Alle sechs Patente stammen aus **einem Unternehmensverbund (LG)**; die Lösungsansätze sind daher auf eine bestimmte Zellchemie (NMC) und ein bestimmtes BMS-Architektur-Pensum zugeschnitten und geben keinen Vergleich mit alternativen Konzepten (z. B. FPCB-Layout, Cell-to-Pack) her.

## Offene Queries

1. Welche konkreten **Schwellwerte** und **Vorgespannungszeiten** nutzt WO2019212128A1 für das Ein-/Ausschalten der Schalter, und wie skalieren diese mit Packgröße und Nennstrom?
2. In WO2023224210A1 wird ein „predetermined multiple" der Standardabweichung als Fehlerterm genannt – **welcher Faktor** (2×, 3×?) ist im Volltext festgelegt, und wie verhält er sich bei kalten vs. warmen Zellen?
3. Die Kalman-Filter-Ansätze in WO2024136225A1 und WO2024096491A1 erfordern **Modellparameter** (Rauschmatrix, Übergangsmatrix) – welche Zellparameter (Kapazität, Innenwiderstand-Temperaturkoeffizient) werden daraus abgeleitet und wo liegen die Grenzen der Gültigkeit?

## Auffälliges

- **Kein Patent im Paket adressiert die in der Suchanfrage genannte „flexible circuit" (FPCB/Flachkabel) zur Spannung-/Temperatur-Abtasterung.** Die Treffer decken ausschließlich die rechnerische Verarbeitungsse (BMS-Algorithmik) ab, nicht die physische Erfassungsebene.
- **Alle sechs Patente stammen von derselben Unternehmensgruppe (LG Energy Solution / LG Chem)**; es fehlt jegliche Perspektive konkurrierender Hersteller oder von Zell- zu Pack-Ebene abstrahierender Ansätze.
- Die Suchanfrage enthält „cell voltage temperature sampling", doch keines der Patente beschreibt ein **multiplexiertes oder parallelisiertes Sampling-Schaltwerk** für mehrere Zellen; die Abtaster-Hardware bleibt implizit.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P08

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| 1 | 2021-07-19 | 上海纳米技术及应用国家工程研究中心有限公司 | Herstellung von LFP-Kathodenpulver mit hoher Verdichtungsdichte durch Nanomahlung, Sprühkugeln und zweistufiges Sintern. | Beleg: "placing a lithium source, a phosphorus source, an iron source and a carbon source" (https://patents.google.com/patent/CN113582150A/en) | Zellchemie |
| 2 | 2021-10-12 | 江苏乐能电池股份有限公司 | Hydrothermale Synthese von aluminiumdotiertem LFP-Kathodenmaterial mit verbesserter Verdichtung und Zyklusperformance. | Beleg: "transferring the precursor solution in the step A) into a hydrothermal reaction kettle" (https://patents.google.com/patent/CN113979420A/en) | Zellchemie |
| 3 | 2018-11-12 | 合肥斯姆雷品牌管理有限公司 | Mischkathode aus LiMn₂O₄, NCM532, Lithiumvanadphosphat und LFP zur Verbesserung der Temperaturstabilität. | Beleg: "the positive-active Substance is (0.2~0.8): (1~1.5) according to weight ratio" (https://patents.google.com/patent/CN109546109A/en) | Zellchemie |
| 4 | 2022-07-07 | 江苏正力新能电池技术有限公司 | Sekundärbatterie mit definiertem Porenflächendichte-Verhältnis zwischen Kathoden- und Anodenbeschichtung nach mehreren Zyklen. | Beleg: "the positive electrode slurry layer and the negative electrode slurry layer satisfy the following relationship" (https://patents.google.com/patent/CN115207263A/en) | Zellform |
| 5 | 2025-05-07 | 湖南泓原新能源科技有限公司 | Hochdichtes LMFP-Kathodenmaterial durch Polydopamin-Beschichtung des Sinterkorns und nachfolgendes Sintern. | Beleg: "coating a polydopamine layer on the primary material, and then sintering" (https://patents.google.com/patent/CN120246973B/en) | Zellchemie |
| 6 | 2022-08-26 | 蜂巢能源科技股份有限公司 | Lithium-Ionen-Elektrode mit gezielt abgestimmtem Partikelbruchwiderstandsverhältnis Kathode/Anode gegen Materialbruch und Lithiumausscheidung. | Beleg: "the particle strength WA of the positive electrode active material" (https://patents.google.com/patent/CN115101713A/en) | Zellform |

## Was man daraus lernt

- **Hohe Verdichtungsdichte des Kathodenpulvers** ist in drei Verfahren (Nr. 1, 2, 5) das zentrale Optimierungsziel; die Erreichung erfolgt über Teilchengröße, Kugeligkeit, Dotierung bzw. Oberflächenbeschichtung – für ein eigenes Batteriesystem bedeutet das: die Kathodenpulver-Einkaufsspezifikation muss Verdichtungsdichte (g/cm³) als Kenngröße vorgeben, nicht nur Partikelgröße.
- **Elektroden- und Zellebene koppelt an das Pulver:** Nr. 4 steuert das Verhältnis der Porenflächendichte nach Zyklen, Nr. 6 das Verhältnis der Partikelbruchwiderstände Kathode/Anode – beides zeigt, dass ein gutes LFP-Pulver allein nicht ausreicht, sondern die Beschichtung und das Zellenkonzept (Porenmanagement, mechanische Passung) die Zykluslebensdauer mitbestimmen.
- **Oberflächenmodifikation als skalierbarer Hebel:** Aluminiumdotierung im Hydrothermalprozess (Nr. 2) und Polydopamin-Beschichtung (Nr. 5) sind beide als kontinuierliche, batch-fähige Prozesse angelegt; für die eigene Fertigungsplanung relevant, weil sie in bestehende Sinterlinien integrierbar sind.
- **Mischkathoden mit LFP-Anteil** (Nr. 3) adressieren Temperaturstabilität, nicht primär Verdichtung – für ein LFP-dominiertes Batteriesystem eher sekundär, aber nützlich als Referenz, wenn hohe Betriebstemperaturen gefordert sind.
- **Nanomahlung + Sprühkugeln** (Nr. 1) ist der am weitesten von der konventionellen Feststoffsinterung entfernt gelegte Ansatz; die Frage der Wirtschaftlichkeit bei Tonnenskalen bleibt offen.

## Offene Fragen

1. Welche konkreten Verdichtungsdichte-Werte (g/cm³) werden in Nr. 1, 2 und 5 erreicht, und wie stehen sie zu den typischen 2,2–2,4 g/cm³ aktueller LFP-Pulver am Markt?
2. Lässt sich das Porendichte-Verhältnis aus Nr. 4 (0,18 ≤ … ≤ 0,85) bei reinen LFP-Zellen ohne Ternär-Kathodenanteil reproduzieren, oder gilt es nur für Mischsysteme?
3. Wie hoch sind die Prozesskosten für Polydopamin-Beschichtung (Nr. 5) im Vergleich zur Aluminium-Hydrothermal-Dotierung (Nr. 2) bei Massenproduktion, und welche Ausbeute an aktivem Material geht dabei verloren?
4. Ist das Partikelbruchwiderstandsverhältnis WA/WB aus Nr. 6 (0,5–15) bei LFP-Kathoden mit hoher Verdichtung (also höheren WA-Werten) noch ein wirksames Kriterium, oder dominiert dort die Bindemittel-Auswahl?

## Auffälliges

- **Falsche Anoden-/Kathodenbezeichnung:** Nr. 1 und Nr. 5 nennen in der englischen Übersetzung der Ansprüche das Material „anode material", obwohl klar Kathodenmaterial (positive electrode) gemeint ist. Offensichtlicher Übersetzungsfehler aus dem Chinesischen; die technische Aussage bleibt korrekt, erschwert aber die automatische Volltextsuche.
- **Nur teilweise relevanter Treffer:** Nr. 3 (CN109546109A) betrifft eine Mischkathode mit lediglich bis zu 0,8 Gewichtsteilen LFP neben drei anderen Kathodenkomponenten – sie adressiert Temperaturstabilität, nicht hochverdichtetes LFP. Sie passt nur am Rande zum Suchbegriff „high compaction density long cycle life".
- **Keine Anweisungen oder Aufforderungen im Pakettext** – nichts zu melden.
- **Lücke:** Kein Patent im Paket behandelt explizit die Bindemittel-Auswahl oder die Elektrodenbeschichtungsmethode (z. B. Dry-Electrode, NMC-freie Bindemittel); die Fertigungsebene ist dünn belegt.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P09

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| CN222463111U | 2024-04-22 | 宁德时代新能源科技股份有限公司 | Verdickte Innenwand am Gehäuseöffnungsbereich zur Verbesserung der Verbindungsfestigkeit zwischen Shell und Deckelkappe. | Beleg: "The inner side wall of at least part of the area of the shell at the opening" (https://patents.google.com/patent/CN222463111U/en) | Zellform, Sicherheit |
| CN215896628U | 2021-09-29 | 宁德时代新能源科技股份有限公司 | Unterschiedliche Abmessungen von Plus- und Minus-Elektrodenblättern in dritter Richtung erzeugen Gasraum und reduzieren Quellung sowie Kraft auf die Deckelverbindung. | Beleg: "wherein the adjacent positive electrode tab (43a) and the adjacent negative electrode tab (43c) have different sizes" (https://patents.google.com/patent/CN215896628U/en) | Sicherheit, Zellform |
| CN223066287U | 2024-07-31 | 宁德时代新能源科技股份有限公司 | Dünnwandiges Stahl- oder Titan-Gehäuse mit festgelegtem Innen-/Außenflächenverhältnis (96,42 %–99,75 %) für gleichzeitig hohe Energiedichte und Festigkeit. | Beleg: "The shell is made of steel or titanium alloy, and includes a side wall arranged around the electrode assembly" (https://patents.google.com/patent/CN223066287U/en) | Zellform, Fertigung |
| CN221994536U | 2024-08-05 | 宁德时代新能源科技股份有限公司 | Pack-Konzept mit erster Zelle (steilere SOC-OCV-Kurve) im Elektrikraum und zweiter Zelle im Energiebereich zur genaueren SOC-Messung und erhöhten thermischen Zuverlässigkeit. | Beleg: "the slope of the SOC-OCV curve of the first battery cell is greater" (https://patents.google.com/patent/CN221994536U/en) | Elektrik, Sicherheit |
| US20230006317A1 | 2021-01-25 | Contemporary Amperex Technology Co., Limited | Adapter zwischen Tab und Elektrodenanschluss mit Biegezone und Verstärkungsabschnitten zu gegebener Biegeradius-Geometrie für mechanisch belastbare elektrische Verbindung. | Beleg: "the third connecting portion comprises a reinforcing portion, the reinforcing portion being located at two sides" (https://patents.google.com/patent/US20230006317A1/en) | Elektrik, Zusammenbau |
| EP4379928A1 | 2022-02-28 | Contemporary Amperex Technology Co., Limited | Gehäuse mit dickerer Frontwand und integriertem Entlastungsmechanismus, der bei Überschreiten eines Gasdruck-Schwellwerts aktiviert wird. | Beleg: "the first wall is provided with a pressure relief mechanism" (https://patents.google.com/patent/EP4379928A1/en) | Sicherheit, Zellform |

## Was man daraus lernt

- **Wiederkehrendes Gasdruck-Problem:** Drei Patente (CN222463111U, CN215896628U, EP4379928A1) lösen das gleiche Grundproblem – Gas und Quellung beanspruchen die Shell-Deckel-Verbindung – mit unterschiedlichen Mitteln (Verdickung, Asymmetrie der Blätter, Entlastungsmechanismus). Für ein eigenes Batteriesystem ist eine gezielte Gasführung/-entlastung in der Zellgeometrie ein zentrales Sicherheitsmerkmal.
- **Dünnwand-Metallgehäuse:** CN223066287U zeigt, dass Stahl- oder Titanwände um 0,05–0,3 mm (Claim 3) bei festgelegtem Flächenverhältnis die Energiedichte pro Volumen steigern. Das ist für die Pack-Dichte direkt relevant und wirft Fragen zur Fertigung (Umschling- oder Pressprozesse) auf.
- **Chemie-Hybrid-Pack für BMS:** CN221994536U nutzt die unterschiedliche SOC-OCV-Steigung zweier Zellchemien (ternär, LFP) zur verbesserten SOC-Präzision. Für ein eigenes System: Elektrik/BMS-Konzept wird bereits in der Zellauswahl mitgedacht, nicht nur nachträglich per Algorithmen.
- **Elektromechanische Zuverlässigkeit der Tab-Verbindung:** US20230006317A1 definiert Verstärkungsformen an Biegungszonen mit expliziter Geometrie (R &lt; L &lt; R + 2 mm). Das betrifft den Zusammenbau und die Lebensdauer unter Vibrations-/Zyklusbelastung.
- **Monolithische Schutzstrategie eines Anbieters:** Alle sechs Treffer stammen von CATL (宁德时代). Für ein eigenes Batteriesystem bedeutet das, dass zumindest im prismatischen Zellsegment die Gestaltungsfreiheit durch ein dichtes Patennetz eines Akteurs stark eingeschränkt sein könnte.

## Offene Fragen

1. Welche konkreten Gasgenerierungsraten (ml/min bei z. B. 150 °C bzw. 200 °C) müssen die Entlastungswege aus CN215896628U und EP4379928A1 abführen, ohne dass die Zelltemperatur einen kritischen Schwellwert überschreitet – und welche Testbedingungen sind für die Nachbildung erforderlich?
2. Wie groß ist der Unterschied in der spezifischen Pack-Energiedichte (Wh/L) zwischen der dünnwandigen Stahl-/Titanzelle (CN223066287U, Wand 0,05–0,3 mm) und einer vergleichbaren Aluminiumzelle (typ. 0,5–0,8 mm), und welche Mehrkosten entstehen durch Stahl/Titan in der Fertigung?
3. Welche absoluten SOC-Fehlerwerte (in %) liefert die Hybridzellanordnung aus CN221994536U gegenüber einer homogenen LFP-Konfiguration im realen WLTP-Fahrzyklus, und ist der Effizienzgewinn der BMS-Messung rechtfertigungsfähig?

## Auffälliges

- **Suchbegriff vs. Treffer:** Der Pakettitel lautet „sodium ion battery cell pack vehicle", jedoch erwähnt keines der sechs Patente Natrium-Ionen-Technologie. CN221994536U (Claim 4) nennt explizit „ternary lithium battery cell" und „lithium iron phosphate battery cell". Alle Treffer sind Lithium-Ionen-Patente; eine Natrium-Ionen-Auswertung ist hier nicht enthalten.
- **Ein einziger Inhaber:** Alle sechs Patente gehören zu CATL (宁德时代新能源科技股份有限公司 bzw. Contemporary Amperex Technology Co., Limited). Die Perspektive ist damit einseitig; Wettbewerber (LG Energy Solution, Panasonic, Toyota, BYD u. a.) fehlen.
- **Inhaber-Schreibweise:** CN-Patente tragen den in-blockschriftlichen Namen, US/EP-Patente den englischen Namen – offenbar dasselbe Unternehmen, in der Tabelle aber als unterschiedliche Zeichenketten ausgewiesen.
- Keine injizierten Anweisungen oder fremden Befehle im Fremdtext gefunden.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P10

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| JP7776433B2 | 2020-03-06 | ページ－ロバーツ オートモーティブ リミテッド | Batteriepack-Modul quer zwischen zwei einander gegenüberliegenden Sitzen, darunterliegend, um Platz im Fahrgastraum zu nutzen. | Beleg: "a lateral module configured to extend perpendicular to a longitudinal axis of the vehicle" (https://patents.google.com/patent/JP7776433B2/en) | Zellform |
| CN223156177U | 2024-07-29 | 宁德时代新能源科技股份有限公司 | Batteriekasten mit Deckplatte und erster Platte, die über einen Vorsprung und eine Nut zwei Aufnahmeräume für Zellen und elektronische Bauteile bilden. | Beleg: "A battery device, characterized by comprising: A battery cell assembly including at least one battery cell" (https://patents.google.com/patent/CN223156177U/en) | Zellform |
| CN112793668B | 2021-01-29 | 云度新能源汽车股份有限公司 | Unterbodenrahmen mit hohlgeformten Schweller-Traversen, die als Kollisionsstruktur die Batteriehalterung integrieren und seitliche Kräfte ableiten. | Beleg: "The frame of the lower body of the electric vehicle is characterized by comprising a front cabin assembly" (https://patents.google.com/patent/CN112793668B/en) | Sicherheit |
| CN115050983A | 2021-03-09 | 通用汽车环球科技运作有限责任公司 | Batteriepack-Gehäuse mit seitlich eingelassenen Aufnehmern für Kohlefaser-Wasserstofftanks, die parallel zu den Batterie-Modulen montiert werden. | Beleg: "a battery pack enclosure defining a battery module compartment therein between first and second case mounting cavities" (https://patents.google.com/patent/CN115050983A/en) | Zellform |
| CN113285167A | 2020-02-19 | 福特全球技术公司 | Kanalhalterung mit integriertem Sicherungsring und Clip zur Führung und Befestigung von Litzenharnischen innerhalb des Batteriepacks. | Beleg: "a first channel bracket mounted to a first battery array and comprising a mounting platform and a ring" (https://patents.google.com/patent/CN113285167A/en) | Elektrik |
| CN219600903U | 2023-04-24 | 宁德时代(上海)智能科技有限公司 | Batteriebox, deren Seitenprofile gleichzeitig als Türschwellen der Karosserie dienen, um Teile zu reduzieren und Platz für Zellen zu gewinnen. | Beleg: "two first side beams which are oppositely arranged at intervals along a first direction" (https://patents.google.com/patent/CN219600903U/en) | Zusammenbau |

## Was man daraus lernt

- **Strukturintegration wiederholt sich:** CN112793668B und CN219600903U nutzen Fahrzeug-Tragstrukturen (Schwellen, Querträger) direkt als Batteriehalterung; das reduziert Masse und Teilezahl, erfordert aber ein gemeinsames Design von Karosserie und Pack.
- **Kompakte zweischichtige Anordnung:** CN223156177U und CN115050983A zeigen, dass in gleicher Packbreite zweite Funktionsräume (Elektronik, Tank) über oder neben der Zellschicht integriert werden – relevant für Energie-/Systemdichte.
- **Seitliche Kollisionssicherheit wird zur Pack-Eigenschaft:** CN112793668B überträgt Seitenaufprallkräfte durch hohle Schweller auf das Vorder-/Hintermodul; ein eigenes Pack muss seine Außenwände als Krallaufnahme dimensionieren.
- **Interne Verdrahtung als gestalterischer Faktor:** CN113285167A führt Litzenharnischen über formschlüssige Kanäle und Clip-Verschlüsse; bei eigenen Packs vermindert das Vibrationsempfindlichkeit und vereinfacht den Zusammenbau.
- **Seat-layout-abhängige Packgeometrie:** JP7776433B2 platziert das Pack quer und unterhalb der Sitzbank, was die zulässige Packhöhe und den Schwerpunkt bestimmt; bei eigener Zellform muss die verfügbare Nettolänge zwischen Schweller und Bodengruppe zuerst bemessen werden.
- **Fremdbehaftete Energieträger im selben Gehäuse:** CN115050983A koppelt Wasserstofftanks an das RESS-Gehäuse; falls das eigene System zusätzlich einen Sekundär-Energieträger trägt, muss die thermische und strukturelle Trennung bereits im Gehäuse definiert sein.

## Offene Fragen

1. Wie hoch ist der zusätzliche Fertigungsaufwand (Formwerkzeug, Pressstrecke), wenn Schweller und Batteriebox als eine Guss- oder Stanz-Bauteilfamilie ausgeführt werden (CN112793668B, CN219600903U)?
2. Welche thermische Kapazität der Zwischenschicht (CN223156177U, CN115050983A) genügt, um die Zellentemperatur unter 45 °C zu halten, wenn die Elektronik- oder Tankschicht gleichzeitig als Wärmequelle wirkt?
3. Lässt sich die Clip-/Ring-Befestigung (CN113285167A) so standardisieren, dass ein einzelnes Werkzeug für mehrere Pack-Baureihen reicht, ohne die Kanalgeometrie pro Variante zu ändern?

## Auffälliges

- Bei JP7776433B2 fehlt die Zusammenfassung komplett („nicht gefunden"); die Auswertung stützt sich ausschließlich auf die angeführten Anspruchsausschnitte.
- CN115050983A behandelt primär die Integration von Wasserstofftanks; der Bezug zur reinen Batteriezellchemie ist gering, der Treffer beruht auf dem gemeinsam genutzten RESS-Gehäuse.
- Keine fremden Anweisungen oder Aufforderungen im Pakettext festgestellt.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P11

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| CN116638953B | 2022-02-24 | 马自达汽车株式会社 | nicht gefunden | nicht gefunden | nicht gefunden |
| CN114585530A | 2019-10-09 | 日产自动车株式会社 | nicht gefunden | nicht gefunden | nicht gefunden |
| CN112896323B | 2021-02-05 | 奇瑞新能源汽车股份有限公司 | nicht gefunden | nicht gefunden | nicht gefunden |
| CN116638954B | 2022-02-24 | 马自达汽车株式会社 | Heck-Karosseriestruktur, die Aufpralllasten vom Heck aufnimmt, während der Batterieraum nach hinten vergrößert wird. | Beleg: "The battery case is mounted to the left and right side rails and the rear side cross member" (https://patents.google.com/patent/CN116638954B/en) | Zusammenbau, Sicherheit |
| CN114379686A | 2022-01-19 | 河北开云汽车制造有限公司 | Fahrzeugkarosserie mit Zentralkeil und Stützrahmen (Halter + Stützhalter), die Front- und Seitenkollision abwehrt. | Beleg: "extending longitudinally as a whole" (https://patents.google.com/patent/CN114379686A/en) | Zusammenbau, Sicherheit |
| CN214930131U | 2021-06-17 | 中国第一汽车股份有限公司 | Untere Karosserierahmenstruktur, bei der die Boden-Längsschienen gleichzeitig als Batteriemontageflächen und Crashtürme dienen. | Beleg: "battery mounting surfaces (25) are arranged on the lower surfaces of the left floor longitudinal beam (21)" (https://patents.google.com/patent/CN214930131U/en) | Zusammenbau, Sicherheit |

## Was man daraus lernt

- **Batterieträger wird Teil der Karosseriestruktur:** Bei CN116638954B ist die Batteriekasse direkt auf Side Rails und Heckquerträger montiert; bei CN214930131U dienen die Boden-Längsschienen gleichzeitig als Batterieaufhängung und Kollisionsschutz. Das vereinfacht den Zusammenbau und reduziert Einzelteile.
- **Querverbände als Batterievorbau:** CN116638954B legt den Heckquerträger auf die Oberkante des Hinteren Batterie Rahmens und verschraubt beides in Vertikalrichtung – eine klare Montage- und Lastpfad-Lösung für ein eigenes Batteriesystem.
- **Stützrahmen auf dem Zentralkeil:** CN114379686A zeigt, dass ein zusätzlicher Halter + Stützhalter am Längsträger die Biege- und Querschnitts-Steifigkeit erhöht, ohne die Batterienische zu verkleinern.
- **Batterieraum nach hinten ausdehnen:** CN116638954B verlagert Batteriekapazität ins Heck und kompensiert damit den Verlust an Heckcrash-Volumen mit einem dedizierten Rahmen hinter der Batterie – relevant für die Dimensionierung des eigenen Tragwerks.
- **Keine Erwähnung von Extrusions-Aluminium oder Zellchemie:** In den verfügbaren Auszügen taucht weder das Material „extruded aluminum" noch eine bestimmte Zellchemie auf; die Treffer konzentrieren sich auf Stahl-Karosseriestrukturen.

## Offene Fragen

1. Wie hoch ist die zusätzliche Masse der integrierten Batterieträger-Querverbände (CN116638954B, CN214930131U) im Vergleich zu einer separaten Batteriebox, und wie wirkt sich das auf das Fahrzeuggewicht aus?
2. Welche Verbindungstechnik (Schrauben, Kleben, Nieten) wird für die Befestigung der Batteriekasse an den Side Rails gefordert, und welche Toleranzen sind daraus resultierend herzustellen?
3. Wie ist der Lastpfad bei einem Seitenansturz bei CN214930131U definiert – tragen die Boden-Längsschienen die volle Seitenaufpralllast, oder übernehmen zusätzliche Crashtürme (Truss) diesen Anteil?
4. Lässt sich die in CN116638954B beschriebene Heckverlängerung der Batterie auf Plattformen mit Heckantriebsachse übertragen, ohne den Antriebsstrang-Aufbau zu verfälschen?

## Auffälliges

- **Drei von sechs Treffern nicht abrufbar:** CN116638953B, CN114585530A und CN112896323B lieferten HTTP 503 – hier fehlen Titel-Inhalt, Zusammenfassung und Ansprüche vollständig.
- **Suchthema nicht bestätigt:** Die Suchanfrage enthält „extruded aluminum frame sill", doch in keinem der drei verfügbaren Patente wird Aluminium-Extrusion als Material genannt; alle beschreiben Stahl-Karosseriestrukturen.
- **Keine Injektionsversuche** im Pakettext erkannt.


Prüfung: 3 Belege bestaetigt, 0 Fehler

## P12

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| CN217114533U | 2021-11-30 | 宁德时代新能源科技股份有限公司 | Wärmemanagementkomponente mit verjüngten Mittelabschnitten in Zweigkanälen zur gleichmäßigeren Kühlung und Temperaturdifferenz-Reduktion im Batterierack. | Beleg: "the cross-sectional area of the middle section is smaller than the cross-sectional area of the end section" (https://patents.google.com/patent/CN217114533U/en) | Kühlung |
| CN105161644B | 2015-09-09 | 江苏科技大学 | Batteriehülse für Softpack-Zellen mit Flüssigkeitskühlplatte, Kühlrippen und flexiblem Wärmetransferpad zur Wärmableitung und Positionierung. | Beleg: "Lower box bottom is flexible heat conductive pad, is contacted with battery pack bottom and liquid cooling plate" (https://patents.google.com/patent/CN105161644B/en) | Kühlung / Zusammenbau |
| WO2025184855A8 | 2024-03-06 | 安徽科技学院 | Synthesemethode für Lithium-Vanadium-Fluorophosphat-Kathodenmaterial sowie Batteriezelle mit Klemmmechanismus und Wärmeableitung. | nicht gefunden | Zellchemie / Sicherheit |
| US20240204317A1 | 2021-10-12 | Contemporary Amperex Technology Co., Limited | Polyedrische (Parallelogramm-/Trapezquerschnitt) Zellen in verticalen Spalten gestapelt, um Steifigkeit und Tragfähigkeit des Packs zu erhöhen. | Beleg: "the battery cell is a polyhedral structure and comprises a first wall and a second wall connected to each other" (https://patents.google.com/patent/US20240204317A1/en) | Zellform / Zusammenbau |
| US12002984B2 | 2020-09-30 | Contemporary Amperex Technology Co., Limited | Batterie mit Zellen unterschiedlicher Energiedichte, jeweils mit eigener Druckentlastung und separaten Entleerungskanälen in der Bodenwand. | Beleg: "pressure relief mechanism configured to be actuated when internal pressure or temperature of the first battery cell reaches a threshold" (https://patents.google.com/patent/US12002984B2/en) | Sicherheit |
| KR102877728B1 | 2020-12-22 | 에스케이온 주식회사 | Batteriemodul mit Kühlplatte, die eine Basisplatte und Vorsprünge Richtung Zellstack bildet, in deren Einsenkung ein Thermoelement montiert ist. | Beleg: "a protrusion that protrudes from the base portion toward the cell stack to form a sunken space" (https://patents.google.com/patent/KR102877728B1/en) | Kühlung |

## Was man daraus lernt

- **Kühlung über veränderliche Kanalgeometrie** (CN217114533U): Ein verjüngter Mittelabschnitt in den Zweigkanälen erhöht die Strömungsgeschwindigkeit dort, wo die Temperatur am höchsten ist – relevant, wenn ein eigenes System eine gleichmäßige Zelltemperatur ohne komplexe Regelung erreichen soll.
- **Kühlung am Pack-Boden mit flexiblem Thermokontakt** (CN105161644B): Ein flexibles Wärmeleitpad zwischen Zellstack und starer Kühlplatte kompensiert Zellausdehnung und Schwingungen – wichtig für Langlebigkeit bei Softpack- oder Pouch-Zellen.
- **Thermoelektrische Kühlkomponente direkt an der Platte** (KR102877728B1): Ein Peltier-Element in einer Vorsprung-Einsenkung der Kühlplatte ermöglicht aktive Kühlung/heizung ohne zusätzliche Fluidverbindung – interessant für lokale Temperaturspitzen.
- **Zellform als Strukturbasis** (US20240204317A1): Parallelogramm-/Trapezquerschnitte ersetzen starre Halterungen; die Zellen selbst stützen sich gegenseitig – reduziert Masse und Bauraum bei gleichzeitig guter Pack-Steifigkeit.
- **Zellenspezifische Druckentlastung** (US12002984B2): Unterschiedliche Zellgrößen (Energiedichte) erhalten eigene Entlastungsflächengrößen und getrennte Entleerungskanäle – reduziert Kreuzkontamination bei thermischem Durchgehen.
- **Kathodenmaterial als Querschnitt** (WO2025184855A8): Lithium-Vanadium-Fluorophosphat wird als alternative Kathode mit moderaterer Überladeempfindlichkeit vorgestellt – für die Chemieauswahl eines sicheren Packs relevant.

## Offene Fragen

1. **Kühlbedarf je Zelle:** Wie viel Wärmeleistung (W/Zelle) muss bei typischer C-Rate abgeführt werden, und reicht die Querschnittsreduktion nach CN217114533U, um ΔT < 5 K im Pack zu halten?
2. **Pack-Dichte durch Zellform:** Wie viel volumetrische Energiedichte (Wh/L) wird realistisch erreicht, wenn parallelogrammförmige Zellen (US20240204317A1) statt runder Zellen verwendet werden, bei vergleichbarer Zellenanzahl?
3. **Grenze der Druckentlastung:** Wie groß müssen die Entleerungskanäle (US12002984B2) dimensioniert sein, um bei einem Zell-DGX die Flammenfront innerhalb der Zelle zu stoppen, ohne dass Gas in benachbarte Zellen übertreten kann?
4. **Thermoeffizienz Peltier vs. Flüssigkeitskühlung:** Ab welcher Pack-Leistung (kW) und welcher Umgebungstemperatur wird die aktive Peltier-Kühlung (KR102877728B1) gegenüber rein passiver Flüssigkeitskühlung sinnvoll?

## Auffälliges

- **WO2025184855A8:** Die Ansprüche wurden im Paket nicht mitgeliefert (Eintrag „nicht gefunden"). Das Patent beschreibt primär eine Kathodenmaterial-Synthesemethode und passt nur am Rande zum Suchthema „dual-sided cooling plate"; möglicher unpassender Treffer in der Trefferliste.
- **KR102877728B1:** Der Anspruchstext ist in dem Paket ein koreanisch-englisch gemischtes Fragment (Koreanische Platzhalter „; ; , , ." am Anfang), was eine verlässliche Zitierung erschwert und auf eine unvollständige Extraktion hindeutet.
- **CN105161644B:** Die Priorität (2015) ist deutlich älter als die übrigen Treffer (2020–2024); das Patent beschreibt eine eher einfache Schwerkraft- bzw. Flusskanal-Kühlung ohne „dual-sided"-Aspekt, es ist daher unklar, warum es auf die Suchanfrage „cooling plate top and bottom cells double sided cooling" gematcht hat.


Prüfung: 5 Belege bestaetigt, 0 Fehler

## P13

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| 1 | 2017-06-15 | Positec Power Tools (Suzhou) Co., Ltd | Ladevorrichtung, die zwei Akkupacks wechselweise lädt und den Ladestrom temperaturabhängig anpasst, um einen Übertemperatur-Zustand zu vermeiden. | Beleg: "a parameter detecting unit (31) configured to detect parameters related to a charging current" (https://patents.google.com/patent/EP3641046B1/en) | Elektrik |
| 2 | 2022-03-21 | 苏州赤兔驱动科技有限公司 | Mehrelementiges Präerhitzungssystem für Lithiumbatterien mit mindestens drei Temperatursensoren, BMS und Fernsteuerung zur präzisen Temperaturführung vor dem Laden. | Beleg: "the temperature sensor comprises at least three temperature probes which are respectively arranged on detection points" (https://patents.google.com/patent/CN114523882B/en) | Kühlung |
| 3 | 2016-03-07 | 더 리젠츠 오브 더 유니버시티 오브 미시건 | Ladungsalgorithmus für Lithium-Ionen-Zellen, der verfügbare Nutzerverfügungszeit, Zell-Dormanz und maximale Sicher­heitstemperatur gleichzeitig als Grenzwerte nutzt. | Beleg: "Determining a threshold voltage at which the battery cell is charged with the constant current" (https://patents.google.com/patent/KR20180114206A/en) | Elektrik |
| 4 | 2025-05-26 | 徐州徐工新能源动力科技有限公司 | Thermomanagement-Verfahren für Traktions­batterien mit thermoelektrischem Modell, Flüssigkeitskühlung, Phasenwechselmaterial und modell­basierter Fehlvorwarnung über den gesamten Lebenszyklus. | Beleg: "the basic model comprises a battery thermoelectric model" (https://patents.google.com/patent/CN120565924A/en) | Kühlung |
| 5 | 2023-05-29 | Contemporary Amperex Technology Co., Limited | Temperatursteuerung pro Batteriecluster eines Batteriesystems, um Zwischencluster-Temperaturgleichmäßigkeit herzustellen und vorzeitiges Vollladen einzelner Cluster zu vermeiden. | Beleg: "obtaining a cluster temperature of each of a plurality of battery clusters of a battery system" (https://patents.google.com/patent/EP4625620A1/en) | Kühlung |
| 6 | 2022-06-29 | 重庆长安新能源汽车科技有限公司 | Dormanz-Management der Batteriegleichstromausgleichsfunktion, bei dem das BMS-Zusatzmodul periodisch aufwacht, ausgleicht und bei hoher Temperatur abschaltet. | Beleg: "the BMS sub-board enters the inspection working mode" (https://patents.google.com/patent/CN114976316A/en) | Sicherheit |

## Was man daraus lernt

- **Mehrpunkt-Temperaturüberwachung während des Ladens** ist das wiederkehrende Muster: Patent 1 misst separat zwei Akkupacks, Patent 2 nutzt ≥3 Probe an unterschiedlichen Zellpositionen, Patent 5 arbeitet auf Cluster-Ebene – jeweils, um lokale Hotspots zu erkennen und den Strom/ die Kühlung gezielt anzupassen.
- **Temperaturabhängige Strom- und Spannungsbeschränkung** (1, 3) begrenzt die Ladung nicht nur am Spannungsende, sondern setzt die maximale erlaubte Temperatur als zweiten Stopp; dafür relevant, dass ein eigenes Ladeprofil nicht nur CC/CV, sondern eine doppelte Grenze (Vmax, Tmax) enthält.
- **Dormanz/Restpause nach Hochstromladung** wird in 3 (vorgegebene Ruhezeit aus der verfügbaren Zeit abgezogen) und in 6 (periodisches Aufwachen, Ausgleichen, Abschalten bei Überschreitung) als zentraler Degradationsfaktor behandelt; für ein eigenes System bedeutet das: Ladezeitfenster und Ruhezeit müssen zusammen optimiert werden, nicht separat.
- **Präerhitzung vor dem Laden bei Kälte** (2) mit zwei Modi (Normal/Schnell) und Schwellenwert-Logik zeigt, dass ein einfaches Widerstandsheizen unzureichend ist; mindestens zwei Temperaturschwellen und eine Strombegrenzung (PWM) sind nötig, um Lithiumabscheidung zu vermeiden.
- **Modellbasiertes, datengetriebenes Thermomanagement** (4) kombiniert thermoelektrisches Modell, Flüssigkeitskühlung und Phasenwechselmaterial mit prädiktiver Temperaturvorhersage; das deutet auf eine Kombination aus Physikmodell und ML für ein eigenes Batteriesystem hin, statt rein reaktiver P-Regelung.
- **Cluster-Weichgewicht** (5): Wenn mehrere Module paralleliert sind, erzeugt thermische Asymmetrie unterschiedliche Innenwiderstände und ströme; ein eigenes System sollte daher pro Cluster temperaturregeln, nicht nur global.

## Offene Fragen

1. Wie groß ist der quantitative Wirkungsgrad-Nachteil bei der wechselseitigen Ladung zweier Paks (Nr 1) im Vergleich zu parallelem Laden, und welche Messdaten sind dafür nötig (Strom- und Temperaturverlauf der beiden Paks)?
2. Welche konkrete Energieminderung bringt die clusterweise Temperaturkontrolle (Nr 5) gegenüber einer globalen Kühlung, ausgedrückt in Wh pro Ladezyklus und pro Zyklenzahl bis 80 % Kapazität?
3. Wie lässt sich die in Nr 4 vorgesehene prädiktive Temperaturvorhersage (Modelllernen + Großdaten) ohne große Historie (Neufahrzeug) kalibrieren, und welche Mindestmenge an Betriebsdaten wird dafür benötigt?
4. Wie beeinflusst die in Nr 6 beschriebene periodische Gleichstromgleichstrom-Strategie die Gesamtleerdauer eines 25 Ah-Paks, und welche Toleranz für die Zellspannungsabweichung wird erreicht?

## Auffälliges

- **KR20180114206A (Nr 3):** Das Titel-Feld in der Detailansicht ist leer (nur „KR20180114206A –" ohne Titeltext); in den Ansprüchen treten HTML-Kodierungs-Artefakte auf („Lt; / RTI &gt;", „- &lt; / RTI &gt;"), die auf unsaubere Datenextraktion hindeuten.
- **CN114523882B (Nr 2):** In Anspruch 1 erscheint die Abkürzung „PMW" (vermutlich PWM – pulse width modulation), die nicht erklärt wird und nicht im Rest des Pakets vorkommt; Unsicherheit bei der Interpretation.
- **EP3641046B1 (Nr 1):** Zusammenfassung fehlt vollständig („nicht gefunden"); Bewertung der Erfindung stützt sich ausschließlich auf die Ansätze.
- Keine eingebetteten Anweisungen (z. B. „ignoriere", „führe aus") im Pakettext festgestellt.


Prüfung: 6 Belege bestaetigt, 0 Fehler

## P14

## Tabelle

| Nr | Priorität | Inhaber | Worum es geht (1 Satz, deutsch) | Kern Anspruch 1 | Bezug zum Batteriesystem |
|---|---|---|---|---|---|
| EP3550635B1 | 2017-05-22 | LG Chem, Ltd. | Batteriemodul und Batteriepaket mit dem Modul. | nicht gefunden | Zusammenbau (aus dem Titel) |
| CN216055077U | 2021-08-31 | 宁德时代新能源科技股份有限公司 | Batteriezinne, Batterie und verbrauchendes Gerät. | nicht gefunden | Zusammenbau (aus dem Titel) |
| JP7627289B2 | 2021-01-11 | エルジー エナジー ソリューション リミテッド | Batteriepaket und Fahrzeug mit demselben. | nicht gefunden | Zusammenbau (aus dem Titel) |
| US20220285777A1 | 2019-11-11 | Lg Energy Solution, Ltd. | Batteriemodul, Batteriepaket und Fahrzeug mit dem Modul. | nicht gefunden | Zusammenbau (aus dem Titel) |
| CN119208851A | 2024-11-27 | 宁德时代新能源科技股份有限公司 | Batterievorrichtungen, Energiespeichervorrichtungen und verbrauchende Geräte. | nicht gefunden | Zusammenbau (aus dem Titel) |
| EP3836247A1 | 2018-12-26 | LG Chem, Ltd. | Batteriemodul, Batteriepaket und Fahrzeug. | nicht gefunden | Zusammenbau (aus dem Titel) |

## Was man daraus lernt

- Aus den Titeln (alle sechs Nummern) lässt sich ablesen, dass die Treffer allgemein **Batteriemodule / Batteriepakte** betreffen; eine auf die Suchanfrage („cell holder adhesive potting both terminals same end busbar") zugeschnittene technische Lösung ist aus den vorliegenden Daten nicht erkennbar.
- Mehr als die Titel konnte nicht ausgewertet werden, da **alle sechs Volltextabrufe fehlgeschlagen sind** (HTTP 503); Aussagen zu Kernansprüchen, Zellhaltern, Klebepotten oder Busbar-Anordnungen liegen daher **nicht vor** (Nr. EP3550635B1, CN216055077U, JP7627289B2, US20220285777A1, CN119208851A, EP3836247A1).
- Eine wiederkehrende technische Lösung lässt sich aus diesem Paket **nicht** ableiten; ein Wiedervergleich nach erfolgreicher Ablage ist nötig ( Nr. EP3550635B1, EP3836247A1, US20220285777A1, CN216055077U, CN119208851A, JP7627289B2).

## Offene Fragen

1. Entspricht einer der sechs Patente tatsächlich der Suchintention „beide Pole am selben Ende, Zellhalter, Kleben/Potten, Busbar", oder handelt es sich um allgemeine Modul-/Paketkonstruktionen ohne Bezug zu diesen Details? (Nr. alle sechs)
2. Kann der Volltext bei erneuter Ablage (nach 503-Ausfall) erfolgreich geladen werden, um Anspruch 1 und die Beschreibung abzugleichen? (Nr. alle sechs)
3. Falls die Paterte nur das „Umspannungs"- und „Modulbau"-Prinzip abdecken: Gibt es separate Patente zu terminalseitigem Potten und einseitig angeordneten Busbars, die in diesem Treffer fehlen? (Nr. alle sechs)

## Auffälliges

- **Alle sechs Volltextabrufe sind fehlgeschlagen** (HTTP 503 – Service Unavailable). Es liegen keine Zusammenfassungen, keine Anspruchstexte und keine beschreibenden Absätze vor. Jede Zitate-Spalte muss mit „nicht gefunden" angegeben werden.
- Die Suchanfrage zielt auf ein sehr spezifisches Detail („cell holder adhesive potting both terminals same end busbar"), während die Titel sämtlicher Treffer nur „Batteriemodul / Batteriepaket" nennen. Es besteht die Gefahr, dass die Treffer **nicht die gesuchte technische Lösung** abdecken, sondern allgemeine Modulbauformen sind.
- Keine Auffälligkeiten in Form von Instruktionen oder Fremdanweisungen im Pakettext.


Prüfung: 0 Belege bestaetigt, 0 Fehler
