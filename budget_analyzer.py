def budget_status(spent, budget):
    remaining_ratio = (budget - spent) / budget if budget else 0
    if remaining_ratio < 0.20:
        return "ROT"
    if remaining_ratio <= 0.40:
        return "GELB"
    return "GRÜN"
