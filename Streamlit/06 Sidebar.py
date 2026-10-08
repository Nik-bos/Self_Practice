import streamlit as st

st.title("Sidebar in Streamlit")

# This is just to create a partition
st.markdown("""
<hr style="
  height: 5px;
  border: none;
  background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
">
""", unsafe_allow_html=True)


# ********************************************* sidebar() *********************************************
st.sidebar.title("**This is a Sidebar**")
