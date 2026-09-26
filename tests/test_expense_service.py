# This test was initially generated with AI assistance
# and then reviewed and modified by me.

import unittest
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from tempfile import TemporaryDirectory

from expense_service import (
    add_expense,
    delete_expense,
    get_monthly_total,
    get_total_expense,
    update_expense,
)
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

    def test_update_expense(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            original = add_expense(
                file_path=file_path,
                description="Lunch",
                amount=Decimal("20.50")
            )

            updated = update_expense(
                file_path=file_path,
                expense_id=original.id,
                description="Dinner"
            )

            self.assertEqual(updated.id, original.id)
            self.assertEqual(updated.description, "Dinner")
            self.assertEqual(updated.amount, Decimal("20.50"))
            self.assertEqual(updated.date, original.date)

    def test_delete_expense(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            first_expense = add_expense(
                file_path=file_path,
                description="Lunch",
                amount=Decimal("20.50")
            )

            second_expense = add_expense(
                file_path=file_path,
                description="Taxi",
                amount=Decimal("10.00")
            )

            deleted_expense = delete_expense(
                file_path=file_path,
                expense_id=first_expense.id
            )

            self.assertEqual(deleted_expense.id, first_expense.id)
            self.assertEqual(deleted_expense.description, "Lunch")

            data = load_data(file_path)

            self.assertEqual(len(data["expenses"]), 1)
            self.assertEqual(
                data["expenses"][0]["id"],
                second_expense.id
            )

            self.assertEqual(data["last_id"], 2)

    def test_get_total_expense(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            add_expense(
                file_path=file_path,
                description="Lunch",
                amount=Decimal("20.50")
            )

            add_expense(
                file_path=file_path,
                description="Taxi",
                amount=Decimal("10.00")
            )

            total = get_total_expense(file_path)

            self.assertEqual(total, Decimal("30.50"))

    def test_get_total_expense_when_empty(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            total = get_total_expense(file_path)

            self.assertEqual(total, Decimal("0"))

    def test_get_monthly_total(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            add_expense(
                file_path=file_path,
                description="Lunch",
                amount=Decimal("20.50")
            )

            add_expense(
                file_path=file_path,
                description="Taxi",
                amount=Decimal("10.00")
            )

            current_month = datetime.now().month

            total = get_monthly_total(
                file_path=file_path,
                month=current_month
            )

            self.assertEqual(total, Decimal("30.50"))

    def test_get_monthly_total_with_invalid_month(self):
        with TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "expenses.json"

            with self.assertRaises(ValueError):
                get_monthly_total(
                    file_path=file_path,
                    month=13
                )


if __name__ == "__main__":
    unittest.main()