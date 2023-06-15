import streamlit as st
st.set_page_config(page_title="DataFrame Demo", page_icon="📊")
import time
import numpy as np
import pandas as pd
import os
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
from scripts.channel_search import grab_channel
from scripts.roberta_demo_day import roberta
from utils import add_logo

# comment

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in df.columns:
        if is_object_dtype(df[col]):
            try:
                df[col] = pd.to_datetime(df[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.tz_localize(None)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df


def get_useful_stats(df):

    channels = list(df.value_counts("channel_id").keys())

    new_df = pd.DataFrame({"channel_id":[], "positive":[], "neutral":[], "negative":[], "positivity":[], "controversy":[]})
    for channel in channels:
        new_df = pd.concat([pd.DataFrame({"channel_id":channel,
            "positive":[df[df["channel_id"] == channel]["Positive (%)"].mean()],
            "neutral":[df[df["channel_id"] == channel]["Neutral (%)"].mean()],
            "negative":[df[df["channel_id"] == channel]["Negative (%)"].mean()],
            "positivity":[df[df["channel_id"] == channel]["Scaler_value"].mean()],
            "controversy":[df[df["channel_id"] == channel]["Positive (%)"].mean() * df[df["channel_id"] == channel]["Negative (%)"].mean() / 100]
            }), new_df])
    return new_df.reset_index(drop=True)



positube_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


add_logo()




st.markdown("# Top 1000 popular channels")
st.sidebar.header("Top 1000")
st.write(
    """This page allows you to browse the top 1000 most popular channels and compare the stats to a channel of your choice"""
)

df = pd.read_csv(os.path.join(positube_path, 'raw_data', 'final_channel_data.csv'))



filepath = os.path.join(os.path.abspath("."),"streamlit","data","top_1000.csv")
top_1000 = pd.read_csv(filepath)

channel_id = st.text_input("Enter Channel ID")
print(f"Channel ID is {channel_id}")
if channel_id == "":
    top_1000_stats = get_useful_stats(top_1000)
    # filter_dataframe(top_1000_stats)
    sub_stats = pd.read_csv(os.path.join(os.path.abspath("."),"streamlit","data","topSubscribed.csv"))
    sub_stats["channel_id"] = sub_stats["Youtube Channel"]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Average Negative", value=f'{np.round(top_1000["Negative (%)"].mean(),2)}%',)
    with col2:
        st.metric(label="Average Neutral", value=f'{np.round(top_1000["Neutral (%)"].mean(),2)}%',)
    with col3:
        st.metric(label="Average Positive", value=f'{np.round(top_1000["Positive (%)"].mean(),2)}%',)
    st.metric(label="Overall Positivity", value=f'{np.round(top_1000["Scaler_value"].mean(),2)*100}%')
    st.dataframe(pd.merge(left=top_1000_stats,right=sub_stats.drop("Youtube Channel",axis=1),how="left",on="channel_id"))





elif channel_id == "MrBeast":
    comments = pd.read_csv(os.path.join(positube_path, 'streamlit', 'data', 'mrbeast_comments.csv'))
    infos = pd.read_csv(os.path.join(positube_path, 'streamlit', 'data', 'mrbeast_infos.csv'))
    IDs = pd.read_csv(os.path.join(positube_path, 'streamlit', 'data', 'mrbeast_videos.csv'))
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Average Negative", value=f'{np.round(comments["Negative (%)"].mean(),2)}%', delta=f'{np.round(comments["Negative (%)"].mean() - top_1000["Negative (%)"].mean(),1)}%', delta_color="inverse")
    with col2:
        st.metric(label="Average Neutral", value=f'{np.round(comments["Neutral (%)"].mean(),2)}%', delta=f'{np.round(comments["Neutral (%)"].mean() - top_1000["Neutral (%)"].mean(),1)}%', delta_color="off")
    with col3:
        st.metric(label="Average Positive", value=f'{np.round(comments["Positive (%)"].mean(),2)}%', delta=f'{np.round(comments["Positive (%)"].mean() - top_1000["Positive (%)"].mean(),1)}%', delta_color="normal")
    # st.metric(label="Overall Positivity", value=f'{np.round(comments["Scaler_value"].mean(),2)*100}%', delta=f'{np.round(comments["Scaler_value"].mean() - top_1000["Scaler_value"].mean(),1)*100}%', delta_color="normal")

    top_1000_stats = get_useful_stats(top_1000)
    sub_stats = pd.read_csv(os.path.join(os.path.abspath("."),"streamlit","data","topSubscribed.csv"))
    sub_stats["channel_id"] = sub_stats["Youtube Channel"]



    ratings_df = pd.concat([pd.DataFrame({"channel_id": [channel_id], "positivity": [comments["Scaler_value"].mean()]}), top_1000_stats[["channel_id", "positivity"]]]).sort_values("positivity", ascending=False).reset_index(drop=True)
    ratings_df["positivity"] = ratings_df["positivity"] * 100

    place = ratings_df[ratings_df["channel_id"] == channel_id].index[0]
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="Positivity score",
        value=f'{np.round(ratings_df.iloc[place]["positivity"], 2)}%',
        delta=f'{np.round(comments["Scaler_value"].mean() - top_1000["Scaler_value"].mean(), 1) * 100}',
        delta_color="normal")


    st.balloons()
    # st.markdown(f"# Positivity score: {np.round(comments['Scaler_value'].mean(),2)*100}%")
    if np.round(comments["Scaler_value"].mean() - top_1000["Scaler_value"].mean(),1)*100 > 0:
        col4, col5 = st.columns(2)
        with col5:
            st.metric(
                label="Less positive",
                value=f'### You are {np.round((comments["Scaler_value"].mean() - top_1000["Scaler_value"].mean()),1)*100}% more positive than average!',
                delta=np.round(comments["Scaler_value"].mean() - top_1000["Scaler_value"].mean(),1)*100
            )
    else:
        col4, col5, col6 = st.columns(3)
        with col5:
            st.markdown(f'### You are {-1*(np.round(comments["Scaler_value"].mean() - top_1000["Scaler_value"].mean(),1)*100)}% less positive than average!')
    # st.write(place)
    st.markdown(f"### The most positive channel is {ratings_df.iloc[0]['channel_id']} at {np.round(ratings_df.iloc[0]['positivity'],2)}%")
    st.markdown(f"### You are slightly less positive than {ratings_df.iloc[place-1]['channel_id']} at {np.round(ratings_df.iloc[place-1]['positivity'],2)}%")
    st.markdown(f"### But slightly more positive than {ratings_df.iloc[place+1]['channel_id']} at {np.round(ratings_df.iloc[place+1]['positivity'],2)}%!")
    st.markdown(f"### And the most negative channel is {ratings_df.iloc[-1]['channel_id']} at {np.round(ratings_df.iloc[-1]['positivity'],2)}%")
    st.markdown("")
    st.dataframe(ratings_df)
    st.dataframe(pd.merge(left=top_1000_stats,right=sub_stats.drop("Youtube Channel",axis=1),how="left",on="channel_id"))

    st.dataframe(comments)

    st.dataframe(pd.merge(left=infos, right=IDs, how="outer", on="video_id"))
else:
    print("Grabbing channel...")
    comments, infos = grab_channel(channel_id)

    print("Processing comments...")
    print("comments")
    comments, IDs = roberta(comments)
    print("Done")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="Average Negative", value=f'{np.round(comments["Negative (%)"].mean(),2)}%', delta=np.round(comments["Negative (%)"].mean() - top_1000["Negative (%)"].mean(),2), delta_color="inverse")
    with col2:
        st.metric(label="Average Neutral", value=f'{np.round(comments["Neutral (%)"].mean(),2)}%', delta=np.round(comments["Neutral (%)"].mean() - top_1000["Neutral (%)"].mean(),2), delta_color="off")
    with col3:
        st.metric(label="Average Positive", value=f'{np.round(comments["Positive (%)"].mean(),2)}%', delta=np.round(comments["Positive (%)"].mean() - top_1000["Positive (%)"].mean(),2), delta_color="normal")
    st.dataframe(comments)
