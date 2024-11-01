import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
from emailsending import send_mail

# Set the page config at the very top
st.set_page_config(page_title="Space Weather Prediction System", layout="wide")

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

# Function to read local JSON file
def read_local_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
    except json.JSONDecodeError:
        st.error("Error decoding JSON from file.")
    except Exception as err:
        st.error(f"An error occurred: {err}")
    return None

# Updated URLs and file paths for the data
geomagnetic_storms_url = "https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?startDate=2024-07-13&endDate=2024-08-13"
solar_flares_url = "https://api.nasa.gov/DONKI/FLR?startDate=2016-01-01&endDate=2016-01-30&api_key=hnu8s05TCBtkTBOvlbBHgDW7NBaqF53qMKg8X9a7"  # Replace YOUR_API_KEY with your actual API key
cosmic_rays_file_path = "C:/Users/PRUDHVI/Desktop/Auger_053385388700.json"

# Fetching the data
geomagnetic_storms_data = fetch_data(geomagnetic_storms_url)
solar_flares_data = fetch_data(solar_flares_url)
cosmic_rays_data = read_local_json(cosmic_rays_file_path)

# Set the background image
background_image_path = "C:/Users/PRUDHVI/AppData/Local/Programs/Python/Python312/Scripts/space-galaxy-universe-space-art-wallpaper-a930f8fd615aadabe667486f9001b64d.jpg"
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("file:///{background_image_path}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Buttons
st.title("Space Weather Prediction System")

# Buttons to show/hide data
if st.button("Show Geomagnetic Storms Data"):
    if geomagnetic_storms_data:
        st.header("Geomagnetic Storms")

        # Visualization for geomagnetic storms data
        st.header("Geomagnetic Storms Visualization")
        df_geomagnetic = pd.json_normalize(geomagnetic_storms_data)
        if not df_geomagnetic.empty:
            st.write("Geomagnetic Storms DataFrame:", df_geomagnetic.head())  # Inspect DataFrame

            # Extracting Kp Index data
            if 'allKpIndex' in df_geomagnetic.columns:
                all_kp_index = df_geomagnetic['allKpIndex'].apply(lambda x: x[0] if isinstance(x, list) and x else None)
                if all_kp_index.dropna().any():
                    kp_data = pd.json_normalize(all_kp_index)
                    if 'observedTime' in kp_data.columns and 'kpIndex' in kp_data.columns:
                        kp_data['observedTime'] = pd.to_datetime(kp_data['observedTime'])
                        plt.figure(figsize=(10, 5))
                        plt.plot(kp_data['observedTime'], kp_data['kpIndex'], label='Kp Index')
                        plt.xlabel('Time')
                        plt.ylabel('Kp Index')
                        plt.title('Geomagnetic Storms Kp Index Over Time')
                        plt.legend()
                        st.pyplot(plt)
                    else:
                        st.error("Expected columns 'observedTime' and 'kpIndex' not found in Kp data.")
                else:
                    st.error("No valid Kp Index data found.")
            else:
                st.error("Column 'allKpIndex' not found in geomagnetic storms data.")

if st.button("Show Solar Flares Data"):
    if solar_flares_data:
        st.header("Solar Flares")

        # Visualization for solar flares data
        st.header("Solar Flares Visualization")
        df_solar_flares = pd.DataFrame(solar_flares_data)
        if not df_solar_flares.empty:
            st.write("Solar Flares DataFrame:", df_solar_flares.head())  # Inspect DataFrame

            # Debug: List all columns
            st.write("Columns in Solar Flares Data:", df_solar_flares.columns)

            # Plotting based on available columns
            if 'beginTime' in df_solar_flares.columns:
                df_solar_flares['beginTime'] = pd.to_datetime(df_solar_flares['beginTime'])
                plt.figure(figsize=(10, 5))
                plt.plot(df_solar_flares['beginTime'], df_solar_flares.index, label='Solar Flares Events')
                plt.xlabel('Time')
                plt.ylabel('Event Index')
                plt.title('Solar Flares Events Over Time')
                plt.legend()
                st.pyplot(plt)
            else:
                st.error("Expected column 'beginTime' not found in the data.")
        else:
            st.error("Solar Flares DataFrame is empty.")
    else:
        st.error("No Solar Flares data available.")

if st.button("Show Cosmic Rays Data"):
    if cosmic_rays_data:
        st.header("Cosmic Rays")

        # Inspect the data structure to determine how to proceed
        if isinstance(cosmic_rays_data, dict):
            st.write("Cosmic Rays Data Keys:", cosmic_rays_data.keys())

            if 'sdrec' in cosmic_rays_data and isinstance(cosmic_rays_data['sdrec'], list):
                # Extract relevant fields for visualization
                times = []
                energies = []

                for entry in cosmic_rays_data['sdrec']:
                    time_entry = entry.get('timestamp')  # Assuming timestamp is the relevant time field
                    energy_entry = entry.get('energy')   # Assuming energy is the intensity

                    if time_entry and energy_entry:
                        times.append(pd.to_datetime(time_entry))
                        energies.append(energy_entry)

                if times and energies:
                    df_cosmic_rays = pd.DataFrame({
                        "Time": times,
                        "Energy": energies
                    })

                    st.write("Cosmic Rays DataFrame:", df_cosmic_rays.head())

                    # Visualization
                    plt.figure(figsize=(10, 5))
                    plt.plot(df_cosmic_rays['Time'], df_cosmic_rays['Energy'], label='Cosmic Ray Intensity')
                    plt.xlabel('Time')
                    plt.ylabel('Intensity (Energy)')
                    plt.title('Cosmic Ray Intensity Over Time')
                    plt.legend()
                    st.pyplot(plt)
                else:
                    st.error("No valid time or energy data found in the cosmic rays dataset.")
            else:
                st.error("'sdrec' field is missing or not a list in the cosmic rays data.")
        else:
            st.error("Cosmic rays data is not in the expected format.")
    else:
        st.error("No Cosmic Rays data available.")
