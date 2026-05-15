import unittest
from main import Transaction, budget_status, risk_score

class FinanceTest(unittest.TestCase):
    def test_budget_status(self):
        self.assertEqual(budget_status(Transaction('claims',1200,1000)), 'red')
        self.assertGreater(risk_score(Transaction('claims',1200,1000)), 0)

if __name__ == '__main__': unittest.main()
