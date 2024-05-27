import os
import streamlit as st

from dotenv import load_dotenv, find_dotenv
_= load_dotenv(find_dotenv())

myvar = os.getenv('TAVILY_API_KEY')
openapikey= "sk-proj-A7WaN8QzHzHfX1gxAWtQT3BlbkFJBBuT10WWn44MP9B6A3PM"
st.write(myvar)
