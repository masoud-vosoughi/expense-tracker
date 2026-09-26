from datetime import datetime

from models import Expense
from storage import load_data, save_data


def add_expense(file_path, description, amount):
    
    data = load_data(file_path)
    
    new_id = data["last_id"] + 1
    current_date = datetime.now()
    
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