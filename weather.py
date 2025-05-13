import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

# Desativar a observação de arquivos para o Streamlit no Docker
# st.set_option('server.headless', True)

# Set the background image
background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.pexels.com/photos/1118873/pexels-photo-1118873.jpeg");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

# Chave de API da OpenWeatherMap (substitua pela sua chave)
API_KEY = "51f1e5703584628c4080f85fa68ef240"

def obter_previsao_tempo(citta):
    endpoint = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": citta,
        "appid": API_KEY,
        "units": "metric",  # Use "imperial" para Fahrenheit ou "metric" para Celsius
        "lang": "pt_br"  
    }

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        meteo = response.json()
        return meteo
    else:
        st.error(f"Errore: {response.status_code}")
        return None

def esibire_previsioni_tempo(meteo):
    if meteo:
        st.write(f"**Citta:** {meteo['name']}")
        st.write(f"**Paese:** {meteo['sys']['country']}")
        st.write(f"**Temperatura Attuale:** {meteo['main']['temp']}°C")
        st.write(f"**Ora:** {meteo['weather'][0]['description'].capitalize()}")
        return (meteo['coord']['lat'], meteo['coord']['lon'], meteo)
    else:
        st.warning("Inserire nome citta valida")
        return None

def exibir_mapa(latitude, longitude, meteo):
    st.write("**Mappa della citta**")
    m = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    # Criar o conteúdo do pop-up sem folium.Popup
    pop_up_content = f"""
    <b>Citta:</b> {meteo['name']}<br>
    <b>Paese:</b> {meteo['sys']['country']}<br>
    <b>Temperatura Attuale:</b> {meteo['main']['temp']}°C<br>
    <b>Tempo:</b> {meteo['weather'][0]['description'].capitalize()}
    """

    # Adicionar o marcador com o conteúdo do pop-up
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(folium.Html(pop_up_content, script=True)),
        icon=folium.Icon(color='blue')
    ).add_to(m)

    folium_static(m)

def main():
    st.title("App di previsione meteo e mappa")

    # Inserir o nome da cidade
    cidade = st.text_input("Inserire nome citta:")

    # Botão para obter a previsão do tempo
    if st.button("Ottenere le previsioni del tempo"):
        if citta:
            meteo = esibire_previsioni_tempo(citta)
            coordinate = exibir_previsao_tempo(dados_clima)
            if coordinate:
                exibir_mapa(*coordenadas)

        else:
            st.warning("Inserire nome dell .")

if __name__ == "__main__":
    main()