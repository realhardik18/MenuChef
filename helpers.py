from prompts import categorize_food_prompt,description_prompt
import streamlit as st
import requests
import replicate
import json

replicate=replicate.Client(api_token=st.secrets("SNOWFLAKE_API_TOKEN"))

def get_weather(city):
    response = requests.get(
        st.secrets("WEATHER_API_URL")+city.format(city),
        headers={'X-Api-Key': st.secrets("WEATHER_API_KEY")})
    return response.json()

def recommend_food_type(temperature):
    score_HTF=0
    score_CTF=0
    score_RTF=0
    #0 for cold food
    #1 for hot-food
    #2 for room-food
    if temperature <= 20:
        score_HTF+=1
        score_CTF-=1
    elif 20 < temperature <= 35:
        score_RTF+=1
        score_CTF-=1
    else:
        score_CTF+=1
        score_HTF-=1
    hierarchy={
        "0":score_CTF,
        "1":score_HTF,
        "2":score_RTF
    }
    final=sorted(hierarchy.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in final]

def describe_weather(city):
    temperature_celsius=get_weather(city)['temp']
    if temperature_celsius < 0:
        return "freezing"
    elif 0 <= temperature_celsius < 10:
        return "very cold"
    elif 10 <= temperature_celsius < 20:
        return "a bit chilly"
    elif 20 <= temperature_celsius < 35:
        return "nice and warm"
    elif 35 <= temperature_celsius < 50:
        return "very hot"
    
def categorize_food(item):
    input = {
    "prompt": categorize_food_prompt(item=item),
    "temperature": 0.2
    }
    responses=list()
    for event in replicate.stream("snowflake/snowflake-arctic-instruct",input=input):
        responses.append(str(event))
    return ''.join(responses).strip(' ')

def generate_description(item,city,favorable):
    weather=describe_weather(city)
    input = {
    "prompt": description_prompt(dish=item,weather=weather,favourable=favorable),
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
    for dish in data['items']:
        dish['type']=categorize_food(dish['Dish Name'])
        dish['Ingredients']=dish['Ingredients'].replace(', ',' | ')
        dish['DescriptionF']=generate_description(dish['Dish Name'],data['city'],True)
        dish['DescriptionNF']=generate_description(dish['Dish Name'],data['city'],False)
    file.close()
    with open(f'Menus\{filename}', "w") as file:
        json.dump(data, file,indent=4)

def generate_item(dish_data,favourable):
    if favourable:
        end='F'
    else:
        end='NF'
    dish_markdown=''
    dish_markdown+=f"### **{dish_data['Dish Name']}** - {dish_data['Price']}\n"
    dish_markdown+=f"- *{dish_data['Description'+end]}*\n"
    dish_markdown+=f"   - *{dish_data['Ingredients']}*\n"
    return dish_markdown

def generate_markdown(filename):
    with open(f'Menus\{filename}') as file:
        data=json.load(file)    
    hierarchy=recommend_food_type(get_weather(data['city'])['temp']) 
    markdown_data=''        
    markdown_data+=f"# {data['restaurant_name']}\n"
    dishes=list()
    for i in hierarchy:
        for dish in data['items']:
            if dish['type']==i:
                dishes.append(dish)
    for dish in dishes:
        if dish['type']==hierarchy[0]:
            markdown_data+=generate_item(dish,True)
        else:
            markdown_data+=generate_item(dish,False)
    return markdown_data

def create_page(filename):
    filename_python="".join(x for x in filename.replace('.json','') if x.isalnum())+'.py'
    with open(f'pages/{filename_python}','w',encoding="utf-8") as file:
        file.write('import streamlit as st\n')
        file.write('from helpers import generate_markdown\n')        
        file.write('st.set_page_config(initial_sidebar_state="collapsed")\n')
        file.write('st.markdown("""<style>[data-testid="collapsedControl"] {display: none}</style>""",unsafe_allow_html=True)\n')
        file.write(f'data=generate_markdown("{filename}")\n')
        file.write(f'st.markdown(data)\n')

#print(create_page#"hardik'skitchen.json"))