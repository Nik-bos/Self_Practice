import streamlit as st

st.title(body = 'File Uploader in Streamlit.')
# This is just to create a partition
st.markdown("""
<hr style="
  height: 5px;
  border: none;
  background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
">
""", unsafe_allow_html=True)

# ********************************************* file_uploader() *********************************************

# This just uploads the file. We have to code for displaying it. we can uploade any file, pdf, image, video, audio etc
files = st.file_uploader(label = '**This is File Uploader**',
                        type = ['png', 'jpg', 'jpeg'],
                        accept_multiple_files = True, 
                        width = 550)

if files:
    for file in files:
        st.image(image = file, width = 256)

# If not used for loop and directly passed image = files, images will be displayd in horizontal format
# We can avoid foor loop because st.image() accepts list as well