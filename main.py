import streamlit as st
import requests
from bs4 import BeautifulSoup
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="🌤️ Weather Dashboard", layout="wide")

# Auto-refresh every 10s
st_autorefresh(interval=60_000, limit=None, key="weather_refresh")
    
st.markdown("""<style>
            header{
                display:none !important;
            }
            body *{
                margin:0 !important;
                padding:0 !important;
            }
            .st-emotion-cache-1vo6xi6{
                display:none !important;
            }
            </style>""",unsafe_allow_html=True)
@st.cache_data(ttl=10)
def fetch_weather_data():
    url = "https://localweatherplus.com/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)..."}
    res = requests.get(url, headers=headers, timeout=60)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")

    def clean(s): return s.replace("°F", "").replace("mph", "").replace("in", "").strip()


    return {
        "condition": soup.find(id="ajaxcurrentcond").get_text(strip=True),
        "temp": clean(soup.find(id="ajaxtemp").get_text(strip=True)),
        "heat_index": clean(soup.select_one("span#ajaxheatidx").get_text(strip=True)),
        "wind_speed": clean(soup.find(id="ajaxwind").get_text(strip=True)),
        "rain_today": clean(soup.find(id="ajaxrain").get_text(strip=True)),
        "rain_yesterday": clean(soup.find(id="ajaxrainydy").get_text(strip=True)),
        "rain_month": clean(soup.find(id="ajaxrainmo").get_text(strip=True)),
        "humidity": clean(soup.find(id="ajaxhumidity").get_text(strip=True)),
        "dew_point": clean(soup.find(id="ajaxdew").get_text(strip=True)),
        "pressure": clean(soup.find(id="ajaxbaro").get_text(strip=True)),
    }

 
try:
    data = fetch_weather_data()

    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    for k, v in data.items():
        html = html.replace(f"{{{{{k}}}}}", v)

    with open("style.css") as f: css = f"<style>{f.read()}</style>"
    with open("script.js") as f: js = f"<script>{f.read()}</script>"

    st.components.v1.html(css + html + js, height=730, scrolling=True)

except Exception as e:
    st.error(f"Error: {e}")
    