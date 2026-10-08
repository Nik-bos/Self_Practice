import streamlit as st

st.title("Session state in Streamlit")

# This is just to create a partition
st.markdown("""
<hr style="
  height: 5px;
  border: none;
  background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
">
""", unsafe_allow_html=True)


# ********************************************* Without Session State *********************************************

st.header("Without Session State")


count = 1

if st.button('Increment', key = '1'):
    count +=1

st.write(count)

st.write('''
* Run the app, counter = 1, button = False.
* Click button, button becomes True and script reruns.
* Counter = 1, now button = True (On every further clicks), counter = 2
* Click again, script reruns, counter = 1, button already True, counter = 2

This same process will happen on every click''')

# This is just to create a partition
st.markdown("""
<hr style="
  height: 5px;
  border: none;
  background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
">
""", unsafe_allow_html=True)



# ********************************************* With Session State *********************************************

st.header("With Session State")

if "counter" not in st.session_state:
    st.session_state.counter = 0

if st.button("Increment", key = '2'):
    st.session_state.counter += 1

st.write(st.session_state.counter)

st.write('''
* First load → Counter = 0
* First click → Script Reruns → Button = True → Counter = 1
* Second click → Script Reruns → Button = True → Counter = 2
* Third click → Script Reruns → Button = True → Counter = 3
* ✅ It remembers the value across reruns.''')

# This is just to create a partition
st.markdown("""
<hr style="
  height: 5px;
  border: none;
  background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
">
""", unsafe_allow_html=True)

# ********************************************* Toggling between values *********************************************

import streamlit as st

if "name" not in st.session_state:
    st.session_state.name = "Nikunj"

if st.button("***Change Name***"):
    if st.session_state.name == "Nikunj":
        st.session_state.name = "Jugal"
    else:
        st.session_state.name = "Nikunj"

st.write(f"**Current Name**: {st.session_state.name}")

st.write('''
* Load → Nikunj
* 1st click → Script Reruns → Button = True → Jugal
* 2nd click → Script Reruns → Button = True → Nikunj
* Keeps toggling.''')
