import streamlit as st

# ********************************************* checkbox() *********************************************

# st.checkbox(label = 'Checkbox_1', value = True)   # value = True for checked and False for not checked

state = st.checkbox(label = 'Checkbox_1', value = True)   # value = True for checked and False for not checked

if state:
    st.write("Checked")
else:
    st.write('Not checked')

# ********************************************* radio() *********************************************


radio = st.radio(label = 'This is radio', options = ['Jetpur', "Virpur", 'Gondal', 'Rajkot', 'Junagadh'])
if radio:
    st.write(f"{radio} selected")

# 'radio' variable is a string and it holds the selected city

def name():
    st.write("Nikunj")

# ********************************************* button() *********************************************
button = st.button(label = 'This is button', on_click = name)
# on_click in radio() and button() executes the function and shows results on terminal. Can avoid.
if button:
    st.write("Button clicked")

# ********************************************* selectbox() *********************************************
button = st.selectbox(label = 'This is selectbox', options = ['Box_1', 'Box_2', 'Box_3', 'Box_4'])
if button:
    st.write(f'Selected {button}')

# ********************************************* multiselect() *********************************************
multi_select = st.multiselect(label = "***This is multiselect***", options = ['Box_1', 'Box_2', 'Box_3', 'Box_4'])
st.write(multi_select)

for select in multi_select:
    st.write(select)

