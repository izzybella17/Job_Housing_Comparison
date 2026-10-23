class Job:
    def __init__(self, name, position, location, base_pay, onsite_days, status):
        self.name = name                    # Comapany Name
        self.position = position            # Job Title
        self.location = location            
        self.base_pay = base_pay            # Annual Salary in USD
        self.onsite_days = onsite_days      # List of days required to be onsite
        self.status = status
    
