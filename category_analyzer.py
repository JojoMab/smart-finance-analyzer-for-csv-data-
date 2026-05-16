def sum_by_category(transactions):
    result = {}
    for transaction in transactions:
        category = transaction["category"]
        result[category] = result.get(category, 0) + float(transaction["amount"])
    return result
