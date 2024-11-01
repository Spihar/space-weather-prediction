import streamlit as st
def page_design():
    # Set the page config at the very top
    st.set_page_config(page_title="Space Weather Prediction System", layout="wide")

    # Set the background image with transparency
    background_image_path = "https://r4.wallpaperflare.com/wallpaper/751/849/165/space-galaxy-universe-space-art-wallpaper-a930f8fd615aadabe667486f9001b64d.jpg"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{background_image_path}");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
        }}
        .stButton {{
            transition: background-color 0.3s ease, transform 0.3s ease;
            margin-top: 10px;
            margin-bottom: 10px;
        }}
        .stButton:hover {{
            background-color: #1e3a8a; /* Darker shade for hover */
            transform: scale(1.05); /* Slightly enlarge the button on hover */
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            flex-direction: column;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    # Title and Buttons with an Icon
    st.markdown("""
        <h1 style="text-align: center;">
            <img src="https://img.icons8.com/external-flat-juicy-fish/64/external-space-astronaut-flat-flat-juicy-fish.png" style="vertical-align: middle; margin-right: 10px;"/> 
            Space Weather Prediction System
        </h1>
        """, unsafe_allow_html=True)

    # Create button containers for top and bottom buttons

