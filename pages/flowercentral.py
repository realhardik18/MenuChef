import streamlit as st
from helpers import generate_markdown
st.set_page_config(initial_sidebar_state="collapsed")
st.markdown("""<style>[data-testid="collapsedControl"] {display: none}</style>""",unsafe_allow_html=True)
data=generate_markdown("flowercentral.json")
st.markdown(data)
