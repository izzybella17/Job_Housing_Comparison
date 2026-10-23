
def meters_to_miles(meters):
    # converts meter to miles
    if meters < 0:
        raise ValueError("Meters must be non negative.")
    return meters / 1609.344

def calculate_gas_cost(distance_miles, mpg, gas_price):
    # calculates cost of gas in dollars 
    # for a trip of given ditance 
    # in a car of given mpg
    if mpg <= 0:
        raise ValueError("MPG must be greater than zero.")
    if distance_miles < 0:
        raise ValueError("Distance must be non negative.")
    if gas_price < 0:
        raise ValueError("Gas price must be non negative.")
    return distance_miles / mpg * gas_price

def duration_to_seconds(time_string):
    # takes a string and converts it to a float
    # ex: '200s' -> 200
    new_string = time_string.replace("s","")
    time_float = float(new_string)
    return time_float

def seconds_to_display(time_float):
    # takes a number of seconds and converts it to readable time format
    # Displays whole minutes, dropping leftover seconds.
    # ex: 348 -> 5m or 12600 -> 3h30m
    total_minutes = int(time_float / 60)
    hours, minutes = divmod(total_minutes, 60)
    if hours >= 1:
        return f"{hours}h{minutes}m"
    return f"{minutes}m"

