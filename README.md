# Smart Finance Analyzer

Smart Finance Analyzer ist ein CLI-basiertes Python-Tool zur Analyse persönlicher Finanzdaten aus CSV-Dateien. Das Programm liest Transaktionen ein, berechnet Einnahmen, Ausgaben, Monatsbilanzen und eine einfache Prognose und erstellt daraus automatisch einen strukturierten Finanzbericht.

## Kurzprofil für Recruiter

- Thema: Finanzdaten, CSV-Verarbeitung, Reporting und einfache Prognose
- Technologie: Python-Standardbibliothek, interaktives CLI, Textreport
- Eingabe: realistische Beispieltransaktionen in `transactions.csv`
- Ausgabe: vollständiger Finanzbericht als Terminalausgabe und Textdatei
- Fokus: saubere Datenvalidierung, strukturierte Auswertung und nachvollziehbare Ergebnisse

## Funktionen

- Transaktionen aus CSV-Dateien laden und validieren
- Gesamteinnahmen, Gesamtausgaben und Netto-Überschuss berechnen
- Ausgaben nach Kategorien sortieren
- Monatsbilanzen erstellen
- Prognose für den nächsten Monat berechnen
- Fehler bei fehlenden Dateien, falschen Spalten oder ungültigen Beträgen abfangen
- Textreport automatisch speichern

## Schnellstart

Projekt aus dem Repository-Root starten:

```bash
python3 main.py
```

Danach können die Standardwerte einfach mit Enter bestätigt werden:

```txt
Name der CSV-Datei eingeben [transactions.csv]:
Name der Report-Datei eingeben [report.txt]:
```

Erwartete Terminalausgabe:

```txt
Smart Finance Analyzer wird gestartet...
[1/5] Lade Transaktionen aus CSV...
✓ 132 Transaktionen erfolgreich geladen.
[2/5] Berechne Gesamtübersicht...
✓ Einnahmen: 37140.00 € | Ausgaben: 20870.00 € | Überschuss: 16270.00 €
[3/5] Analysiere Ausgaben nach Kategorien...
✓ 12 Kategorien gefunden: Miete, Lebensmittel, Freizeit, Sparen, Versicherung, Mobilität, Internet, Kleidung, Telefon, Bildung, Geschenke, Gesundheit
[4/5] Berechne Monatsbilanzen und Prognose...
✓ 12 Monate analysiert. Prognose: 1355.83 €
```

Ein längerer Terminal-Mitschnitt liegt hier:

```txt
examples/terminal_output.txt
```

## Eingabeformat

Die CSV-Datei benötigt diese Spalten:

```csv
month,type,amount,category
Januar,income,2850.00,Gehalt
Januar,expense,820.00,Miete
Januar,expense,345.00,Lebensmittel
```

`type` muss entweder `income` oder `expense` sein.

## Ausgaben

Der generierte Report enthält:

- Gesamtübersicht mit Einnahmen, Ausgaben und Netto-Überschuss
- Kategorienanalyse mit Prozentwerten
- Monatsbilanzen
- Prognose für den nächsten Monat
- Hinweis, ob ein positiver finanzieller Puffer erwartet wird

Standardmäßig wird der Report unter `report.txt` gespeichert. Diese Datei ist generiert und wird nicht versioniert.

## Projektstruktur

```txt
.
├── main.py
├── transactions.csv
├── examples/
│   └── terminal_output.txt
└── README.md
```

## Technische Ziele

- keine externen Abhängigkeiten
- klar lesbare Python-Funktionen
- robuste CSV-Validierung
- nachvollziehbare Berechnungsschritte
- einfache Bedienung über das Terminal

## Bewerbungsbezug

Das Projekt zeigt grundlegende, aber saubere Datenverarbeitung mit Python: Einlesen von CSV-Daten, Validierung, Aggregation, Report-Erstellung und einfache Prognose. Durch die realistischen Beispieltransaktionen ist das Ergebnis für Recruiter direkt nachvollziehbar, ohne dass das Projekt ausgeführt werden muss.
