import pandas as pd
import streamlit as st
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import os
import random

st.set_page_config(
    page_title="Positube",
    page_icon="👋",
)

st.write("# Welcome to Positube! 👋")
st.sidebar.success("Select a demo below.")
