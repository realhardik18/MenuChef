def categorize_food_prompt(item):
    return f'{item} would be in which team? cold(dessert),cold(shake),hot(soup),hot(steamed),hot(fried),hot(baked),room temprature. reply with a ? if you are not sure. reply strictly from the given options only and reply in one word only'

#print(categorize_food_prompt('pizza'))