import streamlit as st
from PIL import Image


def affichage():
    img=Image.open('images\ISIA_Lab.jpg')
    st.set_page_config(page_title="SNL Analysis", page_icon=img, layout='centered')
    st.markdown("""
    <style>
        [data-testid=stSidebar] {
            background-color: #D60D49;
        }
    </style>
    """, unsafe_allow_html=True)
