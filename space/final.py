import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json #what can we do with this??
from emailsending import send_mail
from data import fetch_data
from ui import page_design
import datetime


# Updated URLs for the data
geomagnetic_storms_url = "https://kauai.ccmc.gsfc.nasa.gov/DONKI/WS/get/GST?startDate=2024-07-13&endDate=2024-08-13"
solar_flares_url = "https://api.nasa.gov/DONKI/FLR?startDate=2016-01-01&endDate=2016-01-30&api_key=hnu8s05TCBtkTBOvlbBHgDW7NBaqF53qMKg8X9a7"  # Replace YOUR_API_KEY with your actual API key

# Fetching the data
geomagnetic_storms_data = fetch_data(geomagnetic_storms_url)
solar_flares_data = fetch_data(solar_flares_url)


#calling ui
page_design()
with st.container():
    st.write("")
    show_geomagnetic_btn = st.button("Show Geomagnetic Storms Data", key="geomagnetic_button")
with st.container():
    st.write("")
    show_solar_flares_btn = st.button("Show Solar Flares Data", key="solar_flares_button")


if show_geomagnetic_btn:
    if geomagnetic_storms_data:
        st.header("Geomagnetic Storms")

        # Display image and description
        st.image("https://as1.ftcdn.net/v2/jpg/08/93/92/62/1000_F_893926290_FayyxhJMS2xCj73PNWhX6RRIgI8gk18s.jpg", caption="Geomagnetic Storms", use_column_width=True)
        st.write("""
            **Geomagnetic Storms** occur when there is a disturbance in Earth's magnetic field caused by solar wind and coronal mass ejections from the sun. These storms can lead to stunning auroras but can also disrupt communication systems, GPS, and power grids. Understanding these storms helps in preparing for their effects on our technology.
        """)

        # Visualization for geomagnetic storms data
        st.header("Geomagnetic Storms Visualization")
        df_geomagnetic = pd.json_normalize(geomagnetic_storms_data)#what is normalization??
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
    else:
        st.error("No Geomagnetic Storms data available.")

if show_solar_flares_btn:
    if solar_flares_data:
        st.header("Solar Flares")

        # Display image and description
        st.image("https://media.gettyimages.com/id/151330854/vector/solar-flare-hitting-earth-artwork.jpg?s=612x612&w=0&k=20&c=OiaUy-8nD-ODf7qsRIxTGWNGMYbh2eiVUSiKTKFLwOo=", caption="Solar Flares", use_column_width=True)
        st.write("""
            **Solar Flares** are sudden bursts of energy from the sun that release a massive amount of radiation into space. They can cause radio blackouts and affect satellite communications, navigation systems, and power grids. Monitoring solar flares helps in mitigating their impacts on our technology.
        """)

        # Visualization for solar flares data
        st.header("Solar Flares Visualization")
        df_solar_flares = pd.DataFrame(solar_flares_data)
        if not df_solar_flares.empty:
            st.write("Solar Flares DataFrame:", df_solar_flares.head())  # Inspect DataFrame

            # Debug: List all columns
            st.write("Columns in Solar Flares Data:", df_solar_flares.columns)

            # Example condition to send an alert email if there's a solar flare of class 'M'
            if 'classType' in df_solar_flares.columns and 'M' in df_solar_flares['classType'].values:
                send_mail("Solar Flare Alert", "A solar flare of class M has been detected!")

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
