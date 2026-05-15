import csv
import os
from collections import defaultdict
from datetime import datetime


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_INPUT = input("Enter CSV file name [transactions.csv]: ").strip() or "transactions.csv"
REPORT_INPUT = input("Enter report file name [report.txt]: ").strip() or "report.txt"
CSV_FILE = os.path.join(SCRIPT_DIR, CSV_INPUT)
REPORT_FILE = os.path.join(SCRIPT_DIR, REPORT_INPUT)
SEPARATOR = "=" * 60


def load_transactions(file_path: str) -> list:
    """
    Read all transactions from a CSV file and return them as dictionaries.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Error: The file '{file_path}' was not found.\n"
            "Please make sure it is located in the same folder as main.py."
        )

    transactions = []

    with open(file_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        expected_columns = {"month", "type", "amount", "category"}
        if reader.fieldnames is None:
            raise ValueError("Error: The CSV file is empty or has no header row.")

        existing_columns = set(reader.fieldnames)
        missing_columns = expected_columns - existing_columns

        if missing_columns:
            raise ValueError(
                f"Error: Missing columns in the CSV file: {missing_columns}"
            )

        for line_number, row in enumerate(reader, start=2):
            amount_text = row["amount"].strip()

            try:
                amount = float(amount_text)
            except ValueError:
                print(f"  Warning: line {line_number} has invalid amount '{amount_text}' and was skipped.")
                continue

            transaction_type = row["type"].strip().lower()
            if transaction_type not in ("income", "expense"):
                print(f"  Warning: line {line_number} has unknown type '{transaction_type}' and was skipped.")
                continue

            transactions.append({
                "month": row["month"].strip(),
                "type": transaction_type,
                "amount": amount,
                "category": row["category"].strip()
            })

    if not transactions:
        raise ValueError("Error: The CSV file does not contain valid transactions.")

    return transactions


def calculate_summary(transactions: list) -> dict:
    """
    Calculate total income, total expenses and net surplus.
    """

    total_income = 0.0
    total_expenses = 0.0

    for transaction in transactions:
        if transaction["type"] == "income":
            total_income += transaction["amount"]
        elif transaction["type"] == "expense":
            total_expenses += transaction["amount"]

    surplus = total_income - total_expenses

    return {
        "income": total_income,
        "expenses": total_expenses,
        "surplus": surplus
    }


def calculate_categories(transactions: list) -> dict:
    """
    Sum expenses by category and sort by amount.
    """

    categories = defaultdict(float)

    for transaction in transactions:
        if transaction["type"] == "expense":
            categories[transaction["category"]] += transaction["amount"]

    return dict(
        sorted(categories.items(), key=lambda item: item[1], reverse=True)
    )


def calculate_monthly_balances(transactions: list) -> dict:
    """
    Calculate income, expenses and surplus for each month.
    """

    months = defaultdict(lambda: {"income": 0.0, "expenses": 0.0})

    for transaction in transactions:
        month = transaction["month"]
        amount = transaction["amount"]

        if transaction["type"] == "income":
            months[month]["income"] += amount
        elif transaction["type"] == "expense":
            months[month]["expenses"] += amount

    result = {}
    for month, values in months.items():
        result[month] = {
            "income": values["income"],
            "expenses": values["expenses"],
            "surplus": values["income"] - values["expenses"]
        }

    return result


def predict_next_month(monthly_balances: dict) -> float:
    """
    Forecast the next month's surplus using the average monthly surplus.
    """

    if not monthly_balances:
        return 0.0

    surpluses = []
    for values in monthly_balances.values():
        surpluses.append(values["surplus"])

    average = sum(surpluses) / len(surpluses)

    return round(average, 2)


def create_report(summary: dict, categories: dict,
                  monthly_balances: dict, forecast: float) -> str:
    """
    Create the full finance report as formatted text.
    """

    lines = []
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines.append(SEPARATOR)
    lines.append("       SMART FINANCE ANALYZER - FINANCIAL REPORT")
    lines.append(SEPARATOR)
    lines.append(f"  Created at: {created_at}")
    lines.append(SEPARATOR)

    lines.append("")
    lines.append("  FINANCIAL SUMMARY")
    lines.append("  " + "-" * 40)
    lines.append(f"  {'Total income:':<22} {summary['income']:>10.2f} EUR")
    lines.append(f"  {'Total expenses:':<22} {summary['expenses']:>10.2f} EUR")
    lines.append("  " + "-" * 40)

    surplus = summary["surplus"]
    status = "positive" if surplus >= 0 else "negative"
    lines.append(f"  {'Net surplus:':<22} {surplus:>10.2f} EUR  [{status}]")

    lines.append("")
    lines.append("")
    lines.append("  EXPENSES BY CATEGORY")
    lines.append("  " + "-" * 40)

    if not categories:
        lines.append("  No expenses found.")
    else:
        total_expenses = summary["expenses"]

        for category, amount in categories.items():
            percentage = (amount / total_expenses) * 100 if total_expenses > 0 else 0.0
            lines.append(
                f"  {category:<20} {amount:>8.2f} EUR  ({percentage:>5.1f}%)"
            )

    lines.append("")
    lines.append("")
    lines.append("  MONTHLY BALANCES")
    lines.append("  " + "-" * 58)
    lines.append(f"  {'Month':<12} {'Income':>12} {'Expenses':>12} {'Surplus':>14}")
    lines.append("  " + "-" * 58)

    for month, values in monthly_balances.items():
        surplus_value = values["surplus"]
        sign = "+" if surplus_value >= 0 else ""

        lines.append(
            f"  {month:<12} {values['income']:>10.2f} EUR"
            f"  {values['expenses']:>10.2f} EUR"
            f"  {sign}{surplus_value:>9.2f} EUR"
        )

    lines.append("")
    lines.append("")
    lines.append("  NEXT-MONTH FORECAST")
    lines.append("  " + "-" * 40)
    lines.append(f"  Based on {len(monthly_balances)} month(s)")
    lines.append("  Method: average monthly surplus")
    lines.append("")

    forecast_sign = "+" if forecast >= 0 else ""
    lines.append(f"  Expected surplus: {forecast_sign}{forecast:.2f} EUR")

    if forecast < 0:
        lines.append("  Warning: the current data indicates a possible deficit.")
    elif forecast < 200:
        lines.append("  Note: the buffer is low. Review expenses.")
    else:
        lines.append("  Solid financial buffer expected.")

    lines.append("")
    lines.append(SEPARATOR)
    lines.append("  Smart Finance Analyzer - end of report")
    lines.append(SEPARATOR)

    return "\n".join(lines)


def save_report(report_text: str, file_path: str) -> None:
    """
    Save the finished report as a text file.
    """

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(report_text)


def main():
    """
    Coordinate the full analysis workflow.
    """

    print(SEPARATOR)
    print("  Smart Finance Analyzer starting...")
    print(SEPARATOR)
    print()

    print("  [1/5] Loading transactions from CSV...")
    try:
        transactions = load_transactions(CSV_FILE)
        print(f"  ✓ {len(transactions)} transactions loaded.")
    except (FileNotFoundError, ValueError) as error:
        print(f"\n  ERROR: {error}")
        print("  The program will exit.")
        return

    print()

    print("  [2/5] Calculating financial summary...")
    summary = calculate_summary(transactions)
    print(f"  ✓ Income: {summary['income']:.2f} EUR | "
          f"Expenses: {summary['expenses']:.2f} EUR | "
          f"Surplus: {summary['surplus']:.2f} EUR")
    print()

    print("  [3/5] Analyzing expense categories...")
    categories = calculate_categories(transactions)
    print(f"  ✓ {len(categories)} categories found: {', '.join(categories.keys())}")
    print()

    print("  [4/5] Calculating monthly balances and forecast...")
    monthly_balances = calculate_monthly_balances(transactions)
    forecast = predict_next_month(monthly_balances)
    print(f"  ✓ {len(monthly_balances)} months analyzed. Forecast: {forecast:.2f} EUR")
    print()

    print("  [5/5] Creating and saving report...")
    report = create_report(summary, categories, monthly_balances, forecast)

    print()
    print(report)

    try:
        save_report(report, REPORT_FILE)
        print()
        print(f"  ✓ Report saved: '{REPORT_INPUT}'")
    except OSError as error:
        print(f"  Warning: report could not be saved: {error}")

    print()
    print(SEPARATOR)
    print("  Analysis completed.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
