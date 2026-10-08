import streamlit as st

st.title(body = 'This is Streamlit title.')
st.header(body = 'This is Streamlit Header.')
st.subheader("This is Streamlit Sub header.")
st.text("This is Streamlit text.")

# **************************************************
st.markdown("***Nikunj*** Bosamiya")
# **...** is to bold text
# *...* is for italic
# "# ..." For giving Jupyter like markdown style
# ***...*** is for bold and italic both
# There're various other syntax available for different styles. We can search on google


st.markdown("---")    # This draws the horizontal line
st.markdown("[Google](http://www.google.com)")    # Creates a clickable text "Google" which redirects to google.com

# ****************************************************

json = {"Nikunj": 26, "Jugal": 16}
st.json(json)

code = '''
def factorial(n):
    fact = 1
    for i in range(1, n+1):
        fact = fact*i
    s
    return fact
'''

st.code(code, language = 'python')

st.write(''' *Write function allows us to use any pattern which we can give to **code()**, **markdown()**, **json()**, **latex()** etc
We can go through the documentations and learn it.*
''')