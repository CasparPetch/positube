import streamlit as st

# Page Title
st.title("About PosiTube")

# Tools (left side)
st.sidebar.header("Tools")
st.sidebar.image("https://www.vectorlogo.zone/logos/python/python-ar21.svg")
st.sidebar.image("https://www.vectorlogo.zone/logos/tensorflow/tensorflow-ar21.svg")
st.sidebar.image("https://www.vectorlogo.zone/logos/numpy/numpy-ar21.svg")
st.sidebar.image("https://pandas.pydata.org/static/img/pandas_mark.svg")
st.sidebar.image("https://huggingface.co/landing/assets/hugging-face-logo.png", width=150)

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
st.markdown("Our initial hypothesis revolved around the possibility of accurately predicting the number of dislikes for a video using sentiment analysis on YouTube comments. However, after thorough analysis, we discovered that our hypothesis did not hold true. While sentiment analysis provides valuable insights, accurately predicting dislikes based solely on comments remains a challenge.")

# Conclusion and Future Improvements
st.header("Conclusion and Future Improvements")
st.markdown("Although our hypothesis was disproven, we continue to refine and enhance PosiTube, exploring new avenues to improve the accuracy of our predictions and provide valuable insights to content creators and viewers alike.")
