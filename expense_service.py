from datetime import datetime
from decimal import Decimal

from models import Expense
from storage import load_data, save_data


def add_expense(file_path, description, amount):
    
    data = load_data(file_path)
    
    new_id = data["last_id"] + 1
    current_date = datetime.now().astimezone()
    
    expense = Expense(
        id=new_id,
        description=description,
        amount=amount,
        date=current_date
    )
    
    data["expenses"].append(expense.to_dict())
    data["last_id"] = new_id
    
    save_data(file_path, data)
    
    return expense


def update_expense(file_path, expense_id, description=None, amount=None):
    data = load_data(file_path)
    target_expense = None
    expense_index = None
    for index, expense in enumerate(data["expenses"]):
        if expense_id == expense["id"]:
            target_expense = expense
            expense_index = index
            break
    if target_expense is None:
        raise ValueError("Expense not found")
    
    if description is None and amount is None:
        raise ValueError("No fields provided for update")
    
    old_expense = Expense.from_dict(target_expense)
    if description is not None:
        new_description = description
    else:
        new_description = old_expense.description
        
    if amount is not None:
        new_amount = amount
    else:
        new_amount = old_expense.amount
        
    updated_expense = Expense(
        id=old_expense.id,
        description=new_description,
        amount=new_amount,
        date=old_expense.date
    )
    
    data["expenses"][expense_index] = updated_expense.to_dict()
    save_data(file_path,data)
    
    return updated_expense


def delete_expense(file_path, expense_id):
    data = load_data(file_path)
    expense_index = None
    
    for index, expense in enumerate(data["expenses"]):
        if expense_id == expense["id"]:
            expense_index = index
            break
        
    if expense_index is None:
        raise ValueError("Expense not found")
    
    deleted_expense_data = data["expenses"].pop(expense_index)
    
    save_data(file_path, data)
    
    return Expense.from_dict(deleted_expense_data)


def list_expenses(file_path):
    data = load_data(file_path)
    expenses_list = []
    
    
    for expense in data["expenses"]:
        expense_object = Expense.from_dict(expense)
        expenses_list.append(expense_object)
        
    
    return expenses_list
    
    
def get_total_expense(file_path):
    total = Decimal(0)
    data = load_data(file_path)
    for expense in data["expenses"]:
        amount = Decimal(expense["amount"])
        total += amount
    return total

def get_monthly_total(file_path, month):
    if month not in range(1,13):
        raise ValueError(
            "Invalid month. Month must be an integer between 1 and 12"
            )
    
    total = Decimal(0)
    data = load_data(file_path)
    current_year = datetime.now().astimezone().year
        
    for expense in data["expenses"]:
        expense_date = datetime.fromisoformat(expense["date"]) 
        if month == expense_date.month and expense_date.year == current_year:
            amount = Decimal(expense["amount"])
            total += amount
    return total
        