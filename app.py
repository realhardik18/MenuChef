import streamlit as st
import pandas as pd

# Initialize a session state to store the table data
if 'data' not in st.session_state:
    st.session_state['data'] = []

# Title of the app
st.title('Name and Option Selector')

# Input fields
# Submit button
if st.button('Submit'):
    if name and option:
        # Add the input data to the session state
        st.session_state['data'].append({'Name': name, 'Option': option})
    else:
        st.error('Please enter a name and select an option.')

# Display the table
if st.session_state['data']:
    df = pd.DataFrame(st.session_state['data'])
    st.table(df)
