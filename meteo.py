# import streamlit as st
# import os 
# from dotenv import load_dotenv
# import requests 

# load_dotenv()

# api_key = os.getenv('API_key')

# def weather_search(city):
#     url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
#     result = requests.get(url)  
#     return result.json()

# def weather_var(city):
#     data = weather_search(city)
#     temperatura = round(data['main']['temp']-273.15,2)
#     meteo = data['weather'][0]['main']
#     umidita = data['main']['humidity']
#     temp_min = round(data['main']['temp_min']-273.15,2)
#     temp_max= round(data['main']['temp_max']-273.15,2)
#     result= [temperatura,meteo,umidita,temp_min,temp_max]
#     return result



# def main():
#     st.title("Weather time")
#     city = st.text_input("Inserisci una città",'Modena')
#     result = weather_var(city)
#     temperatura = result[0]
#     meteo = result[1]
#     umidita = result[2]
#     temp_min = result[3]
#     temp_max=result[4]

#     st.write(f"*Temperatura:* {temperatura}°C")
#     st.write(f"*Meteo:* {meteo}")
#     st.write(f"*Umidità:* {umidita}%")
#     st.write(f"*Temperatura minima:* {temp_min}°C")
#     st.write(f"*Temperatura massima:* {temp_max}°C")


# if __name__== "__main__":
#     main()

import streamlit as st
#import os 
#from dotenv import load_dotenv
import requests 
import pandas as pd

#load_dotenv()

#api_key = os.getenv('API_key')
api_key=st.secrets['api_key']

def weather_search(city):
    url =f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=it'
    result = requests.get(url)  
    return result.json()

def get_weather_emoji(condition):
    condition = condition.lower()
    if "clear" in condition:
        return "☀️"
    elif "cloud" in condition:
        return "☁️"
    elif "rain" in condition:
        return "🌧️"
    elif "thunderstorm" in condition:
        return "⛈️"
    elif "snow" in condition:
        return "❄️"
    elif "mist" in condition or "fog" in condition:
        return "🌫️"
    else:
        return "🌡️"

def weather_var(city):
    data = weather_search(city)
    temperatura = round(data['main']['temp'] - 273.15, 2)
    meteo = data['weather'][0]['main']
    umidita = data['main']['humidity']
    temp_min = round(data['main']['temp_min'] - 273.15, 2)
    temp_max = round(data['main']['temp_max'] - 273.15, 2)
    lat = data['coord']['lat']
    lon = data['coord']['lon']
    return [temperatura, meteo, umidita, temp_min, temp_max, lat, lon]

def main():
    st.title("🌍 Weather Time")

    city = st.text_input("Inserisci una città", 'Modena')

    try:
        result = weather_var(city)
        temperatura, meteo, umidita, temp_min, temp_max, lat, lon = result
        emoji = get_weather_emoji(meteo)

        st.subheader(f"Meteo attuale a {city}")
        st.write(f"{emoji} *Condizione:* {meteo}")
        st.write(f"🌡️ *Temperatura:* {temperatura}°C")
        st.write(f"📉 *Temperatura minima:* {temp_min}°C")
        st.write(f"📈 *Temperatura massima:* {temp_max}°C")
        st.write(f"💧 *Umidità:* {umidita}%")
        st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://pixabay.com/it/photos/fotografia-aerea-cielo-bianca-1381617.jpg");
            background-repeat: no-repeat;
            background-size: cover;
            background-attachment: fixed;
        }

        label {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

        st.subheader("📍 Mappa della città")
        city_map = pd.DataFrame({'lat': [lat], 'lon': [lon]})
        st.map(city_map)

    except KeyError:
        st.error("❌ Città non trovata. Verifica il nome e riprova.")

if __name__== "__main__":
    main()
