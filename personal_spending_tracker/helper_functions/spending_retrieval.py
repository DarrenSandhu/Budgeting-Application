
# a recursive function for sorting spendings into days of the cycle  
def check_if_is_this_days_spending(spending, n):
    if (spending.date.day) == n + 1: 
        return n
    else:
        return check_if_is_this_days_spending(spending, n+1)