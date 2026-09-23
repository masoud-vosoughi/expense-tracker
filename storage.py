import json


def load_data(file_path):
    if file_path.exists():
        with file_path.open("r") as file:
            data = json.load(file)
            return data

    else:
        expenses_dict = {
            "expenses":[],
            "last_id":0
                         }
        return expenses_dict