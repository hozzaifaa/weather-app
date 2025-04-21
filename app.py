import streamlit as st
import requests
import geocoder
import pandas as pd

# Session state for search history
if "history" not in st.session_state:
    st.session_state["history"] = []

# Get user's location using IP
def detect_location():
    g = geocoder.ip('me')
    return g.city if g.city else "New York"

# Set Streamlit layout
st.set_page_config(page_title="🌦️ Weather Dashboard", layout="centered")
st.title("🌤️ Real-Time Weather App")

# Get user input
default_city = detect_location()
city = st.text_input("Enter a city", default_city)

# Fetch and display weather
if st.button("Get Weather"):
    try:
        response = requests.get(f"http://localhost:8000/weather?city={city}")
        if response.status_code == 200:
            data = response.json()

            # Save to search history
            if city not in st.session_state["history"]:
                st.session_state["history"].append(city)

            # Layout with columns
            col1, col2 = st.columns([1, 2])

            with col1:
                st.image(data["icon_url"], width=100)
                st.metric("🌡️ Temperature", f"{data['temperature']} °C")
                st.metric("💧 Humidity", f"{data['humidity']}%")
                st.metric("🌬️ Wind", f"{data['wind_speed']} m/s")

            with col2:
                st.subheader(f"Weather in {data['city']}")
                st.write(f"📝 {data['description']}")

                # Map using coordinates from backend
                df = pd.DataFrame({
                    "lat": [data["lat"]],
                    "lon": [data["lon"]],
                })
                st.map(df)

        else:
            st.error("❌ Could not retrieve weather data.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# Show search history
if st.session_state["history"]:
    st.markdown("### 📍 Search History")
    for past_city in reversed(st.session_state["history"]):
        st.write(f"• {past_city}")
