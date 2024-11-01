import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from emailsending import send_mail

# Function to fetch data from a given URL
def fetch_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        return response.json()  # Try to parse JSON data
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except ValueError:
        st.error("The data is not in JSON format.")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Updated URLs for the data

geomagnetic_storms_url = "https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?startDate=2024-07-13&endDate=2024-08-13"
solar_flares_url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"
cosmic_rays_url = "https://www.nmdb.eu/api/v1/get_data?type=cosmicrays"

# Fetching the data

geomagnetic_storms_data = fetch_data(geomagnetic_storms_url)
solar_flares_data = fetch_data(solar_flares_url)
cosmic_rays_data = fetch_data(cosmic_rays_url)

# Streamlit interface
st.title("Space Weather Prediction System")

'''
# Geomagnetic Storms Data
if geomagnetic_storms_data:
    st.header("Geomagnetic Storms")
    st.write(geomagnetic_storms_data[:5])

    # Example visualization for geomagnetic storms data
    st.header("Geomagnetic Storms Visualization")
    df_geomagnetic = pd.DataFrame(geomagnetic_storms_data)
    if not df_geomagnetic.empty:
        df_geomagnetic['time_tag'] = pd.to_datetime(df_geomagnetic['time_tag'])
        plt.figure(figsize=(10, 5))
        plt.plot(df_geomagnetic['time_tag'], df_geomagnetic['kp_index'], label='Kp Index')
        plt.xlabel('Time')
        plt.ylabel('Kp Index')
        plt.title('Geomagnetic Storms Kp Index Over Time')
        plt.legend()
        st.pyplot(plt)'''

# Solar Flares Data
if solar_flares_data:
    st.header("Solar Flares")
    st.write(solar_flares_data[:5])

    # Example visualization for solar flares data
    st.header("Solar Flares Visualization")
    df_solar_flares = pd.DataFrame(solar_flares_data)
if not df_solar_flares.empty:
    df_solar_flares['time_tag'] = pd.to_datetime(df_solar_flares['time_tag'])
    plt.figure(figsize=(10, 5))
    plt.plot(df_solar_flares['time_tag'], df_solar_flares['flux'], label='Flux')
    for i in df_solar_flares["flux"]:
        if i>4:
            send_mail("solar flare alert")

    plt.xlabel('Time')
    plt.ylabel('Flux (W/m²)')
    plt.title('Solar X-ray Flux Over Time')
    plt.legend()
    st.pyplot(plt)

# Cosmic Rays Data
'''if cosmic_rays_data:
    st.header("Cosmic Rays")
    st.write(cosmic_rays_data[:5])  # Display the first 5 data points for simplicity

    # Example visualization for cosmic rays data
    st.header("Cosmic Rays Visualization")
    df_cosmic_rays = pd.DataFrame(cosmic_rays_data)
    if not df_cosmic_rays.empty:
        plt.figure(figsize=(10, 5))
        plt.plot(df_cosmic_rays['date'], df_cosmic_rays['intensity'], label='Cosmic Ray Intensity')
        plt.xlabel('Date')
        plt.ylabel('Intensity')
        plt.title('Cosmic Ray Intensity Over Time')
        plt.legend()
        st.pyplot(plt)'''
