import os

import matplotlib.pyplot as plt
import seaborn as sns


def _ensure_output_dir(output_dir):
    os.makedirs(output_dir, exist_ok=True)


def _format_euro(value):
    return f"{value:.2f} €".replace(".", ",")


def _expense_rows(df):
    if "type" not in df.columns:
        return df.copy()
    return df[df["type"].astype(str).str.upper() == "EXPENSE"].copy()


def _budget_color(pct: float) -> str:
    if pct > 90:
        return "#d62728"
    if pct >= 70:
        return "#ffcc00"
    return "#2ca02c"


def plot_expenses_by_category(df, output_dir):
    _ensure_output_dir(output_dir)
    expenses = _expense_rows(df)
    grouped = (
        expenses.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=True)
    )

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(grouped.index, grouped.values, color="#4C72B0")
    ax.set_title("Ausgaben nach Kategorie")
    ax.set_xlabel("Betrag in €")
    ax.set_ylabel("Kategorie")

    max_value = grouped.max() if not grouped.empty else 0
    offset = max_value * 0.01 if max_value else 1
    for index, value in enumerate(grouped.values):
        ax.text(value + offset, index, _format_euro(value), va="center")

    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "ausgaben_kategorien.png"), dpi=150)
    plt.close(fig)


def plot_monthly_balance(df, output_dir):
    _ensure_output_dir(output_dir)
    data = df.copy()
    data["date"] = data["date"].astype(str)
    data["month"] = data["date"].str[:7]
    if "type" not in data.columns:
        data["type"] = "EXPENSE"
    data["type"] = data["type"].astype(str).str.upper()

    monthly = (
        data.groupby(["month", "type"])["amount"]
        .sum()
        .unstack(fill_value=0)
        .sort_index()
    )
    income = monthly["INCOME"] if "INCOME" in monthly.columns else [0] * len(monthly)
    expenses = monthly["EXPENSE"] if "EXPENSE" in monthly.columns else [0] * len(monthly)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(monthly.index, income, color="#2ca02c", marker="o", label="Einnahmen")
    ax.plot(monthly.index, expenses, color="#d62728", marker="o", label="Ausgaben")
    ax.set_title("Monatliche Einnahmen und Ausgaben")
    ax.set_xlabel("Monat")
    ax.set_ylabel("Betrag in €")
    ax.legend()

    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "monatliche_bilanz.png"), dpi=150)
    plt.close(fig)


def plot_budget_gauge(total_expenses, budget, output_dir):
    _ensure_output_dir(output_dir)
    remaining = max(budget - total_expenses, 0)
    pct = (total_expenses / budget * 100) if budget else 0
    values = [total_expenses, remaining]
    labels = ["Verbraucht", "Verbleibend"]
    colors = [_budget_color(pct), "#d0d0d0"]

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.barh(labels, values, color=colors)
    ax.set_title("Budgetauslastung")
    ax.set_xlabel("Betrag in €")
    ax.text(
        0.5,
        -0.25,
        f"Budget: {_format_euro(budget)} | Verbraucht: {_format_euro(total_expenses)} | Verbleibend: {_format_euro(remaining)}",
        transform=ax.transAxes,
        ha="center",
        va="top",
    )

    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "budget_auslastung.png"), dpi=150)
    plt.close(fig)


def plot_expense_share_pie(df, output_dir):
    _ensure_output_dir(output_dir)
    expenses = _expense_rows(df)
    grouped = expenses.groupby("category")["amount"].sum()
    total = grouped.sum()
    if total > 0:
        small = grouped[grouped / total < 0.05]
        grouped = grouped[grouped / total >= 0.05]
        if not small.empty:
            grouped.loc["Sonstige"] = small.sum()

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(9, 7))
    colors = plt.get_cmap("tab10").colors
    ax.pie(grouped.values, autopct="%1.1f%%", startangle=90, colors=colors)
    ax.set_title("Ausgabenverteilung nach Kategorie")
    ax.legend(grouped.index, loc="center left", bbox_to_anchor=(1, 0.5))

    fig.tight_layout()
    plt.savefig(os.path.join(output_dir, "ausgaben_verteilung.png"), dpi=150)
    plt.close(fig)
