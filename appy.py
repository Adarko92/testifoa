import os
from dotenv import load_dotenv
import requests
import streamlit as st

load_dotenv()
API_KEY = os.getenv('API_key')

st.title("Inserire latitudine e longitudine")

lat = st.number_input("Latitudine", value=44.5, format="%.4f")
lon = st.number_input("Longitudine", value=11.3, format="%.4f")

if st.button("Mostra Meteo"):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}"
    res = requests.get(url).json()
    st.metric("Temperatura", f"{res['main']['temp']} °C")
    st.write(res['weather'][0]['description'].capitalize())
    st.write(f"Umidità: {res['main']['humidity']} %")
    st.write(f"Vento: {res['wind']['speed']} m/s")