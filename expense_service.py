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