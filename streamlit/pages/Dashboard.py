import pandas as pd
import plotly.express as px
import streamlit as st
st.set_page_config(page_title="Channel Dashboard", page_icon="📈")
# import os
from utils import add_logo


# from PIL import Image
# from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# my function import
# from single_video_scripts.channel_search import grab_channel
from scripts.dashboard_helper import *
# from scripts.roberta_demo_day import roberta_channel
from scripts.formatting import millify

# st.session_state['API_KEY'] = os.getenv('API_KEY')
# for key in st.session_state.keys():
#     st.session_state[key] = None



add_logo()


st.markdown("# Channel Dashboard")
st.sidebar.header("Channel Dashboard")
st.write("""#### Discover how controversial your favourite channel is! """)
st.write("""##### Enter their username or channel id below to run sentiment analysis on a sample of comments from their Top 10 Most Viewed videos""")

st.text("")

# Enter channel ID

channel_name = st.text_input("Enter Channel Username or ID")

if channel_name not in st.session_state.keys():

    if st.button("Tube me"):
        if channel_name is not None:
            # st.write(f'searching for channel_id of {channel_name}')
            st.session_state['channel_name'] = channel_name
        else:
            st.write('Pick a channel dummy!')

        prepared = ['PewDiePie', 'BenShapiro']
        if channel_name in prepared:
            st.session_state['channel_name'] = channel_name
            st.session_state['channel_df'] = pd.read_csv(f'streamlit/data/{channel_name}_channel_df.csv', index_col=0)
            st.session_state['channel_stats'] = pd.read_csv(f'streamlit/data/{channel_name}_channel_stats.csv', index_col=0)

        # elif 'channel_name' in st.session_state.keys():
        #     channel_df, channel_info, channel_stats = grab_channel(st.session_state['channel_name'])
        #     st.session_state['channel_df'] = channel_df
        #     st.session_state['channel_info'] = channel_info
        #     st.session_state['channel_stats'] = channel_stats
        #     st.session_state['channel_id'] = st.session_state['channel_stats']['channel_id'].values[0]

        # Line breaks
        st.text("")

        if 'channel_stats' in st.session_state.keys():

            # Basic Statistics
            view_count = st.session_state['channel_stats']['Total_Views'].values[0]
            subscriber_count = st.session_state['channel_stats']['Sub_Count'].values[0]
            video_count = st.session_state['channel_stats']['Video_Count'].values[0]

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(label='Total Channel Views', value = millify(view_count))
            with col2:
                st.metric(label='Total Channel Subscribers', value = millify(subscriber_count))
            with col3:
                st.metric(label='Total Videos on Channel', value = millify(video_count))

            if st.session_state['channel_name'] in prepared:
                st.session_state['sentiment_df'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_results.csv", index_col=0)
                st.session_state['pos_score_df'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_IDs_df.csv", index_col=0)
                st.session_state['channel_stats'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_channel_stats.csv", index_col=0)
                st.session_state['channel_info'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_channel_info.csv", index_col=0)
                st.session_state['channel_df'] = pd.read_csv(f"streamlit/data/{st.session_state['channel_name']}_channel_df.csv", index_col=0)
            # else:
            #     # sentiment_results, pos_score = roberta_channel(st.session_state['channel_df'])
            #     st.session_state['sentiment_df'] = None #sentiment_results
            #     st.session_state['pos_score_df'] = None #pos_score
            #     st.session_state['channel_stats'] = None
            #     st.session_state['channel_info'] = None
            #     st.session_state['channel_df'] = None

            if 'sentiment_df' in st.session_state.keys():
                sentiment_description = f"Mostly {st.session_state['sentiment_df']['Sentiment'].value_counts().index[0]}"
                st.write(f"#### Sentiment amongst viewers of {st.session_state['channel_name']} is {sentiment_description}")

                # Charts and Bars
                # 1
                chart1_prep = st.session_state['sentiment_df']
                chart1_data = chart1_prep.groupby('video_id')[['Negative (%)', 'Neutral (%)', 'Positive (%)']].mean(numeric_only=True)
                chart1_data.index = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']

                st.bar_chart(chart1_data)



                # st.session_state['pos_score_df'] = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_st.session_state['pos_score_df'].csv",index_col=0)
                # st.session_state['channel_info'] = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_channel_info.csv",index_col=0)
                # results = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_results.csv",index_col=0)
                # channel_df = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_channel_df.csv",index_col=0)
                # channel_stats = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_channel_stats.ccsv",index_col=0)



                st.session_state['comments_score'] = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/pages/comment_score.csv",index_col=0)



                video_stats = pd.merge(left=st.session_state['pos_score_df'],right=st.session_state['channel_info'],how="inner",on="video_id").sort_values("date")

                dislikes_pred = linear_model(video_stats[["positivity_score","views","likes","comments","genre"]])
                video_stats["pred_dislikes"] = dislikes_pred
                fig = px.bar(video_stats, x='title', y='pred_dislikes', title='Predicted dislikes on recent videos')
                st.plotly_chart(fig, use_container_width=True)


                fig = px.line(video_stats, x="date", y="views", title='Views over last 10 videos', text='title')
                fig.update_traces(textposition="bottom right")
                st.plotly_chart(fig, use_container_width=True)


                fig = px.line(video_stats, x="date", y="positivity_score", title='Positivity score over last 10 videos', text='title')
                fig.update_traces(textposition="bottom right")
                st.plotly_chart(fig, use_container_width=True)

                controversy = []
                cut_dfs = df_cutter(st.session_state['sentiment_df'])
                for df in cut_dfs:
                    controversy.append(df["Negative (%)"].mean() * df["Positive (%)"].mean())
                st.session_state['pos_score_df']["controversy"] = controversy


                fig = px.line(video_stats, x="date", y="positivity_score", title='Positivity score over last 10 videos', text='title')
                fig.update_traces(textposition="bottom right")
                st.plotly_chart(fig, use_container_width=True)



                video_stats = pd.merge(left=st.session_state['pos_score_df'],right=st.session_state['channel_info'],how="inner",on="video_id").sort_values("date")

                fig = px.line(video_stats, x="date", y="controversy", title='Controversy over last 10 videos', text='title')
                fig.update_traces(textposition="bottom right")
                st.plotly_chart(fig, use_container_width=True)
