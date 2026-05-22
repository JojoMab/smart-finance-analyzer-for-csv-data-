import csv

import pandas as pd

from report_generator import create_monthly_report
from src.visualizer import (
    plot_budget_gauge,
    plot_expense_share_pie,
    plot_expenses_by_category,
    plot_monthly_balance,
)
from validator import validate_transaction


def load_transactions(path="data/transaction_data.csv"):
    with open(path, newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))
    invalid = [row for row in rows if not validate_transaction(row)]
    if invalid:
        raise ValueError("Ungültige Transaktionsdaten gefunden")
    return rows


def main():
    transactions = load_transactions()
    report_path = create_monthly_report(transactions)
    df = pd.DataFrame(transactions)
    df["amount"] = df["amount"].astype(float)
    if "type" not in df.columns:
        df["type"] = "EXPENSE"
    total_expenses = df[df["type"].astype(str).str.upper() == "EXPENSE"]["amount"].sum()
    budget = float(transactions[0]["budget"]) if transactions else 0.0
    charts_dir = "charts"

    plot_expenses_by_category(df, charts_dir)
    plot_monthly_balance(df, charts_dir)
    plot_budget_gauge(total_expenses, budget=budget, output_dir=charts_dir)
    plot_expense_share_pie(df, charts_dir)

    print("Smart Finance Analyzer abgeschlossen.")
    print(f"Report: {report_path}")
    print("Diagramme gespeichert in: charts/")


if __name__ == "__main__":
    main()
