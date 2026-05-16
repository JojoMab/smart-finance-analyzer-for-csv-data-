from validator import validate_transaction


def test_valid_transaction():
    row = {"date": "2026-05-01", "category": "claims", "description": "Test", "amount": "100", "budget": "1000"}
    assert validate_transaction(row)


def test_invalid_date():
    row = {"date": "01.05.2026", "category": "claims", "description": "Test", "amount": "100", "budget": "1000"}
    assert not validate_transaction(row)
