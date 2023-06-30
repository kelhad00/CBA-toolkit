import streamlit as st
from PIL import Image
import os

def affichage():
    image_path = os.path.join('images', 'ISIA_Lab.jpg')
    img = Image.open(image_path)
    st.set_page_config(page_title="SNL Analysis", page_icon=img, layout='centered')
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #D60D49;
        }
    </style>
    """, unsafe_allow_html=True)
