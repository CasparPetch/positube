import streamlit as st
import os

def add_logo():
    image_filename = "positube_logo.png"
    current_directory = os.getcwd()
    mask_image = os.path.join(current_directory, 'streamlit', image_filename)
    st.sidebar.image(mask_image, use_column_width=False, width=300)

