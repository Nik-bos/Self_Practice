import streamlit as st
import datetime

st.title('Advance Widgets in Streamlit')

# This is just to create a partition
st.markdown("""
<hr style="
  height: 5px;
  border: none;
  background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
">
""", unsafe_allow_html=True)


# ********************************************* slider() *********************************************
value = st.slider(label = '**This is a Slider**', min_value = 0, max_value = 100, step = 2)

if value:
    st.write(value)

# ********************************************* text_input() *********************************************
text_input = st.text_input(label = "**This is text input**", max_chars = 250)

if text_input:
    st.write(text_input)    # Press enter to apply

# ********************************************* text_input() *********************************************
text_area = st.text_area(label = "**This is text area**", max_chars = 250)

if text_area:
    st.write(text_area)    # Press cntrl + enter to apply and enter to line_break

# ********************************************* chat_input() *********************************************

chat = st.chat_input("Type here...")
if chat:
    st.write(chat)

# ********************************************* date_input() *********************************************
date_input = st.date_input(label = '**This is date input**', min_value = None)

if date_input:
    st.write(date_input)

# ********************************************* time_input() *********************************************
time_input = st.time_input(label = 'This is time input', value = datetime.time())    # try value = None

if time_input:
    st.write(f'**{time_input}**')
