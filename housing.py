
class Housing:
    def __init__(self, name, location, price, rating, status):
        self.name = name
        self.location = location
        self.price = price          # Monthly rent in USD
        self.rating = rating        # 1-10, 0 means unrated
        self.status = status

