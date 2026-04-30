# =============================================================================
# SMART FINANCE ANALYZER
# =============================================================================
# Dieses Programm liest Finanzdaten aus einer CSV-Datei ein,
# analysiert sie und erstellt einen übersichtlichen Bericht.
#
# Autor: Dein Name
# Version: 1.0
# Benötigt: Python 3.8 oder neuer (keine externen Pakete nötig!)
# =============================================================================


# --- Importe (eingebaute Python-Module, keine Installation nötig) ---

import csv          # Ermöglicht das Lesen von CSV-Dateien (Comma-Separated Values)
import os           # Ermöglicht den Zugriff auf das Dateisystem (z.B. Dateipfade)
from collections import defaultdict  # Ein spezielles Dictionary, das bei fehlenden
                                     # Schlüsseln automatisch einen Standardwert liefert
from datetime import datetime        # Ermöglicht Datum und Uhrzeit zu nutzen



# =============================================================================
# KONSTANTEN (Werte, die sich nie ändern – werden GROSS geschrieben)
# =============================================================================

SCRIPT_ORDNER = os.path.dirname(os.path.abspath(__file__))
CSV_DATEI = input("Name der CSV-Datei eingeben [transactions.csv]: ").strip() or "transactions.csv"
REPORT_DATEI = input("Name der Report-Datei eingeben [report.txt]: ").strip() or "report.txt"
CSV_DATEI = os.path.join(SCRIPT_ORDNER, CSV_DATEI)
REPORT_DATEI = os.path.join(SCRIPT_ORDNER, REPORT_DATEI)
TRENNLINIE = "=" * 60


# =============================================================================
# 1. FUNKTION: Transaktionen aus CSV laden
# =============================================================================

def load_transactions(dateipfad: str) -> list:
    """
    Liest alle Transaktionen aus der CSV-Datei und gibt sie als Liste zurück.

    Parameter:
        dateipfad (str): Der Pfad zur CSV-Datei, z.B. "transactions.csv"

    Rückgabe:
        list: Eine Liste von Dictionaries. Jedes Dictionary ist eine Transaktion.
              Beispiel: [{"month": "Januar", "type": "income", ...}, ...]
    """

    # Prüfen, ob die Datei überhaupt existiert – sonst Fehlermeldung ausgeben
    if not os.path.exists(dateipfad):
        # "raise" erzeugt einen Fehler und stoppt das Programm mit einer Nachricht
        raise FileNotFoundError(
            f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden.\n"
            f"Bitte stelle sicher, dass sie im selben Ordner wie main.py liegt."
        )

    # Leere Liste, in die wir alle Transaktionen speichern werden
    transaktionen = []

    # "with open(...)" öffnet die Datei und schließt sie automatisch danach
    # encoding="utf-8" sorgt dafür, dass Umlaute (ä, ö, ü) korrekt gelesen werden
    with open(dateipfad, newline="", encoding="utf-8") as csv_datei:

        # csv.DictReader liest jede Zeile als Dictionary (Schlüssel = Spaltenname)
        # Erste Zeile (Kopfzeile) wird automatisch als Schlüssel verwendet
        reader = csv.DictReader(csv_datei)

        # Prüfen, ob die erwarteten Spalten vorhanden sind
        erwartete_spalten = {"month", "type", "amount", "category"}
        if reader.fieldnames is None:
            raise ValueError("Fehler: Die CSV-Datei ist leer oder hat keine Kopfzeile.")

        # set() wandelt die Spaltenliste in eine Menge um – für einfachen Vergleich
        vorhandene_spalten = set(reader.fieldnames)
        fehlende_spalten = erwartete_spalten - vorhandene_spalten  # Mengendifferenz

        if fehlende_spalten:
            raise ValueError(
                f"Fehler: Folgende Spalten fehlen in der CSV-Datei: {fehlende_spalten}"
            )

        # Jede Zeile der CSV-Datei durchgehen
        for zeilen_nummer, zeile in enumerate(reader, start=2):  # start=2 weil Zeile 1 = Kopfzeile

            # Den Betrag (amount) von Text in eine Zahl umwandeln
            # "strip()" entfernt Leerzeichen vor und nach dem Wert
            betrag_text = zeile["amount"].strip()

            try:
                # float() wandelt Text wie "1200" oder "9.99" in eine Dezimalzahl um
                betrag = float(betrag_text)
            except ValueError:
                # Wenn die Umwandlung fehlschlägt, diese Zeile überspringen und warnen
                print(f"  Warnung: Zeile {zeilen_nummer} hat ungültigen Betrag '{betrag_text}' – wird übersprungen.")
                continue  # "continue" springt zur nächsten Schleifenrunde

            # Typ prüfen – erlaubt sind nur "income" und "expense"
            typ = zeile["type"].strip().lower()  # .lower() macht alles klein (z.B. "Income" → "income")
            if typ not in ("income", "expense"):
                print(f"  Warnung: Zeile {zeilen_nummer} hat unbekannten Typ '{typ}' – wird übersprungen.")
                continue

            # Gültige Transaktion als Dictionary zur Liste hinzufügen
            transaktionen.append({
                "month":    zeile["month"].strip(),     # Monatsname, z.B. "Januar"
                "type":     typ,                         # "income" oder "expense"
                "amount":   betrag,                      # Betrag als Zahl, z.B. 1200.0
                "category": zeile["category"].strip()   # Kategorie, z.B. "Gehalt"
            })

    # Prüfen, ob nach dem Laden überhaupt Daten vorhanden sind
    if not transaktionen:
        raise ValueError("Fehler: Die CSV-Datei enthält keine gültigen Transaktionen.")

    # Die fertige Liste zurückgeben
    return transaktionen


# =============================================================================
# 2. FUNKTION: Gesamtübersicht berechnen
# =============================================================================

def calculate_summary(transaktionen: list) -> dict:
    """
    Berechnet die Gesamteinnahmen, Gesamtausgaben und den Überschuss.

    Parameter:
        transaktionen (list): Die Liste aller Transaktionen (von load_transactions)

    Rückgabe:
        dict: Ein Dictionary mit den Schlüsseln 'einnahmen', 'ausgaben', 'ueberschuss'
    """

    # Startwerte auf 0 setzen – wir addieren gleich alles auf
    gesamt_einnahmen = 0.0   # Hier sammeln wir alle Einnahmen
    gesamt_ausgaben  = 0.0   # Hier sammeln wir alle Ausgaben

    # Jede Transaktion einzeln durchgehen
    for transaktion in transaktionen:

        if transaktion["type"] == "income":
            # Einnahme: zum Einnahmen-Zähler addieren
            gesamt_einnahmen += transaktion["amount"]

        elif transaktion["type"] == "expense":
            # Ausgabe: zum Ausgaben-Zähler addieren
            gesamt_ausgaben += transaktion["amount"]

    # Überschuss = Einnahmen minus Ausgaben
    # Positiv = mehr eingenommen als ausgegeben (gut!)
    # Negativ = mehr ausgegeben als eingenommen (Vorsicht!)
    ueberschuss = gesamt_einnahmen - gesamt_ausgaben

    # Ergebnis als Dictionary zurückgeben
    return {
        "einnahmen":   gesamt_einnahmen,
        "ausgaben":    gesamt_ausgaben,
        "ueberschuss": ueberschuss
    }


# =============================================================================
# 3. FUNKTION: Ausgaben nach Kategorien aufschlüsseln
# =============================================================================

def calculate_categories(transaktionen: list) -> dict:
    """
    Summiert alle Ausgaben pro Kategorie.

    Parameter:
        transaktionen (list): Die Liste aller Transaktionen

    Rückgabe:
        dict: Ein Dictionary wie {"Miete": 850.0, "Lebensmittel": 220.0, ...}
              Sortiert nach Betrag (höchste zuerst)
    """

    # defaultdict(float) ist wie ein normales Dictionary, aber:
    # Wenn ein Schlüssel noch nicht existiert, wird er automatisch mit 0.0 angelegt
    # Das erspart uns die Prüfung "if key in dict"
    kategorien = defaultdict(float)

    # Nur Ausgaben verarbeiten (Einnahmen interessieren uns hier nicht)
    for transaktion in transaktionen:
        if transaktion["type"] == "expense":
            kategorie = transaktion["category"]   # z.B. "Miete"
            betrag    = transaktion["amount"]      # z.B. 850.0

            # Betrag zur bisherigen Summe dieser Kategorie addieren
            kategorien[kategorie] += betrag

    # Dictionary nach Betrag sortieren (höchste Ausgabe zuerst)
    # "sorted()" gibt eine sortierte Liste zurück
    # "key=lambda x: x[1]" bedeutet: nach dem zweiten Element (dem Betrag) sortieren
    # "reverse=True" dreht die Reihenfolge um → höchste zuerst
    sortiert = dict(
        sorted(kategorien.items(), key=lambda x: x[1], reverse=True)
    )

    return sortiert


# =============================================================================
# 4. FUNKTION: Monatsüberschüsse berechnen
# =============================================================================

def calculate_monthly_balances(transaktionen: list) -> dict:
    """
    Berechnet für jeden Monat: Einnahmen, Ausgaben und Überschuss.

    Parameter:
        transaktionen (list): Die Liste aller Transaktionen

    Rückgabe:
        dict: Pro Monat ein Dictionary mit 'einnahmen', 'ausgaben', 'ueberschuss'
              Beispiel: {"Januar": {"einnahmen": 2800, "ausgaben": 1199, ...}, ...}
    """

    # Für jeden Monat ein eigenes Sub-Dictionary anlegen
    # Struktur: {"Januar": {"einnahmen": 0.0, "ausgaben": 0.0}, ...}
    monate = defaultdict(lambda: {"einnahmen": 0.0, "ausgaben": 0.0})

    for transaktion in transaktionen:
        monat  = transaktion["month"]    # z.B. "Januar"
        betrag = transaktion["amount"]   # z.B. 2500.0

        if transaktion["type"] == "income":
            monate[monat]["einnahmen"] += betrag   # Einnahme zum Monat addieren

        elif transaktion["type"] == "expense":
            monate[monat]["ausgaben"] += betrag    # Ausgabe zum Monat addieren

    # Jetzt den Überschuss für jeden Monat berechnen und eintragen
    ergebnis = {}
    for monat, werte in monate.items():
        ergebnis[monat] = {
            "einnahmen":   werte["einnahmen"],
            "ausgaben":    werte["ausgaben"],
            "ueberschuss": werte["einnahmen"] - werte["ausgaben"]  # Differenz berechnen
        }

    return ergebnis


# =============================================================================
# 5. FUNKTION: Prognose für nächsten Monat
# =============================================================================

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

    # Sicherheitsprüfung: Wenn keine Monatsdaten vorhanden, 0 zurückgeben
    if not monats_bilanzen:
        return 0.0

    # Alle monatlichen Überschüsse in einer Liste sammeln
    alle_ueberschuesse = []
    for monat, werte in monats_bilanzen.items():
        alle_ueberschuesse.append(werte["ueberschuss"])

    # Durchschnitt berechnen: Summe aller Werte geteilt durch Anzahl der Werte
    # sum() addiert alle Zahlen in der Liste
    # len() zählt die Anzahl der Elemente
    durchschnitt = sum(alle_ueberschuesse) / len(alle_ueberschuesse)

    # round() rundet auf 2 Nachkommastellen (Cent-Genauigkeit)
    return round(durchschnitt, 2)


# =============================================================================
# 6. FUNKTION: Report als Text erstellen
# =============================================================================

def create_report(zusammenfassung: dict, kategorien: dict,
                  monats_bilanzen: dict, prognose: float) -> str:
    """
    Erstellt den vollständigen Report als formatierten Text-String.

    Parameter:
        zusammenfassung  (dict): Ergebnis von calculate_summary()
        kategorien       (dict): Ergebnis von calculate_categories()
        monats_bilanzen  (dict): Ergebnis von calculate_monthly_balances()
        prognose        (float): Ergebnis von predict_next_month()

    Rückgabe:
        str: Der vollständige Report als ein langer Text-String
    """

    # Liste von Zeilen – am Ende mit "\n".join() zu einem Text zusammenbauen
    # Das ist effizienter als viele Strings mit "+" zu verketten
    zeilen = []

    # Aktuelles Datum und Uhrzeit für den Report-Header
    jetzt = datetime.now().strftime("%d.%m.%Y %H:%M Uhr")  # Format: "15.06.2025 14:30 Uhr"

    # --- HEADER ---
    zeilen.append(TRENNLINIE)
    zeilen.append("       SMART FINANCE ANALYZER – FINANZBERICHT")
    zeilen.append(TRENNLINIE)
    zeilen.append(f"  Erstellt am: {jetzt}")
    zeilen.append(TRENNLINIE)

    # --- ABSCHNITT 1: Gesamtübersicht ---
    zeilen.append("")
    zeilen.append("  GESAMTÜBERSICHT")
    zeilen.append("  " + "-" * 40)

    # f-Strings: Mit f"..." kann man Variablen direkt in Text einbauen
    # :>10.2f = rechtsbündig, 10 Zeichen breit, 2 Nachkommastellen, float
    zeilen.append(f"  {'Gesamteinnahmen:':<22} {zusammenfassung['einnahmen']:>10.2f} €")
    zeilen.append(f"  {'Gesamtausgaben:':<22} {zusammenfassung['ausgaben']:>10.2f} €")
    zeilen.append("  " + "-" * 40)

    ueberschuss = zusammenfassung["ueberschuss"]

    # Visuelles Feedback: "+" für positiv, Warnung für negativ
    if ueberschuss >= 0:
        status = "✓ Positiv"
    else:
        status = "⚠ Negativ – Achtung!"

    zeilen.append(f"  {'Nettoüberschuss:':<22} {ueberschuss:>10.2f} €  [{status}]")

    # --- ABSCHNITT 2: Ausgaben nach Kategorien ---
    zeilen.append("")
    zeilen.append("")
    zeilen.append("  AUSGABEN NACH KATEGORIEN")
    zeilen.append("  " + "-" * 40)

    if not kategorien:
        zeilen.append("  Keine Ausgaben gefunden.")
    else:
        # Gesamtausgaben berechnen für Prozentangaben
        gesamt_ausgaben = zusammenfassung["ausgaben"]

        for kategorie, betrag in kategorien.items():
            # Prozentualen Anteil berechnen
            if gesamt_ausgaben > 0:
                prozent = (betrag / gesamt_ausgaben) * 100  # Dreisatz
            else:
                prozent = 0.0

            # Kleine Balkengrafik im Terminal: ein "█" pro 5%
            balken_laenge = int(prozent / 5)           # Ganzzahl-Division
            balken        = "█" * balken_laenge         # String-Wiederholung

            zeilen.append(
                f"  {kategorie:<20} {betrag:>8.2f} €  ({prozent:>5.1f}%)  {balken}"
            )

    # --- ABSCHNITT 3: Monatliche Bilanzen ---
    zeilen.append("")
    zeilen.append("")
    zeilen.append("  MONATLICHE BILANZEN")
    zeilen.append("  " + "-" * 55)
    zeilen.append(f"  {'Monat':<12} {'Einnahmen':>12} {'Ausgaben':>12} {'Überschuss':>12}")
    zeilen.append("  " + "-" * 55)

    for monat, werte in monats_bilanzen.items():
        # Negativen Überschuss mit "–" kennzeichnen, positiven mit "+"
        ue    = werte["ueberschuss"]
        zeichen = "+" if ue >= 0 else ""  # Vorzeichen: leer wenn negativ (Minus kommt automatisch)

        zeilen.append(
            f"  {monat:<12} {werte['einnahmen']:>10.2f} €"
            f"  {werte['ausgaben']:>10.2f} €"
            f"  {zeichen}{ue:>9.2f} €"
        )

    # --- ABSCHNITT 4: Prognose ---
    zeilen.append("")
    zeilen.append("")
    zeilen.append("  PROGNOSE NÄCHSTER MONAT")
    zeilen.append("  " + "-" * 40)

    # Anzahl der Monate als Basis für die Prognose anzeigen
    anzahl_monate = len(monats_bilanzen)
    zeilen.append(f"  Berechnung basiert auf {anzahl_monate} Monat(en)")
    zeilen.append(f"  Methode: Durchschnitt der Monatsüberschüsse")
    zeilen.append("")

    vorzeichen = "+" if prognose >= 0 else ""
    zeilen.append(f"  Voraussichtlicher Überschuss: {vorzeichen}{prognose:.2f} €")

    if prognose < 0:
        zeilen.append("  ⚠ Warnung: Auf Basis der bisherigen Daten droht ein Defizit!")
    elif prognose < 200:
        zeilen.append("  ℹ Hinweis: Der Puffer ist gering. Ausgaben prüfen.")
    else:
        zeilen.append("  ✓ Gut! Solider finanzieller Puffer erwartet.")

    # --- FOOTER ---
    zeilen.append("")
    zeilen.append(TRENNLINIE)
    zeilen.append("  Smart Finance Analyzer – Ende des Berichts")
    zeilen.append(TRENNLINIE)

    # Alle Zeilen mit Zeilenumbruch "\n" verbinden → ein einziger Text-String
    return "\n".join(zeilen)


# =============================================================================
# 7. FUNKTION: Report in Datei speichern
# =============================================================================

def save_report(report_text: str, dateipfad: str) -> None:
    """
    Speichert den fertigen Report als .txt-Datei auf der Festplatte.

    Parameter:
        report_text (str): Der vollständige Report-Text
        dateipfad   (str): Wo die Datei gespeichert werden soll, z.B. "report.txt"

    Rückgabe:
        None (die Funktion gibt nichts zurück, sie hat einen Nebeneffekt: Datei schreiben)
    """

    # "with open(..., 'w')" öffnet die Datei zum Schreiben ("w" = write)
    # Wenn die Datei schon existiert, wird sie überschrieben
    # encoding="utf-8" sorgt für korrekte Darstellung von Umlauten
    with open(dateipfad, "w", encoding="utf-8") as datei:
        datei.write(report_text)   # Den gesamten Text in die Datei schreiben



# =============================================================================
# HAUPTPROGRAMM – wird nur ausgeführt wenn main.py direkt gestartet wird
# =============================================================================

def main():
    """
    Hauptfunktion: Koordiniert den gesamten Ablauf des Programms.
    Ruft alle anderen Funktionen in der richtigen Reihenfolge auf.
    """

    print(TRENNLINIE)
    print("  Smart Finance Analyzer wird gestartet...")
    print(TRENNLINIE)
    print()

    # --- SCHRITT 1: Daten laden ---
    print("  [1/5] Lade Transaktionen aus CSV...")

    # "try/except" fängt Fehler ab, ohne dass das Programm abstürzt
    try:
        transaktionen = load_transactions(CSV_DATEI)
        print(f"  ✓ {len(transaktionen)} Transaktionen erfolgreich geladen.")
    except (FileNotFoundError, ValueError) as fehler:
        # "fehler" enthält die Fehlermeldung, die wir in der Funktion definiert haben
        print(f"\n  FEHLER: {fehler}")
        print("  Das Programm wird beendet.")
        return   # Funktion beenden – ohne "return" würde Python weiter unten abstürzen

    print()

    # --- SCHRITT 2: Gesamtübersicht berechnen ---
    print("  [2/5] Berechne Gesamtübersicht...")
    zusammenfassung = calculate_summary(transaktionen)
    print(f"  ✓ Einnahmen: {zusammenfassung['einnahmen']:.2f} € | "
          f"Ausgaben: {zusammenfassung['ausgaben']:.2f} € | "
          f"Überschuss: {zusammenfassung['ueberschuss']:.2f} €")
    print()

    # --- SCHRITT 3: Kategorien analysieren ---
    print("  [3/5] Analysiere Ausgaben nach Kategorien...")
    kategorien = calculate_categories(transaktionen)
    print(f"  ✓ {len(kategorien)} Kategorien gefunden: {', '.join(kategorien.keys())}")
    print()

    # --- SCHRITT 4: Monatsbilanzen und Prognose ---
    print("  [4/5] Berechne Monatsbilanzen und Prognose...")
    monats_bilanzen = calculate_monthly_balances(transaktionen)
    prognose        = predict_next_month(monats_bilanzen)
    print(f"  ✓ {len(monats_bilanzen)} Monate analysiert. Prognose: {prognose:.2f} €")
    print()

    # --- SCHRITT 5: Report erstellen und anzeigen ---
    print("  [5/5] Erstelle und speichere Report...")
    report = create_report(zusammenfassung, kategorien, monats_bilanzen, prognose)

    # Report im Terminal ausgeben
    print()
    print(report)

    # Report als Datei speichern
    try:
        save_report(report, REPORT_DATEI)
        print()
        print(f"  ✓ Report wurde gespeichert: '{REPORT_DATEI}'")
    except OSError as fehler:
        # OSError tritt auf, wenn z.B. keine Schreibrechte vorhanden sind
        print(f"  ⚠ Warnung: Report konnte nicht gespeichert werden: {fehler}")

    print()
    print(TRENNLINIE)
    print("  Analyse abgeschlossen!")
    print(TRENNLINIE)


# =============================================================================
# EINSTIEGSPUNKT DES PROGRAMMS
# =============================================================================
# Diese Zeile sorgt dafür, dass main() nur ausgeführt wird,
# wenn die Datei direkt gestartet wird (z.B. "python main.py")
# und NICHT wenn sie von einer anderen Datei importiert wird.
#
# __name__ ist eine spezielle Variable in Python:
# - Beim direkten Ausführen: __name__ == "__main__"
# - Beim Importieren:       __name__ == "main" (der Dateiname)
# =============================================================================

if __name__ == "__main__":
    main()   # Hauptfunktion aufrufen → Programm startet
