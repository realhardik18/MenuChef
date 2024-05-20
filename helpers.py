from creds import WEATHER_API_KEY,WEATHER_API_URL,SNOWFLAKE_API_TOKEN
from prompts import categorize_food_prompt
import requests
import replicate

replicate=replicate.Client(api_token=SNOWFLAKE_API_TOKEN)

def get_weather(city):
    response = requests.get(
        WEATHER_API_URL+city.format(city),
        headers={'X-Api-Key': WEATHER_API_KEY})
    print(response.text)

def recommend_food_type(temperature, humidity):
    items={
        'cold-shakes':0,
        'cold-dessert':0,
        'room-temp':0,
        'hot-soup':0,
        'hot-steamed':0,
        'hot-fried':0

    }
    if temperature >= 30:
        items['cold-shakes']+=1
        items['cold-dessert']+=1
        if humidity < 50:
            items['cold-shakes']+=1
        else:
            items['cold-dessert']+=1
    elif 20 <= temperature < 30:
        items['cold-dessert']+=1
        items['room-temp']+=1
        if humidity < 50:
            items['cold-dessert']+=1
        else:
            items['room-temp']+=1
    elif 10 <= temperature < 20:
        items['room-temp']+=1
        items['hot-soup']+=1
        if humidity >= 50:
            items['hot-soup']+=1
        else:
            items['room-temp']+=1
    else:
        items['hot-fried']+=1
        items['hot-steamed']+=1
        if humidity >= 50:
             items['hot-steamed']+=1
        else:
             items['hot-fried']+=1
    items=sorted(items.items(), key=lambda x:x[1])
    hierarchy=list()
    for item in items[::-1]:
        hierarchy.append(item[0])
    return hierarchy

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
    with open('currencies.txt','r') as file:
        currencies='%'.join(file.readlines()).replace('\n','').replace('\t','').split('%')    
    return currencies

def get_cities():
    with open('cities.txt','r') as file:
        cities='%'.join(file.readlines()).replace('\n','').replace('\t','').split('%')    
    return cities