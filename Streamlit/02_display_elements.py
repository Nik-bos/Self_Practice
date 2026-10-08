import streamlit as st
import pandas as pd

data = {"Name": ['Nikunj', "Jugal", "Harshit", "Jenish", "Parth"],
       "Surname": ['Bosamiya', 'Bosamiya', 'Kamani', 'Mer', "Paghdar"],
        'Fav_Food': ['Pakoda', 'Vada-pav', 'Ghughra', 'Dabeli', 'Samosa']
       }
df = pd.DataFrame(data)
st.table(df)    # This will return the simple table
st.dataframe(df)    # dataframe() allows us to filter and sort the df in the app 

# ********************************************** Media Widgets **********************************************

st.image(image = ["jethalal.jpg", "jethalal.jpg"], caption = ["JC Gada1", 'JC Gada2'], width = 250)
st.audio(data = 'jethalal.mp3',format = 'audio', width = 500, autoplay = False)
st.video(data = 'video.mp4', format = 'mp4', end_time = 7, width = 256, loop = False, autoplay = False)

# ********************************************** Remove Deploy and three dots present on top right side **********************************************

# Hide the Streamlit style elements
hide_streamlit_style = """
    <style>
    /* Hide deploy button, menu (hamburger) and footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

