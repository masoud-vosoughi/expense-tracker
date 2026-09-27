import argparse
from decimal import Decimal, InvalidOperation
from pathlib import Path

from expense_service import (
    add_expense,
    delete_expense,
    get_monthly_total,
    get_total_expense,
    list_expenses,
    update_expense,
)

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

list_parser = subparsers.add_parser("list")

summary_parser = subparsers.add_parser("summary")

summary_parser.add_argument(
    "--month",
    required=False
)

update_parser = subparsers.add_parser("update")

update_parser.add_argument(
    "--id",
    required=True
)

update_parser.add_argument(
    "--description",
    required=False
)

update_parser.add_argument(
    "--amount",
    required=False
)

delete_parser = subparsers.add_parser("delete")

delete_parser.add_argument(
    "--id",
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
    

elif args.command == "list":
    expenses = list_expenses(DATA_FILE)
    if not expenses:
        print("No expenses found.")
        
    else:
        print(
            f"{'ID':<5} "
            f"{'Date':<12} "
            f"{'Description':<20} "
            f"{'Amount':>10}"
        )
        
        for expense in expenses:
            print(
                f"{expense.id:<5} "
                f"{expense.date.strftime('%Y-%m-%d'):<12} "
                f"{expense.description:<20} "
                f"{expense.amount:>10}"
                )
            
            
elif args.command == "delete":
    try:
        expense_id = int(args.id)
    except ValueError:
        print("Error: ID must be an integer")
    else:
        try:
            delete_expense(
                DATA_FILE,
                expense_id=expense_id
            )
            
            print("Expense deleted successfully")
            
        except ValueError as error:
            print(f"Error: {error}")


elif args.command == "update":
    if args.description is None and args.amount is None:
        print("Error: provide at least a description or an amount")
    else:
        try:
            expense_id = int(args.id)
        except ValueError:
            print("Error: ID must be an integer")
        else:
            try:
                if args.amount is not None:
                    amount = Decimal(args.amount)
                else:
                    amount = None
                
                update_expense(
                    file_path=DATA_FILE,
                    expense_id=expense_id,
                    description=args.description,
                    amount=amount
                    )
                print("Expense updated successfully")
                    
            except InvalidOperation:
                print("Error: amount must be a valid number")
                
            except ValueError as error:
                print(f"Error: {error}")
    
    
elif args.command == "summary":
        if args.month is None:
            total = get_total_expense(DATA_FILE)
            print(f"Total expenses: {total}")
            
        else:
            try:
                month = int(args.month)
            except ValueError:
                print("Error: month must be an integer")
            else:
                try:
                    total = get_monthly_total(DATA_FILE, month)
                    print(f"Total expenses for month {month}: {total}")
                except ValueError as error:
                    print(f"Error: {error}")