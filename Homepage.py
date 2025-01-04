import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from mplsoccer import Pitch, VerticalPitch

st.set_page_config(
    page_title="Multiple Apps",
    page_icon="🤜🤛",
)

st.title("Main Page")
st.sidebar.success("Select a page above.")
