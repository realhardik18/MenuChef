from helpers import get_cities,get_ingredients,get_currencies,add_details,create_page
import streamlit as st
import pandas as pd
import json

if 'items' not in st.session_state:
    st.session_state['items'] = []

st.set_page_config(initial_sidebar_state="collapsed")

st.markdown("""<style>[data-testid="collapsedControl"] {display: none}</style>""",unsafe_allow_html=True)

st.title('Welcome To MenuChef 👨‍🍳📃')
st.markdown('###### Enter the details below and we will cook a digital menu for you!')
st.markdown('###### Items in the menu will dynamically adjust according to the weather in your city!')

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
            st.success("Generating...")
            menu_data = {
                "filename":restaurant_name.replace(' ',''),
                'restaurant_name': restaurant_name,
                'city': city,
                'currency': currency,
                'items': st.session_state['items']
            }
            with open(fr'Menus\{menu_data["filename"]}.json', 'w') as json_file:
                json.dump(menu_data, json_file, indent=4)
            add_details(menu_data["filename"]+'.json')            
            create_page(menu_data["filename"]+'.json')            
            url=st.secrets("APP_URL")+menu_data["filename"]
            st.success("Your menu is live 🔗 [here!](%s)" % url)
        else:
            st.error('No items to save.')
