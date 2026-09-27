import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path

from expense_service import add_expense

DATA_FILE = Path("expenses.json")

parser = argparse.ArgumentParser(
    description="Expense Tracker"
)

subparsers = parser.add_subparsers(dest="command")

add_parser = subparsers.add_parser("add")

add_parser.add_argument(
    "--description",
    required=True
)

add_parser.add_argument(
    "--amount",
    required=True
)

args = parser.parse_args()

if args.command == "add":
    try:
        amount = Decimal(args.amount)
        
        expense = add_expense(
            file_path=DATA_FILE,
            description=args.description,
            amount=amount 
        )
        
        print(f"Expense added successfully (ID: {expense.id})")
        
    except InvalidOperation:
        print("Error: amount must be a valid number")

    except ValueError as error:
        print(f"Error: {error}")
    