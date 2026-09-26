#This test was initially generated with AI assistance 
#and then reviewed and modified by me.
import unittest
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from expense_service import add_expense
from storage import load_data


class TestExpenseService(unittest.TestCase):

    def test_add_expense(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            expense = add_expense(
                file_path=file_path,
                description="Lunch",
                amount=Decimal("20.50")
            )

            self.assertEqual(expense.id, 1)
            self.assertEqual(expense.description, "Lunch")
            self.assertEqual(expense.amount, Decimal("20.50"))

            data = load_data(file_path)

            self.assertEqual(data["last_id"], 1)
            self.assertEqual(len(data["expenses"]), 1)

            saved_expense = data["expenses"][0]

            self.assertEqual(saved_expense["id"], 1)
            self.assertEqual(saved_expense["description"], "Lunch")
            self.assertEqual(saved_expense["amount"], "20.50")