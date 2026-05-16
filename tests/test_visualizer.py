import pandas as pd

from src.visualizer import _budget_color, plot_expenses_by_category


def test_charts_dir_created(tmp_path):
    output_dir = tmp_path / "charts"
    df = pd.DataFrame(
        [{"date": "2026-05-01", "type": "EXPENSE", "category": "Miete", "amount": 800.0}]
    )

    plot_expenses_by_category(df, output_dir)

    assert output_dir.exists()


def test_png_file_created(tmp_path):
    output_dir = tmp_path / "charts"
    df = pd.DataFrame(
        [{"date": "2026-05-01", "type": "EXPENSE", "category": "Miete", "amount": 800.0}]
    )

    plot_expenses_by_category(df, output_dir)

    assert (output_dir / "ausgaben_kategorien.png").exists()


def test_budget_gauge_colors():
    assert _budget_color(69.9) == "#2ca02c"
    assert _budget_color(70.0) == "#ffcc00"
    assert _budget_color(90.0) == "#ffcc00"
    assert _budget_color(90.1) == "#d62728"
