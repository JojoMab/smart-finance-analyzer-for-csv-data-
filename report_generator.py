from pathlib import Path

from budget_analyzer import budget_status
from category_analyzer import sum_by_category


def create_monthly_report(transactions, output_path="reports/monthly_report.txt"):
    categories = sum_by_category(transactions)
    total_spent = sum(categories.values())
    budget = float(transactions[0]["budget"]) if transactions else 0
    lines = [
        "Smart Finance Analyzer Monatsreport",
        "===================================",
        "",
        f"Gesamtausgaben: {total_spent:.2f} EUR",
        f"Budgetampel: {budget_status(total_spent, budget)}",
        "",
        "Kategorien",
    ]
    for category, amount in sorted(categories.items()):
        lines.append(f"{category}: {amount:.2f} EUR")
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path
