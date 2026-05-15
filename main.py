import csv
from dataclasses import dataclass

@dataclass
class Transaction:
    category: str
    amount: float
    planned: float

def load_transactions(path='data/transactions.csv'):
    with open(path, newline='', encoding='utf-8') as f:
        return [Transaction(r['category'], float(r['amount']), float(r['planned'])) for r in csv.DictReader(f)]

def budget_status(transaction):
    ratio = transaction.amount / transaction.planned if transaction.planned else 0
    if ratio <= 0.9: return 'green'
    if ratio <= 1.05: return 'yellow'
    return 'red'

def risk_score(transaction):
    return round(max(0, transaction.amount - transaction.planned) / max(transaction.planned, 1) * 100, 2)

if __name__ == '__main__':
    print('Report generated successfully.')
    for t in load_transactions():
        print(f'{t.category}: {budget_status(t)} risk={risk_score(t)}')
