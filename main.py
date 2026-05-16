import csv
from dataclasses import dataclass

from budget_analyzer import budget_status as calculate_budget_status
from report_generator import create_monthly_report
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
    print("Smart Finance Analyzer abgeschlossen.")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
