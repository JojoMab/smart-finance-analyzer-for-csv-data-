# Smart Finance Analyzer

Ein CLI-basiertes Python-Tool zur Analyse persönlicher Finanzdaten aus
CSV-Dateien.\
Das Programm erstellt automatisch einen strukturierten Finanzbericht
inklusive Auswertung und einfacher Prognose.

------------------------------------------------------------------------

## Overview

Der Smart Finance Analyzer verarbeitet Transaktionen aus einer CSV-Datei
und generiert daraus einen übersichtlichen Bericht.

Dabei werden: - Einnahmen und Ausgaben berechnet - Ausgaben nach
Kategorien analysiert - Monatsbilanzen erstellt - eine Prognose für den
nächsten Monat berechnet

Das Tool ist bewusst einfach gehalten und kommt ohne externe
Bibliotheken aus.

------------------------------------------------------------------------

## Features

-   Gesamtübersicht (Einnahmen, Ausgaben, Überschuss)
-   Analyse der Ausgaben nach Kategorien
-   Monatliche Finanzübersicht
-   Prognose basierend auf Durchschnittswerten
-   Robustes Fehlerhandling
-   Automatische Erstellung eines Text-Reports

------------------------------------------------------------------------

## Project Structure

    .
    ├── main.py
    ├── transactions.csv
    └── report.txt

------------------------------------------------------------------------

## Input Format

Die CSV-Datei muss folgende Spalten enthalten:

    month,type,amount,category

### Beispiel

    Januar,income,2500,Gehalt
    Januar,expense,800,Miete
    Februar,expense,200,Lebensmittel

------------------------------------------------------------------------

## Usage

Programm starten:

``` bash
python main.py
```

Anschließend: - CSV-Datei auswählen (Default: transactions.csv) - Namen
für den Report festlegen (Default: report.txt)

------------------------------------------------------------------------

## Output

Der generierte Report enthält: - Gesamtübersicht - Kategorienanalyse mit
Prozentwerten - Monatsbilanzen - Prognose für den nächsten Monat

------------------------------------------------------------------------

## Tech Stack

-   Python 3
-   Standardbibliotheken (`csv`, `os`, `collections`, `datetime`)

------------------------------------------------------------------------

## Design Goals

-   Klare und verständliche Struktur
-   Keine externen Abhängigkeiten
-   Fokus auf Datenverarbeitung
-   Gute Erweiterbarkeit

------------------------------------------------------------------------

## License

Frei nutzbar für Lern- und private Zwecke.
