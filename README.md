# Smart Finance Analyzer 💰

Ein Command-Line-Tool zur automatischen Analyse persönlicher Finanzdaten aus einer CSV-Datei.

## 📋 Projektübersicht

Dieses Python-Projekt liest Einnahmen und Ausgaben aus einer CSV-Datei ein,
analysiert sie nach verschiedenen Kriterien und erstellt einen strukturierten
Finanzbericht – sowohl als Terminal-Ausgabe als auch als gespeicherte Textdatei.

## 🗂️ Projektstruktur

```
smart_finance_analyzer/
│
├── main.py              # Hauptprogramm mit allen Funktionen
├── transactions.csv     # Beispieldaten (Einnahmen & Ausgaben)
├── report.txt           # Wird beim Ausführen automatisch erstellt
└── README.md            # Diese Datei
```

## ⚙️ Voraussetzungen

- Python 3.8 oder neuer
- Keine externen Pakete nötig – nur Python-Standardbibliothek

Python-Version prüfen:
```bash
python --version
```

## 🚀 Programm starten

1. In den Projektordner wechseln:
```bash
cd smart_finance_analyzer
```

2. Programm ausführen:
```bash
python main.py
```

Das war's! Der Report wird im Terminal angezeigt und als `report.txt` gespeichert.

## 📊 CSV-Format

Die Datei `transactions.csv` muss diese vier Spalten haben:

| Spalte     | Beschreibung                    | Beispielwert |
|------------|---------------------------------|--------------|
| `month`    | Monatsname                      | `Januar`     |
| `type`     | `income` oder `expense`         | `expense`    |
| `amount`   | Betrag (Dezimalzahl)            | `850.00`     |
| `category` | Kategorie der Transaktion       | `Miete`      |

Beispielzeile:
```
Januar,expense,850,Miete
```

## 📈 Funktionen

| Funktion                    | Aufgabe                                           |
|-----------------------------|---------------------------------------------------|
| `load_transactions()`       | CSV-Datei einlesen & validieren                  |
| `calculate_summary()`       | Gesamteinnahmen, -ausgaben & Überschuss           |
| `calculate_categories()`    | Ausgaben nach Kategorien sortiert                |
| `calculate_monthly_balances()` | Bilanz pro Monat                             |
| `predict_next_month()`      | Prognose via Durchschnitt der Vergangenheit      |
| `create_report()`           | Formatierten Bericht-Text zusammenstellen        |
| `save_report()`             | Bericht als .txt-Datei speichern                 |

## 🛡️ Fehlerbehandlung

Das Programm behandelt folgende Fehlerfälle:
- CSV-Datei nicht gefunden
- Fehlende Pflicht-Spalten in der CSV
- Ungültige Beträge (kein Zahlenwert)
- Unbekannte Transaktionstypen
- Leere Datei / keine gültigen Daten
- Keine Schreibrechte beim Speichern

## 🔧 Eigene Daten verwenden

Einfach `transactions.csv` mit eigenen Daten befüllen oder ersetzen.
Das Format muss beibehalten werden (Kopfzeile + vier Spalten).

## 📝 Beispiel-Output

```
============================================================
       SMART FINANCE ANALYZER – FINANZBERICHT
============================================================
  Erstellt am: 15.06.2025 14:30 Uhr
============================================================

  GESAMTÜBERSICHT
  ----------------------------------------
  Gesamteinnahmen:        9950.00 €
  Gesamtausgaben:         5954.00 €
  ----------------------------------------
  Nettoüberschuss:        3996.00 €  [✓ Positiv]
  ...
```

## 🛠️ Technologien

- **Sprache:** Python 3.8+
- **Module:** `csv`, `os`, `collections`, `datetime` (alle eingebaut)
- **Paradigma:** Funktionale Programmierung mit klarer Schichttrennung
- **Architektur:** ETL-Pattern (Extract → Transform → Load/Output)

## 👤 Autor

Dein Name  
[deine@email.de](mailto:deine@email.de)  
[GitHub](https://github.com/dein-username)
