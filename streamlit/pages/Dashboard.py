import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from utils import add_logo


add_logo()
# from PIL import Image
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# my function import
from single_video_scripts.channel_search import grab_channel

for key in st.session_state.keys():
    st.session_state[key] = None

st.set_page_config(page_title="Channel Dashboard", page_icon="📈")

st.markdown("# Channel Dashboard")
st.sidebar.header("Channel Dashboard")
st.write(
    """We're still generating a bunch of random numbers because the dataframe
    is a huge headache """
)

st.text("")
st.text("")

# Enter channel ID

channel_name = st.text_input("Enter Channel ID")
# comments_df = grab_channel(channel_id)
if st.button("Tube me"):
    if channel_name is not None:
        # st.write('YOU PRESSED A BUTTON')
        st.write(f'searching for channel_id of {channel_name}')
        st.session_state['channel_name'] = channel_name
    else:
        st.write('Pick a channel dummy!')


    if 'channel_name' in st.session_state.keys():
        channel_df, channel_info, channel_stats = grab_channel(st.session_state['channel_name'])
        st.session_state['channel_df'] = channel_df
        st.session_state['channel_info'] = channel_info
        st.session_state['channel_stats'] = channel_stats

    # Line breaks

    st.text("")
    st.text("")

    # if 'channel_df' in st.session_state.keys():
    #     st.write(st.session_state['channel_df'])

    # if 'channel_info' in st.session_state.keys():
    #     st.write(st.session_state['channel_info'])
    #     st.write(type(st.session_state['channel_info']))

    if 'channel_stats' in st.session_state.keys():
    #     st.write(st.session_state['channel_stats'])
    #     st.write(type(st.session_state['channel_stats']))

        # Basic Statistics
        view_count = st.session_state['channel_stats']['Total_Views'].values[0]
        subscriber_count = st.session_state['channel_stats']['Sub_Count'].values[0]
        video_count = st.session_state['channel_stats']['Video_Count'].values[0]
        sentiment_description = 'WE NEED TO ADD THIS'

        st.caption(f"Pewdiepie has {view_count} views")
        st.caption(f'Pewdiepie has {subscriber_count} subscribers')
        st.caption(f'Pewdiepie has {video_count} videos')
        st.caption(f'Pewdiepie is {sentiment_description} amongst viewers')

        # Charts and Bars
        # 1
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=["Video", "Views", "ID"])

        st.bar_chart(chart_data)

        # 2
        arr = np.random.normal(1, 1, size=100)
        fig, ax = plt.subplots()
        ax.hist(arr, bins=20)

        st.pyplot(fig)

        # 3
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        st.area_chart(chart_data)
