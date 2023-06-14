# my function imports
from fetching_details import fetch_details
from fetch_channel import fetch_channel
from fetch_stats import fetch_stats
from comments_relevance import fetch_comments_relevance
import pandas as pd

# temporary
from icecream import ic
ic.disable()

def fetch_all_info(video_id, api_key):
        # fetch the details of the individual video
        details = pd.DataFrame(fetch_details(video_id, api_key))
        # testing fetch_comments_relevance it works!
        comments_relevance = pd.DataFrame(fetch_comments_relevance(video_id, api_key))
        # testing fetch_stats and it works!
        stats = pd.DataFrame(fetch_stats(video_id, api_key))
        ic(details)
        ic(stats)
        ic(comments_relevance)
        # testing fetch_channel and it works!
        channel = pd.DataFrame([fetch_channel(details['channel_id'][0], api_key)])
        info_all = pd.concat([stats,details],axis=1)
        ic(info_all.head(2))
        comments_relevance["video_id"] = video_id
        info_all["video_id"] = video_id
        ic(comments_relevance.columns)
        ic(type(comments_relevance))
        ic(type(comments_relevance.at[2, 'comment_clean']))
        return comments_relevance, info_all, channel

if __name__ == '__main__':
    import os
    test_video = 'SGqg_ZzThDU'
    API_KEY = os.getenv('API_KEY')
    fetch_all_info(test_video, API_KEY)
