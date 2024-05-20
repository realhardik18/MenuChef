from creds import WEATHER_API_KEY,WEATHER_API_URL,SNOWFLAKE_API_TOKEN
from prompts import categorize_food_prompt
import requests
import replicate
import json

replicate=replicate.Client(api_token=SNOWFLAKE_API_TOKEN)

def get_weather(city):
    response = requests.get(
        WEATHER_API_URL+city.format(city),
        headers={'X-Api-Key': WEATHER_API_KEY})
    print(response.text)

def recommend_food_type(temperature, humidity):
    if temperature <= 15:
        if humidity > 50:
            return 1
        else:
            return 2
    elif 15 < temperature <= 25:
        if humidity > 60:
            return 1
        elif 40 <= humidity <= 60:
            return 2
        else:
            return 0
    else:
        if humidity > 50:
            return 2
        else:
            return 0

def categorize_food(item):
    input = {
    "prompt": categorize_food_prompt(item=item),
    "temperature": 0.2
    }
    responses=list()
    for event in replicate.stream("snowflake/snowflake-arctic-instruct",input=input):
        responses.append(str(event))
    return ''.join(responses).strip(' ')

def get_currencies():
    with open('DropDownOptions\currencies.txt','r') as file:
        currencies='%'.join(file.readlines()).replace('\n','').replace('\t','').split('%')    
    return currencies

def get_cities():
    with open('DropDownOptions\cities.txt','r') as file:
        cities='%'.join(file.readlines()).replace('\n','').replace('\t','').split('%')    
    return cities

def get_ingredients():
    with open('DropDownOptions\Ingredients.txt','r') as file:
        ingredients='%'.join(file.readlines()).replace('\n','').replace('\t','').split('%')    
    return ingredients

def add_details(filename):
    with open(f'Menus\{filename}') as file:
        data=json.load(file)
    for dish in  data['items']:
        dish['type']=categorize_food(dish['Dish Name'])
        dish['Ingredients']=dish['Ingredients'].replace(', ','|')
    print(data)

def create_page(filename):
    markdown_data=''
    with open(f'Menus\{filename}') as file:
        data=json.load(file)
    markdown_data+=f"##{data['restaurant_name']}\n"


#print(create_page('jj'))
add_details("hardik'skitchen.json")
#print(recommend_food_type(24,84))