# Fetching data from a single video

### Importing Packages

import pandas as pd
import numpy as np
import requests

import re
import string
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk import download
import os


video_id = 'SGqg_ZzThDU'
# video_id

### Defining .env and API Key
def single_video_process(video_id):
    API_KEY = os.environ.get('API_KEY')

    ### Cleaning Dataset

    download('words')

    def clean_and_filter(df):
        def remove_newline(text):
            text = text.replace('\n', '')
            return text

        def remove_punctuation(text):
            for punctuation in string.punctuation:
                text = text.replace(punctuation, '')
            return text

        def lowercase (text):
            lowercased = text.lower()
            return lowercased

        df['comment_clean'] = df.comment.apply(remove_newline)
        df['comment_clean'] = df.comment_clean.apply(remove_punctuation)
        df['comment_clean'] = df.comment_clean.apply(lowercase)

        english_words = set(words.words())
        def is_english(text):
            words_in_comment = word_tokenize(text)
            num_words_in_comment = len(words_in_comment)
            num_english_words_in_comment = 0
            for word in words_in_comment:
                if word in english_words:
                    num_english_words_in_comment += 1
            english = False
            if num_words_in_comment > 0:
                if num_english_words_in_comment/num_words_in_comment >= 0.3:
                    english = True
                return english
            else:
                return False

        def english_only(df):
            df['english'] = df['comment_clean'].apply(is_english)
            return df

        df = english_only(df)

        def remove_non_english_symbols(text):
            english_pattern = re.compile(r'[^a-zA-Z0-9\s\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]')
            cleaned_text = re.sub(english_pattern, '', text)
            return cleaned_text


        df['comment_clean'] = df.comment_clean.apply(remove_non_english_symbols)

        return df[df["english"] == True]

    ### Genre Dictionary

    genre_dict = {
        "1":"Film & Animation",
        "2":"Autos & Vehicles",
        "10":"Music",
        "15":"Pets & Animals",
        "17":"Sports",
        "18":"Short Movies",
        "19":"Travel & Events",
        "20":"Gaming",
        "21":"Videoblogging",
        "22":"People & Blogs",
        "23":"Comedy",
        "24":"Entertainment",
        "25":"News & Politics",
        "26":"Howto & Style",
        "27":"Education",
        "28":"Science & Technology",
        "29":"Nonprofits & Activism",
        "30":"Movies",
        "31":"Anime/Animation",
        "32":"Action/Adventure",
        "33":"Classics",
        "34":"Comedy",
        "35":"Documentary",
        "36":"Drama",
        "37":"Family",
        "38":"Foreign",
        "39":"Horror",
        "40":"Sci-Fi/Fantasy",
        "41":"Thriller",
        "42":"Shorts",
        "43":"Shows",
        "44":"Trailers"
    }

    ### Fetching Relevant Comments Function

    def fetch_comments_relevance(video_id, api_key):
        url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100&order=relevance"
        comments = []
        nextPageToken = None
        iter_number = 0
        token_count = 0
        while len(comments) < 200:
            print(f"Tokens used: {token_count}")

            if nextPageToken:
                url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100&order=relevance"
                url += f"&pageToken={nextPageToken}"

            response = requests.get(url)
            token_count += 1
            try:
                data = response.json()
            except ValueError:
                print(f"{url} failed!")


            error = data.get("error", False)
            if error:
                return [""]

            for item in data.get("items", []):
                if item:
                    comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                    author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                    likecount = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                    date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                    replies = item["snippet"]["totalReplyCount"]
                    dict_ = {"comment": comment, "author": author, "likecount": likecount, "date": date, "replies": replies}

                    if comment is not None and pd.to_datetime(date).year <= 2024:
                        cleaned_comment = clean_and_filter(pd.DataFrame([comment],columns=["comment"]))
                        if not cleaned_comment.empty:
                            if cleaned_comment["english"][0] == True:
                                dict_["comment_clean"] = cleaned_comment["comment_clean"]
                                comments.append(dict_)
            nextPageToken = data.get("nextPageToken", None)
            if not nextPageToken or iter_number >= 100:
                break
            if iter_number == 0:
                if len(comments) < 5:
                    break
            iter_number += 1

        return comments

    ### Fetching Stats Function

    def fetch_stats(video_id, api_key):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=statistics&id={video_id}&key={api_key}"

        response = requests.get(url)
    #     print(response.status_code)
        try:
            data = response.json()
        except ValueError:
            print(f"{url} failed!")
        error = data.get("error",False)
        if not error:
            data = data.get("items",False)
            if data:
                views = data[0]["statistics"]["viewCount"]
                likes = data[0]["statistics"]["likeCount"]
                comments = data[0]["statistics"].get("commentCount",0)
                dict_ = {"views":[views], "likes":[likes], "comments":[comments]}
                return dict_
            return {}
        else:
            return {}

    ### Fetching Details Function

    def fetch_details(video_id, api_key):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"

        response = requests.get(url)
    #     print(response.status_code)
        try:
            data = response.json()
        except ValueError:
            print(f"{url} failed!")
        error = data.get("error",False)
        if not error:
            data = data.get("items",False)
            if data:
                date = data[0]["snippet"]["publishedAt"]
                channel_id = data[0]["snippet"]["channelId"]
                title = data[0]["snippet"]["title"]
                description = data[0]["snippet"]["description"]
                thumbnail = data[0]["snippet"]["thumbnails"]["maxres"]["url"]
                channel_title = data[0]["snippet"]["channelTitle"]
                tags = data[0]["snippet"].get("tags",[""])
                genre = genre_dict[data[0]["snippet"]["categoryId"]]
                language = data[0]["snippet"].get("defaultAudioLanguage","")
                dict_ = {"date":date, "channel_id":channel_id, "title":title, "description":description, "thumbnail":thumbnail,"channel_title":channel_title, "tags":[tags], "genre":genre, "language":language}
                return dict_
            return {}
        else:
            return {}

    ### Fetch Channel Details

    def fetch_channel(channel_id, api_key):
        url = f"https://www.googleapis.com/youtube/v3/channels?part=statistics&id={channel_id}&key={api_key}"

        response = requests.get(url)
    #     print(response.status_code)
        try:
            data = response.json()
        except ValueError:
            print(f"{url} failed!")
        error = data.get("error",False)
        if not error:
            data = data.get("items",False)
            if data:
                view_count = data[0]['statistics']['viewCount']
                subscriber_count = data[0]['statistics']['subscriberCount']
                video_count = data[0]['statistics']['videoCount']
                dict_ = {"viewCount":view_count, "subscriberCount":subscriber_count, "videoCount":video_count}
                return dict_
            return {}
        else:
            return {}

    ### Fetching and Storing in CSV

    def fetch_all_info(video_id, api_key):
        details = pd.DataFrame(fetch_details(video_id, api_key))
        comments_relevance = pd.DataFrame(fetch_comments_relevance(video_id, api_key))
        stats = pd.DataFrame(fetch_stats(video_id, api_key))
        channel = pd.DataFrame([fetch_channel(details['channel_id'][0], api_key)])
        info_all = pd.concat([stats,details],axis=1)
        comments_relevance["video_id"] = video_id
        info_all["video_id"] = video_id
        return comments_relevance, info_all, channel

    print(video_id)
    result = fetch_all_info(video_id, API_KEY)
    if result:
        comment, info, channel = result

    ### Adding Channel details to Info DataFrame

    info['Total_Views'] = channel['viewCount']
    info['Sub_Count'] = channel['subscriberCount']
    info['Video_Count'] = channel['videoCount']

    ### The big info DataFrame
    return info, comment
