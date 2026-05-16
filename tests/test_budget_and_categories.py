from budget_analyzer import budget_status
from category_analyzer import sum_by_category


def test_budget_status_red():
    assert budget_status(900, 1000) == "ROT"


def test_budget_status_green():
    assert budget_status(300, 1000) == "GRÜN"


def test_sum_by_category():
    result = sum_by_category([{"category": "claims", "amount": "100"}, {"category": "claims", "amount": "50"}])
    assert result["claims"] == 150
