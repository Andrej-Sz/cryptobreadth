import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

def create_header():
    st.markdown("""
        <style>
        .header {
            background-color: #0D1824;
            padding: 20px;
            text-align: center;
            color: white;
            font-size: 64px;
            font-weight: bold;
            width: 100vw;
            position: fixed;
            top: 0;
            left: 0;
            z-index: 1000;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px; /* Tiny space above the text */
        }
        .stApp {
            padding-top: 80px;
        }

        </style>
        <div class="header">
            Crypto Breadth & Speculation Index
        </div>
        """, unsafe_allow_html=True)

def set_background():
    st.markdown("""
        <style>
        .stApp {
            background-color: #1D2B3A;
        }
        </style>
        """, unsafe_allow_html=True)

@st.cache_data(ttl=600)
def get_data(sheet_name):
    # Fetch data from the Google Apps Script API using the specified sheet name
    url = f'https://script.google.com/macros/s/AKfycbyArX-VqTB_BGt_iRJ-2vCPu1mfY4McZw85m7XJu6nOeXvwt1suVoCwAhPdYlNdRrQn/exec?sheet={sheet_name}'
    response = requests.get(url)  # Send a GET request to the API
    return response

# Configure the Streamlit page layout to be wide
st.set_page_config(layout = "wide")
create_header()
set_background()

# Separator
st.write("---")

st.markdown("<h2 style='text-align: center; color: white;'><a href='https://trw-toolbox.streamlit.app/Crypto-Breadth'>THIS APP WAS MOVED TO A DIFFERENT DASHBOARD, click on this text to be redirected to the new dashboard.</a></h2>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: white;'>Or search for: https://trw-toolbox.streamlit.app/Crypto-Breadth.</h2>", unsafe_allow_html=True)

st.write("---")
