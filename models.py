class Expense:
    def __init__(self,id,description,amount,date):
        
        if not description.strip():
            raise ValueError("Description cannot be empty")
        
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        
        self.id = id
        self.description = description.strip()
        self.amount = amount
        self.date = date
            
        
    def to_dict(self):
        return {
            "id" : self.id,
            "description" : self.description,
            "amount" : str(self.amount),
            "date" : self.date.isoformat()
        }