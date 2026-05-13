import csv
import os
from collections import defaultdict
from datetime import datetime


SCRIPT_ORDNER = os.path.dirname(os.path.abspath(__file__))
CSV_DATEI = input("Name der CSV-Datei eingeben [transactions.csv]: ").strip() or "transactions.csv"
REPORT_DATEI = input("Name der Report-Datei eingeben [report.txt]: ").strip() or "report.txt"
CSV_DATEI = os.path.join(SCRIPT_ORDNER, CSV_DATEI)
REPORT_DATEI = os.path.join(SCRIPT_ORDNER, REPORT_DATEI)
TRENNLINIE = "=" * 60


def load_transactions(dateipfad: str) -> list:
    """
    Liest alle Transaktionen aus der CSV-Datei und gibt sie als Liste zurück.

    Parameter:
        dateipfad (str): Der Pfad zur CSV-Datei, z.B. "transactions.csv"

    Rückgabe:
        list: Eine Liste von Dictionaries. Jedes Dictionary ist eine Transaktion.
              Beispiel: [{"month": "Januar", "type": "income", ...}, ...]
    """

    if not os.path.exists(dateipfad):
        raise FileNotFoundError(
            f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden.\n"
            f"Bitte stelle sicher, dass sie im selben Ordner wie main.py liegt."
        )

    transaktionen = []

    with open(dateipfad, newline="", encoding="utf-8") as csv_datei:
        reader = csv.DictReader(csv_datei)

        erwartete_spalten = {"month", "type", "amount", "category"}
        if reader.fieldnames is None:
            raise ValueError("Fehler: Die CSV-Datei ist leer oder hat keine Kopfzeile.")

        vorhandene_spalten = set(reader.fieldnames)
        fehlende_spalten = erwartete_spalten - vorhandene_spalten

        if fehlende_spalten:
            raise ValueError(
                f"Fehler: Folgende Spalten fehlen in der CSV-Datei: {fehlende_spalten}"
            )

        for zeilen_nummer, zeile in enumerate(reader, start=2):
            betrag_text = zeile["amount"].strip()

            try:
                betrag = float(betrag_text)
            except ValueError:
                print(f"  Warnung: Zeile {zeilen_nummer} hat ungültigen Betrag '{betrag_text}' – wird übersprungen.")
                continue

            typ = zeile["type"].strip().lower()
            if typ not in ("income", "expense"):
                print(f"  Warnung: Zeile {zeilen_nummer} hat unbekannten Typ '{typ}' – wird übersprungen.")
                continue

            transaktionen.append({
                "month": zeile["month"].strip(),
                "type": typ,
                "amount": betrag,
                "category": zeile["category"].strip()
            })

    if not transaktionen:
        raise ValueError("Fehler: Die CSV-Datei enthält keine gültigen Transaktionen.")

    return transaktionen


def calculate_summary(transaktionen: list) -> dict:
    """
    Berechnet die Gesamteinnahmen, Gesamtausgaben und den Überschuss.

    Parameter:
        transaktionen (list): Die Liste aller Transaktionen (von load_transactions)

    Rückgabe:
        dict: Ein Dictionary mit den Schlüsseln 'einnahmen', 'ausgaben', 'ueberschuss'
    """

    gesamt_einnahmen = 0.0
    gesamt_ausgaben = 0.0

    for transaktion in transaktionen:
        if transaktion["type"] == "income":
            gesamt_einnahmen += transaktion["amount"]
        elif transaktion["type"] == "expense":
            gesamt_ausgaben += transaktion["amount"]

    ueberschuss = gesamt_einnahmen - gesamt_ausgaben

    return {
        "einnahmen": gesamt_einnahmen,
        "ausgaben": gesamt_ausgaben,
        "ueberschuss": ueberschuss
    }


def calculate_categories(transaktionen: list) -> dict:
    """
    Summiert alle Ausgaben pro Kategorie.

    Parameter:
        transaktionen (list): Die Liste aller Transaktionen

    Rückgabe:
        dict: Ein Dictionary wie {"Miete": 850.0, "Lebensmittel": 220.0, ...}
              Sortiert nach Betrag (höchste zuerst)
    """

    kategorien = defaultdict(float)

    for transaktion in transaktionen:
        if transaktion["type"] == "expense":
            kategorie = transaktion["category"]
            betrag = transaktion["amount"]
            kategorien[kategorie] += betrag

    sortiert = dict(
        sorted(kategorien.items(), key=lambda x: x[1], reverse=True)
    )

    return sortiert


def calculate_monthly_balances(transaktionen: list) -> dict:
    """
    Berechnet für jeden Monat: Einnahmen, Ausgaben und Überschuss.

    Parameter:
        transaktionen (list): Die Liste aller Transaktionen

    Rückgabe:
        dict: Pro Monat ein Dictionary mit 'einnahmen', 'ausgaben', 'ueberschuss'
              Beispiel: {"Januar": {"einnahmen": 2800, "ausgaben": 1199, ...}, ...}
    """

    monate = defaultdict(lambda: {"einnahmen": 0.0, "ausgaben": 0.0})

    for transaktion in transaktionen:
        monat = transaktion["month"]
        betrag = transaktion["amount"]

        if transaktion["type"] == "income":
            monate[monat]["einnahmen"] += betrag
        elif transaktion["type"] == "expense":
            monate[monat]["ausgaben"] += betrag

    ergebnis = {}
    for monat, werte in monate.items():
        ergebnis[monat] = {
            "einnahmen": werte["einnahmen"],
            "ausgaben": werte["ausgaben"],
            "ueberschuss": werte["einnahmen"] - werte["ausgaben"]
        }

    return ergebnis


def predict_next_month(monats_bilanzen: dict) -> float:
    """
    Berechnet den voraussichtlichen Überschuss des nächsten Monats.
    Methode: Einfacher Durchschnitt aller bisherigen Monatsüberschüsse.

    Parameter:
        monats_bilanzen (dict): Das Ergebnis von calculate_monthly_balances()

    Rückgabe:
        float: Der prognostizierte Überschuss, z.B. 820.50
               Gibt 0.0 zurück wenn keine Daten vorhanden sind.
    """

    if not monats_bilanzen:
        return 0.0

    alle_ueberschuesse = []
    for monat, werte in monats_bilanzen.items():
        alle_ueberschuesse.append(werte["ueberschuss"])

    durchschnitt = sum(alle_ueberschuesse) / len(alle_ueberschuesse)

    return round(durchschnitt, 2)


def create_report(zusammenfassung: dict, kategorien: dict,
                  monats_bilanzen: dict, prognose: float) -> str:
    """
    Erstellt den vollständigen Report als formatierten Text-String.

    Parameter:
        zusammenfassung  (dict): Ergebnis von calculate_summary()
        kategorien       (dict): Ergebnis von calculate_categories()
        monats_bilanzen  (dict): Ergebnis von calculate_monthly_balances()
        prognose         (float): Ergebnis von predict_next_month()

    Rückgabe:
        str: Der vollständige Report als ein langer Text-String
    """

    zeilen = []
    jetzt = datetime.now().strftime("%d.%m.%Y %H:%M Uhr")

    zeilen.append(TRENNLINIE)
    zeilen.append("       SMART FINANCE ANALYZER – FINANZBERICHT")
    zeilen.append(TRENNLINIE)
    zeilen.append(f"  Erstellt am: {jetzt}")
    zeilen.append(TRENNLINIE)

    zeilen.append("")
    zeilen.append("  GESAMTÜBERSICHT")
    zeilen.append("  " + "-" * 40)
    zeilen.append(f"  {'Gesamteinnahmen:':<22} {zusammenfassung['einnahmen']:>10.2f} €")
    zeilen.append(f"  {'Gesamtausgaben:':<22} {zusammenfassung['ausgaben']:>10.2f} €")
    zeilen.append("  " + "-" * 40)

    ueberschuss = zusammenfassung["ueberschuss"]
    status = "✓ Positiv" if ueberschuss >= 0 else "⚠ Negativ – Achtung!"
    zeilen.append(f"  {'Nettoüberschuss:':<22} {ueberschuss:>10.2f} €  [{status}]")

    zeilen.append("")
    zeilen.append("")
    zeilen.append("  AUSGABEN NACH KATEGORIEN")
    zeilen.append("  " + "-" * 40)

    if not kategorien:
        zeilen.append("  Keine Ausgaben gefunden.")
    else:
        gesamt_ausgaben = zusammenfassung["ausgaben"]

        for kategorie, betrag in kategorien.items():
            if gesamt_ausgaben > 0:
                prozent = (betrag / gesamt_ausgaben) * 100
            else:
                prozent = 0.0

            zeilen.append(
                f"  {kategorie:<20} {betrag:>8.2f} €  ({prozent:>5.1f}%)"
            )

    zeilen.append("")
    zeilen.append("")
    zeilen.append("  MONATLICHE BILANZEN")
    zeilen.append("  " + "-" * 55)
    zeilen.append(f"  {'Monat':<12} {'Einnahmen':>12} {'Ausgaben':>12} {'Überschuss':>12}")
    zeilen.append("  " + "-" * 55)

    for monat, werte in monats_bilanzen.items():
        ue = werte["ueberschuss"]
        zeichen = "+" if ue >= 0 else ""

        zeilen.append(
            f"  {monat:<12} {werte['einnahmen']:>10.2f} €"
            f"  {werte['ausgaben']:>10.2f} €"
            f"  {zeichen}{ue:>9.2f} €"
        )

    zeilen.append("")
    zeilen.append("")
    zeilen.append("  PROGNOSE NÄCHSTER MONAT")
    zeilen.append("  " + "-" * 40)
    zeilen.append(f"  Berechnung basiert auf {len(monats_bilanzen)} Monat(en)")
    zeilen.append("  Methode: Durchschnitt der Monatsüberschüsse")
    zeilen.append("")

    vorzeichen = "+" if prognose >= 0 else ""
    zeilen.append(f"  Voraussichtlicher Überschuss: {vorzeichen}{prognose:.2f} €")

    if prognose < 0:
        zeilen.append("  ⚠ Warnung: Auf Basis der bisherigen Daten droht ein Defizit!")
    elif prognose < 200:
        zeilen.append("  ℹ Hinweis: Der Puffer ist gering. Ausgaben prüfen.")
    else:
        zeilen.append("  ✓ Gut! Solider finanzieller Puffer erwartet.")

    zeilen.append("")
    zeilen.append(TRENNLINIE)
    zeilen.append("  Smart Finance Analyzer – Ende des Berichts")
    zeilen.append(TRENNLINIE)

    return "\n".join(zeilen)


def save_report(report_text: str, dateipfad: str) -> None:
    """
    Speichert den fertigen Report als .txt-Datei auf der Festplatte.

    Parameter:
        report_text (str): Der vollständige Report-Text
        dateipfad   (str): Wo die Datei gespeichert werden soll, z.B. "report.txt"

    Rückgabe:
        None
    """

    with open(dateipfad, "w", encoding="utf-8") as datei:
        datei.write(report_text)


def main():
    """
    Hauptfunktion: Koordiniert den gesamten Ablauf des Programms.
    """

    print(TRENNLINIE)
    print("  Smart Finance Analyzer wird gestartet...")
    print(TRENNLINIE)
    print()

    # Daten laden und validieren
    print("  [1/5] Lade Transaktionen aus CSV...")
    try:
        transaktionen = load_transactions(CSV_DATEI)
        print(f"  ✓ {len(transaktionen)} Transaktionen erfolgreich geladen.")
    except (FileNotFoundError, ValueError) as fehler:
        print(f"\n  FEHLER: {fehler}")
        print("  Das Programm wird beendet.")
        return

    print()

    # Kennzahlen berechnen
    print("  [2/5] Berechne Gesamtübersicht...")
    zusammenfassung = calculate_summary(transaktionen)
    print(f"  ✓ Einnahmen: {zusammenfassung['einnahmen']:.2f} € | "
          f"Ausgaben: {zusammenfassung['ausgaben']:.2f} € | "
          f"Überschuss: {zusammenfassung['ueberschuss']:.2f} €")
    print()

    print("  [3/5] Analysiere Ausgaben nach Kategorien...")
    kategorien = calculate_categories(transaktionen)
    print(f"  ✓ {len(kategorien)} Kategorien gefunden: {', '.join(kategorien.keys())}")
    print()

    print("  [4/5] Berechne Monatsbilanzen und Prognose...")
    monats_bilanzen = calculate_monthly_balances(transaktionen)
    prognose = predict_next_month(monats_bilanzen)
    print(f"  ✓ {len(monats_bilanzen)} Monate analysiert. Prognose: {prognose:.2f} €")
    print()

    # Report erstellen und speichern
    print("  [5/5] Erstelle und speichere Report...")
    report = create_report(zusammenfassung, kategorien, monats_bilanzen, prognose)

    print()
    print(report)

    try:
        save_report(report, REPORT_DATEI)
        print()
        print(f"  ✓ Report wurde gespeichert: '{REPORT_DATEI}'")
    except OSError as fehler:
        print(f"  ⚠ Warnung: Report konnte nicht gespeichert werden: {fehler}")

    print()
    print(TRENNLINIE)
    print("  Analyse abgeschlossen!")
    print(TRENNLINIE)


if __name__ == "__main__":
    main()
