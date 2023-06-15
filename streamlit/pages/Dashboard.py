import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
st.set_page_config(page_title="Channel Dashboard", page_icon="📈")
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












import plotly.express as px
import pandas as pd
import numpy as np



IDs_df = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_IDs_df.csv",index_col=0)
channel_info = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_channel_info.csv",index_col=0)
results = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_results.csv",index_col=0)
channel_df = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_channel_df.csv",index_col=0)
channel_stats = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/BenShapiro_channel_stats.csv",index_col=0)



comments_score = pd.read_csv("https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/pages/comment_score.csv",index_col=0)


def linear_model(df):
    import pandas as pd
    from sklearn.linear_model import LinearRegression
    import numpy as np

    data = pd.read_csv('https://raw.githubusercontent.com/CasparPetch/positube/master/streamlit/data/data_for_regression.csv', index_col=0)

    data["dislike_ratio"] = data["dislikes_2021"] / (data["likes_2021"] + data["dislikes_2021"])
    data = data[['dislike_ratio', 'positivity_score', 'views_2023', 'likes_2023', 'comments_2023', 'genre']]
    data.dropna(inplace=True)


    from sklearn.preprocessing import OneHotEncoder

    genre_ohe = OneHotEncoder(sparse=False, handle_unknown='ignore') # Instanciate One hot encoder

    genre_ohe.fit(data[['genre']]) # Fit one hot encoder

    data[genre_ohe.get_feature_names_out()] = genre_ohe.fit_transform(data[['genre']])

    data.drop(columns=['genre'], inplace = True) # Drop original column

    X = data.drop('dislike_ratio', axis= 1)

    y = data['dislike_ratio']


    from sklearn.preprocessing import MinMaxScaler

    minmax_scaler = MinMaxScaler()
    X_scaled = minmax_scaler.fit_transform(X)

    # Create and fit the linear regression model
    model = LinearRegression()
    model.fit(X_scaled, y)

    # Predict the dislikes for the test set
    df_scaled = df.copy()
    df_scaled.columns = ["positivity_score", "views_2023", "likes_2023", "comments_2023", "genre"]

    df_scaled[genre_ohe.get_feature_names_out()] = genre_ohe.transform(df[["genre"]])
    df_scaled.drop(columns=['genre'], inplace = True)
    df_scaled = minmax_scaler.transform(df_scaled)

    y_pred = model.predict(df_scaled)

    dislikes_pred = (df["likes"] * y_pred)/(1-y_pred)
    return dislikes_pred
video_stats = pd.merge(left=IDs_df,right=channel_info,how="inner",on="video_id").sort_values("date")

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

def df_cutter(df):
    IDs_list = df.value_counts('video_id').keys()
    cut_dfs = []
    for i, video in enumerate(IDs_list):
        cut_df = df[df['video_id'] == IDs_list[i]]
        cut_dfs.append(cut_df)
    return cut_dfs


controversy = []
cut_dfs = df_cutter(results)
for df in cut_dfs:
#     print(df["Negative (%)"].mean())
    controversy.append(df["Negative (%)"].mean() * df["Positive (%)"].mean())
IDs_df["controversy"] = controversy


fig = px.line(video_stats, x="date", y="positivity_score", title='Positivity score over last 10 videos', text='title')
fig.update_traces(textposition="bottom right")
st.plotly_chart(fig, use_container_width=True)



video_stats = pd.merge(left=IDs_df,right=channel_info,how="inner",on="video_id").sort_values("date")

fig = px.line(video_stats, x="date", y="controversy", title='Controversy over last 10 videos', text='title')
fig.update_traces(textposition="bottom right")
st.plotly_chart(fig, use_container_width=True)
