import pandas as pd
import requests
# streamlit import
# from single_video_scripts.cleaning_functions import clean_and_filter
# vs code import
from cleaning_functions import clean_and_filter

# temporary
from icecream import ic
ic.disable()

def fetch_comments_relevance(video_id, api_key):
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100&order=relevance"
    ic(url)
    comments = []
    nextPageToken = None
    iter_number = 0
    token_count = 0
    while len(comments) < 50:
        # print(f"Tokens used: {token_count}")

        if nextPageToken:
            url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&key={api_key}&maxResults=100&order=relevance"
            url += f"&pageToken={nextPageToken}"
        # print(url)
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
                date = item["snippet"]["topLevelComment"]["snippet"]["publishedAt"]
                if comment is not None and pd.to_datetime(date).year <= 2024:
                    cleaned_comment, is_english = clean_and_filter(comment)
                    if is_english == True:
                        author = item["snippet"]["topLevelComment"]["snippet"]["authorDisplayName"]
                        likecount = item["snippet"]["topLevelComment"]["snippet"]["likeCount"]
                        replies = item["snippet"]["totalReplyCount"]
                        dict_ = {"comment": comment, "author": author, "likecount": likecount, "date": date, "replies": replies, "comment_clean": cleaned_comment}
                        comments.append(dict_)
        nextPageToken = data.get("nextPageToken", None)
        if not nextPageToken or iter_number >= 100:
            break
        if iter_number == 0:
            if len(comments) < 5:
                break
        iter_number += 1
    ic(comments)
    return comments

if __name__ == '__main__':
    import os
    test_video = 'SGqg_ZzThDU'
    API_KEY = os.getenv('API_KEY')
    fetch_comments_relevance(test_video, API_KEY)
