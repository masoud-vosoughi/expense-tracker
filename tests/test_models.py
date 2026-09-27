import unittest
from datetime import datetime, timezone
from decimal import Decimal

from models import Expense


class TestExpense(unittest.TestCase):
    def test_create_valid_expense(self):
        expense = Expense(
            id=1,
            description="Lunch",
            amount=Decimal("20.50"),
            date=datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(expense.id, 1)
        self.assertEqual(expense.description, "Lunch")
        self.assertEqual(expense.amount, Decimal("20.50"))
        self.assertEqual(
            expense.date, datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc)
        )

    def test_create_with_empty_description(self):
        with self.assertRaises(ValueError):
            Expense(
                id=2,
                description="",
                amount=Decimal("20.00"),
                date=datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc),
            )

    def test_create_with_space_description(self):
        with self.assertRaises(ValueError):
            Expense(
                id=3,
                description="   ",
                amount=Decimal("20.00"),
                date=datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc),
            )

    def test_create_with_neg_amount(self):
        with self.assertRaises(ValueError):
            Expense(
                id=3,
                description="Unknown price",
                amount=Decimal(-10),
                date=datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc),
            )

    def test_create_zero_amount(self):
        expense = Expense(
            id=2,
            description="Unknown price",
            amount=Decimal(0),
            date=datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc),
        )

        self.assertEqual(expense.id, 2)
        self.assertEqual(expense.description, "Unknown price")
        self.assertEqual(expense.amount, Decimal(0))
        self.assertEqual(
            expense.date, datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc)
        )

    def test_expense_to_dict(self):
        expense = Expense(
            id=1,
            description="Lunch",
            amount=Decimal("20.50"),
            date=datetime(2026, 9, 22, 12, 0, tzinfo=timezone.utc),
        )
        data = expense.to_dict()

        self.assertEqual(data["id"], 1)
        self.assertEqual(data["description"], "Lunch")
        self.assertEqual(data["amount"], "20.50")
        self.assertEqual(data["date"], "2026-09-22T12:00:00+00:00")
