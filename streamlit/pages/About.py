import streamlit as st

import streamlit as st

# Set page config
st.set_page_config(
    page_title="PosiTube",
    page_icon=":movie_camera:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for YouTube-inspired theme
st.markdown(
    """
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        padding-top: 5rem;
    }
    .stApp footer {
        display: none;
    }
    .stTextInput > div:first-child {
        background-color: #fa0505;
    }
    .stButton button {
        background-color: #ff0000;
        color: white;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #c50a0a;
    }
    </style>
    """,
    unsafe_allow_html=True,
)












# Page Title
st.title("About PosiTube")

# Tools (left side)
st.sidebar.header("Tools")
st.sidebar.image("https://www.vectorlogo.zone/logos/python/python-ar21.svg")
st.sidebar.image("https://www.vectorlogo.zone/logos/tensorflow/tensorflow-ar21.svg")
st.sidebar.image("https://www.vectorlogo.zone/logos/numpy/numpy-ar21.svg")
st.sidebar.image("https://www.vectorlogo.zone/logos/google_bigquery/google_bigquery-ar21.svg")
st.sidebar.image("https://pandas.pydata.org/static/img/pandas_mark.svg")
st.sidebar.image("https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white")
st.sidebar.image("https://img.shields.io/badge/GIT-E44C30?style=for-the-badge&logo=git&logoColor=white")
st.sidebar.image("https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white")


# Main content (right side)
st.markdown("PosiTube is a unique application designed to predict the number of dislikes on YouTube videos through sentiment analysis of user comments. With the recent removal of the dislike feature on YouTube in late 2021, our app aims to fill the void by providing insights into the potential negativity surrounding a video.")

# Usage
st.header("Usage")
st.code("""
from positube import roberta

# Return a DataFrame with the positivity score of a video
roberta('PewDiePie')
""", language="python")

# Our Goal
st.header("Our Goal")
st.markdown("With the removal of the dislike option on YouTube, our team recognized the need for a solution to gauge the potential negative sentiment surrounding videos. Thus, we created PosiTube, an innovative app that utilizes sentiment analysis of comments to predict the number of dislikes a video might have.")

# Hypothesis
st.header("Hypothesis")
st.markdown("Our initial hypothesis revolved around accurately predicting the number of dislikes for a video using sentiment analysis on YouTube comments. While our prediction for dislikes didn't yield accurate results, we made significant discoveries in understanding the public sentiment towards videos.")

st.markdown("Through our analysis, we were able to identify videos that were universally liked by the general public as well as those that were more controversial. This insight has brought immense value, and we are delighted with the findings.")

st.markdown("Although our initial goal of predicting dislikes was not achieved, the valuable information we gained about the sentiment and public reception of videos has opened up new avenues for further research and exploration.")

# Conclusion and Future Improvements
st.header("Conclusion and Future Improvements")
st.markdown("Although we didn't fully achieve our initial goal of accurately predicting the number of dislikes for a video based on sentiment analysis of YouTube comments, our journey with PosiTube has been a success.")

st.markdown("PosiTube has provided valuable insights into the public sentiment and reception of videos, identifying universally liked content and more controversial topics. This information empowers content creators and enhances the YouTube viewing experience.")

st.markdown("We are excited about the positive impact PosiTube can have and look forward to future improvements and advancements that will benefit the YouTube platform.")
