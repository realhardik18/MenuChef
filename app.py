import streamlit as st
import pandas as pd


st.title('Item List Manager')

if 'items' not in st.session_state:
    st.session_state['items'] = []


item_name = st.text_input('Item Name')
item_price = st.number_input('Item Price', min_value=0.0, step=0.01)

currencies = ['USD', 'EUR', 'GBP', 'JPY', 'AUD', 'CAD', 'CHF', 'CNY', 'SEK', 'NZD']
item_currency = st.selectbox('Currency', currencies)

if st.button('Add Item'):
    if item_name and item_price > 0:
        st.session_state['items'].append({'Name': item_name, 'Price': f'{item_price:.2f} {item_currency}'})
        st.success(f'Added {item_name} - {item_price:.2f} {item_currency}')
    else:
        st.error('Please enter both an item name and a valid price.')

if st.session_state['items']:
    df = pd.DataFrame(st.session_state['items'])
    st.write('## Items Table')
    st.table(df)
else:
    st.write('No items added yet.')

