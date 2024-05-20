from helpers import get_cities,get_ingredients, get_weather,get_currencies
import streamlit as st
import pandas as pd
import json

if 'items' not in st.session_state:
    st.session_state['items'] = []

st.title('Restaurant Menu Manager')

st.header('Restaurant Details')
restaurant_name = st.text_input('Enter the name of the restaurant')

city = st.selectbox('Choose the city', options=get_cities())
currency = st.selectbox('Choose the currency', options=get_currencies())

st.header('Add Menu Item')
dish_name = st.text_input('Dish Name')
dish_price = st.number_input('Price', min_value=0.0, format="%.2f")

ingredients = st.multiselect('Ingredients Used', options=get_ingredients())

if st.button('Add Item'):
    if restaurant_name and city and currency and dish_name and dish_price and ingredients:
        st.session_state['items'].append({
            'Dish Name': dish_name,
            'Price': f"{currency} {dish_price:.2f}",
            'Ingredients': ', '.join(ingredients)
        })
        st.success(f"Added {dish_name} to the menu.")
    else:
        st.error("Please fill out all fields before adding an item.")

if st.session_state['items']:
    st.header('Menu Items')
    df = pd.DataFrame(st.session_state['items'])
    df.index += 1
    st.table(df)
else:
    st.info('No items in the menu yet.')

ResetBtn,CookBtn=st.columns([1,1])

with ResetBtn:
    if st.button('Reset Menu'):
        st.session_state['items'] = []
        st.success('Menu has been reset.')

with CookBtn:
    if st.button('Cook Menu'):
        if st.session_state['items']:
            menu_data = {
                "filename":restaurant_name.replace(' ',''),
                'restaurant_name': restaurant_name,
                'city': city,
                'currency': currency,
                'items': st.session_state['items']
            }
            with open(fr'Menus\{menu_data["filename"]}.json', 'w') as json_file:
                json.dump(menu_data, json_file, indent=4)
            st.success('Menu has been saved to menu.json.')
        else:
            st.error('No items to save.')
