# Auftrag an PI: Wissensaufbau zu einem Thema (Batteriesystem)

## Erklärung
Das Thema befasst sich mit wieder aufladbaren elektrischen Energiespeichersystemen, den sogenannten REESS, die in Elektrofahrzeugen die elektrische Antriebsunterstützung bereitstellen. REESS speichern elektrische Energie in Zellen und geben sie bei Bedarf an den Elektromotor ab. Für die Fahrzeugsicherheit ist entscheidend, dass die gespeicherte Energie und die elektrischen Spannungen bei einem Unfall keine Gefahr darstellen. Daraus ergeben sich Anforderungen an Isolationswiderstände, automatische Trennungen und die Begrenzung von Elektrolytleakage. Das System umfasste neben den Zellen auch Elektrolyte, elektronische Kontrollen und thermische Management-Systeme.

## Kennwerte
| Größe | Wert | Einheit | Beleg |
|---|---|---|---|
| Hochspannung (DC) | > 60 | V | "High voltage" means the classification of an electric component or circuit, if its working voltage is > 60 V (file:///home/cae/hermes/batterie/quellen/normen/R094r4e.pdf) |
| Hochspannung (AC) | > 30 | V | "High voltage" means the classification of an electric component or circuit, if its working voltage is > 30 V (file:///home/cae/hermes/batterie/quellen/normen/R094r4e.pdf) |
| Isolation resistance | 500 | Ω/V | "Isolation resistance between the high voltage bus and the electrical chassis shall have a minimum value of 500 Ω/V" (file:///home/cae/hermes/batterie/quellen/normen/R094r4e.pdf) |
| Total Energy (TE) | 0.2 | J | "Total Energy (TE) on the high voltage buses shall be less than 0.2 joules" (file:///home/cae/hermes/batterie/quellen/normen/R094r4e.pdf) |

## Bedeutung für unser Batteriesystem
- Folgerung: Die Hochspannungsgrenzen erfordern eine sorgfältige Isolierung unserer Batteriekomponenten, um Berührungsspannungen zu vermeiden.
- Folgerung: Die Isolationswiderstände von mindestens 500 Ω/V müssen in der Konstruktion sichergestellt werden.
- Folgerung: Die Begrenzung der Gesamtenergie auf 0,2 J nach einem Impact beeinflusst die Auslegung von Kondensatoren und der automatischen Trennung.
- Folgerung: Die Anforderungen an keine Elektrolytleckage in den Passagierbereich verlangen ein dichtes Gehäuse und zuverlässige Dichtungen.

## Offene Fragen
- Welche Elektrolytart (aqueous oder non-aqueous) ist in unserer Batterie vorgesehen?
- Wie ist die automatische Trennfunktion in unser System integriert?
- Welche Isolationsüberwachung wird während des Betriebs eingesetzt?
- Wie wird die Thermomanagement-Strategie bei einem Impact-Event gestaltet?

## Auffälliges
nichts
