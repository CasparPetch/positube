import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import os
from utils import add_logo


# from PIL import Image
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# my function import
from single_video_scripts.channel_search import grab_channel
from scripts.roberta_demo_day import roberta_channel
from scripts.formatting import millify

st.session_state['API_KEY'] = os.getenv('API_KEY')
# for key in st.session_state.keys():
#     st.session_state[key] = None

st.set_page_config(page_title="Channel Dashboard", page_icon="📈")

add_logo()


st.markdown("# Channel Dashboard")
st.sidebar.header("Channel Dashboard")
st.write("""#### Discover how controversial your favourite channel is! """)
st.write("""##### Enter their username or channel id below to run sentiment analysis on a sample of comments from their Top 10 Most Viewed videos""")

st.text("")
st.text("")

# Enter channel ID

channel_name = st.text_input("Enter Channel Username or ID")

if st.button("Tube me"):
    if channel_name is not None:
        # st.write(f'searching for channel_id of {channel_name}')
        st.session_state['channel_name'] = channel_name
    else:
        st.write('Pick a channel dummy!')

    prepared = ['pewdiepie', 'benshapiro']
    if channel_name.lower() in prepared:
        st.session_state['channel_name'] = channel_name
        st.session_state['channel_df'] = pd.read_csv(f'streamlit/data/{channel_name}_channel_df.csv', index_col=0)
        st.session_state['channel_stats'] = pd.read_csv(f'streamlit/data/{channel_name}_channel_stats.csv', index_col=0)

    elif 'channel_name' in st.session_state.keys():
        channel_df, channel_info, channel_stats = grab_channel(st.session_state['channel_name'])
        st.session_state['channel_df'] = channel_df
        st.session_state['channel_info'] = channel_info
        st.session_state['channel_stats'] = channel_stats
        st.session_state['channel_id'] = st.session_state['channel_stats']['channel_id'].values[0]

    # Line breaks
    st.text("")

    if 'channel_stats' in st.session_state.keys():

        # Basic Statistics
        view_count = st.session_state['channel_stats']['Total_Views'].values[0]
        subscriber_count = st.session_state['channel_stats']['Sub_Count'].values[0]
        video_count = st.session_state['channel_stats']['Video_Count'].values[0]

        # st.caption(f"{st.session_state['channel_name']} has {millify(view_count)} views")
        # st.caption(f"{st.session_state['channel_name']} has {millify(subscriber_count)} subscribers")
        # st.caption(f"{st.session_state['channel_name']} has {millify(video_count)} videos")
        # st.write('## Channel Statistics')
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label='Total Channel Views', value = millify(view_count))
        with col2:
            st.metric(label='Total Channel Subscribers', value = millify(subscriber_count))
        with col3:
            st.metric(label='Total Videos on Channel', value = millify(video_count))

        if st.session_state['channel_name'].lower() in prepared:
            st.session_state['sentiment_df'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_results.csv", index_col=0)
            st.session_state['pos_score_df'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_IDs_df.csv", index_col=0)
        else:
            sentiment_results, pos_score = roberta_channel(st.session_state['channel_df'])
            st.session_state['sentiment_df'] = sentiment_results
            st.session_state['pos_score_df'] = pos_score

        if 'sentiment_df' in st.session_state.keys():
            sentiment_description = f"Mostly {st.session_state['sentiment_df']['Sentiment'].value_counts().index[0]}"
            st.write(f"#### Sentiment amongst viewers of {st.session_state['channel_name']} is {sentiment_description}")
            # st.caption('[based on their Top 10 Most Viewed videos]')

        # st.write(st.session_state['sentiment_df'])
        # Charts and Bars
        # 1
        chart1_prep = st.session_state['sentiment_df']
        # chart1_data.drop(columns=['Comment'], inplace=True)
        chart1_data = chart1_prep.groupby('video_id')[['Negative (%)', 'Neutral (%)', 'Positive (%)']].mean(numeric_only=True)
        chart1_data.index = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        # st.write(chart1_data)
        st.bar_chart(chart1_data)


        # 2
        # arr = np.random.normal(1, 1, size=100)
        # fig, ax = plt.subplots()
        # ax.hist(arr, bins=20)

        # st.pyplot(fig)

        # 3
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=['a', 'b', 'c'])

        st.area_chart(chart1_data)
