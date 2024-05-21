import streamlit as st
from helpers import add_details,generate_markdown
#add_details("ramu'skitchen.json")
data=generate_markdown("ramu'skitchen.json")
st.markdown(data)
