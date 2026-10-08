import streamlit as st

'''
clicked = st.button("Click me")
st.write(f"button() returned: {clicked}")
'''

'''
button_1 = st.button("Button 1")
button_2 = st.button('Button_2')

st.write(f"Clicked_Button_1 {button_1}")
st.write(f"Clicked_Button_2 {button_2}")
'''

#----------------------------------------------------------------------------

'''
# 1️⃣ Initialize (runs only once per session)
if "count" not in st.session_state:
    st.session_state.count = 0

# 2️⃣ Event
if st.button("Click"):
    st.session_state.count += 1

# 3️⃣ Display
st.write("Count:", st.session_state.count)

'''

# st.text_input("Name")

'''
name = st.text_input("Enter name")
st.write(name)
'''

'''
st.text_input("Enter name", key="username")
st.write(st.session_state.username)
'''

'''
st.session_state.name = "Guest"
st.text_input("Your name", key="name")
st.write(st.session_state.name)
'''
'''
name = st.text_input("Enter name")
st.write(name)
'''

'''
with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    submitted = st.form_submit_button("Submit Form")

if submitted:
    st.write("Name:", name)
    st.write("Age:", age)
'''

'''
x = 0
if st.button("Click"):
    x = 10
st.write(x)
'''

'''
x = 0

if st.button("Click"):
    x = 10

st.button("Another button")  # 👈 causes rerun

st.write(x)
'''

# ==================== Session State ====================
'''
page = 1

if page == 1:
    name = st.text_input("Enter your name")
    if st.button("Next"):
        page = 2

if page == 2:
    st.write("Welcome", name)
'''

"""
page = 1

if page == 1:
    name = st.text_input("Enter your name")
    if st.button("Next"):
        page = 2

st.button("Anything")   # 👈 new interaction

if page == 2:
    st.write("Welcome", name)

"""

'''
if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Increase"):
    st.session_state.count += 1

st.button("Other button.")

st.write("Count:", st.session_state.count)
'''

'''
if "page" not in st.session_state:
    st.session_state.page = 1

if st.session_state.page == 1:
    st.text_input("Enter your name", key="name")
    if st.button("Next"):
        st.session_state.page = 2
        
if st.session_state.page == 2:
    st.write("Welcome", st.session_state.name)
    if st.button("Back"):
        st.session_state.page = 1
        st.rerun()
'''

'''
# Initialize session_state keys
if "page" not in st.session_state:
    st.session_state.page = 1
if "name" not in st.session_state:
    st.session_state.name = ""  # initialize with empty string

# Page 1
if st.session_state.page == 1:
    st.text_input("Enter your name", key="name")
    if st.button("Next"):
        st.session_state.page = 2
        st.rerun()  # force immediate rerun to show Page 2

# Page 2
if st.session_state.page == 2:
    st.write("Welcome", st.session_state.name)
    if st.button("Back"):
        st.session_state.page = 1
        st.rerun()  # force immediate rerun to show Page 1
'''

# Initialize session_state keys
if "page" not in st.session_state:
    st.session_state.page = 1
if "name" not in st.session_state:
    st.session_state.name = ""  # initialize with empty string

# Page 1
if st.session_state.page == 1:
    st.text_input("Enter your name", key="name")
    if st.button("Next"):
        if st.session_state.name.strip() != "":  # check user typed something
            st.session_state.page = 2
            st.rerun()
        else:
            st.warning("Please enter your name before proceeding!")


# Page 2
if st.session_state.page == 2:
    st.write("Welcome", st.session_state.name)
    if st.button("Back"):
        st.session_state.page = 1
        st.rerun()  # force immediate rerun to show Page 1
