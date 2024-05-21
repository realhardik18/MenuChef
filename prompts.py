def categorize_food_prompt(item):
    return f'{item} would be in which team? reply 0 for cold, 1 for hot, 2 for room-temprature in one word and one word only and strictly from the options. if you are confused between 2 choices choose any one'

def description_prompt(dish,weather,favourable):
    if favourable:
        return f'write a small intro about 20 words for an item called {dish} on the menu. it is {weather} outside. add 2 emojis at the end'
    else:
        return f'write a small intro about 25 words for an item called {dish} on the menu add 2 emojis in the end'

#print(categorize_food_prompt('pizza'))
