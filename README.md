# Smart Finance Analyzer

![Python CI](https://github.com/JojoMab/smart-finance-analyzer-for-csv-data-/actions/workflows/python-ci.yml/badge.svg)

Dieses Bewerberprojekt analysiert synthetische Finanzdaten aus CSV-Dateien. Es validiert Buchungen, berechnet eine Budgetampel, wertet Ausgaben nach Kategorien aus und erzeugt einen Monatsreport.

## Bewerbungskontext

Das Projekt passt zu dualen Studiengängen in Wirtschaftsinformatik, Informatik und Finanz-IT. Es ist relevant für Allianz, Generali, Atruvia, Finanz Informatik und Bayerische Versorgungskammer.

## Tech Stack

- Python 3.11
- CSV-Verarbeitung
- Datenvalidierung
- Budgetampel
- Unit Tests
- GitHub Actions

## Funktionen

- synthetische Transaktionen laden
- Pflichtfelder, Beträge und Datumsformat prüfen
- Kategorienanalyse durchführen
- Budgetstatus ROT/GELB/GRÜN berechnen
- Monatsreport als TXT erzeugen

## Projektstruktur

```txt
smart-finance-analyzer-for-csv-data-/
├── main.py
├── validator.py
├── budget_analyzer.py
├── category_analyzer.py
├── report_generator.py
├── data/transaction_data.csv
├── tests/
└── docs/
```

## Schnellstart

```bash
python main.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Beispielausgabe

```txt
Smart Finance Analyzer abgeschlossen.
Report: reports/monthly_report.txt
```

## Hinweis zum Repository-Namen

Der aktuelle Repository-Name endet technisch bedingt mit einem Bindestrich. Für die öffentliche Wirkung wird eine Umbenennung in `smart-finance-analyzer` empfohlen.

## Hinweis auf synthetische Daten

Alle Buchungen sind synthetisch. Das Projekt verarbeitet keine echten Finanzdaten.

## English Summary

Smart Finance Analyzer is an applicant portfolio project for CSV-based financial data analysis. It demonstrates validation, budget status logic, category analysis and reporting with synthetic data.
