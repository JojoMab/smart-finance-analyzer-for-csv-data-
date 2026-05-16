import csv
from dataclasses import dataclass

import pandas as pd

from budget_analyzer import budget_status as calculate_budget_status
from report_generator import create_monthly_report
from src.visualizer import (
    plot_budget_gauge,
    plot_expense_share_pie,
    plot_expenses_by_category,
    plot_monthly_balance,
)
from validator import validate_transaction


@dataclass
class Transaction:
    category: str
    amount: float
    budget: float


def budget_status(transaction):
    status = calculate_budget_status(float(transaction.amount), float(transaction.budget))
    return {"ROT": "red", "GELB": "yellow", "GRÜN": "green"}[status]


def risk_score(transaction):
    remaining_ratio = (float(transaction.budget) - float(transaction.amount)) / float(transaction.budget)
    return max(0, round((1 - remaining_ratio) * 10, 2))


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
    charts_dir = "charts"

    plot_expenses_by_category(df, charts_dir)
    plot_monthly_balance(df, charts_dir)
    plot_budget_gauge(total_expenses, budget=1500.0, output_dir=charts_dir)
    plot_expense_share_pie(df, charts_dir)

    print("Smart Finance Analyzer abgeschlossen.")
    print(f"Report: {report_path}")
    print("Diagramme gespeichert in: charts/")


if __name__ == "__main__":
    main()
