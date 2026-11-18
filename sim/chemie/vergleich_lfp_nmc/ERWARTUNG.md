| Dok.-Nr. | ERW-C0 | Version | 1.0 | Status | Entwurf |
|---|---|---|---|---|---|
| Titel | Erwartung Chemievergleich LFP gegen NMC (1500 kg, 400 km) | Ersteller | Claude Opus (KI) | Prüfer | – (Mensch offen) |

> **KI-generiert.** Festgelegt vor der Rechnung (AGENTS.md Nr. 3, REQ-D06). Eingaben: `eingaben.json`. Vorgaben Autor 2026-11-16: 1500 kg, 400 km, „LFP oder NMC sollte verglichen werden“. Anforderungen REQ-P01, P02, P06, P07, P10.

## Frage
Welche Chemie ergibt bei 1500 kg und 400 km das bessere Pack? Kriterien: Masse, Zellzahl und Verschaltung, Zyklen, Bauraum, Kälte, Sicherheit. Wie stark hängt die Antwort an Annahmen?

## Erwartung (Schätzung vor der Rechnung)
1. **Energie:** Nutzbar etwa 68 kWh, brutto etwa 74 kWh in Fall A, für beide Chemien gleich. In Fall B 15–25 % mehr, weil die Batteriemasse den Verbrauch erhöht. Die Iteration konvergiert in wenigen Schritten.
2. **Masse:** Die belegten Bänder der Zelle überlappen (LFP 185–210, NMC 150–275 Wh/kg). Erwartet wird deshalb **kein klarer Massenvorteil** aus belegten Daten. Packmasse beider Chemien etwa 400–600 kg. NMC ist nur am oberen Bandende deutlich leichter.
3. **Grenze 30 %** (Annahme): In Fall A nahe an der Grenze oder darüber, in Fall B eher darunter.
4. **Zellzahl:** Bei 800 V etwa 250 Zellen in Reihe (LFP) gegen etwa 220 (NMC).
5. **Zyklen:** Bedarf etwa 1000 Vollzyklen. LFP erfüllt das klar. NMC erfüllt es nach dem allgemeinen Li-Ion-Band (400–1200) **nicht sicher**, der Beleg ist aber nicht NMC-spezifisch.
6. **Bauraum:** Nötig etwa 214 Wh/L (Pack) im angenommenen Bauraum. Für LFP-Blade ist keine Aussage möglich (Lücke). Ergebnis „offen“, nicht „passt nicht“.
7. **Deutung vorab:** Aus belegten Daten spricht die Masse für keine Seite klar. Zyklen, Sicherheit und Vorbild sprechen für LFP, die Kälte spricht für NMC. Entscheidend wird der Wh/L-Wert der Blade-Zelle (Zerlegungsstudie, W19).

## Was als verfehlte Erwartung gilt
- Masse: Ein Band liegt vollständig unter dem anderen (kein Überlapp).
- Fall B: Die Energie steigt um mehr als 35 % oder die Iteration konvergiert nicht.
- Die Zellzahl weicht um mehr als 10 % von Punkt 4 ab.
