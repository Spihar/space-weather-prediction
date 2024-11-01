import requests
import streamlit as st
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