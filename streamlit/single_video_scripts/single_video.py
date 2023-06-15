# Fetching data from a single video

# my function imports
from single_video_scripts.fetch_all_video_info import fetch_all_info

### Importing Packages
import os
from icecream import ic
ic.disable()

### Defining .env and API Key
def single_video_process(video_id):
    API_KEY = os.environ.get('API_KEY')
    ic(video_id)
    result = fetch_all_info(video_id, API_KEY)
    if result:
        comment, info, channel = result

    ### Adding Channel details to Info DataFrame

    info['Total_Views'] = channel['viewCount']
    info['Sub_Count'] = channel['subscriberCount']
    info['Video_Count'] = channel['videoCount']

    ### The big info DataFrame
    return info, comment

if __name__ == '__main__':
    test_video = 'SGqg_ZzThDU'
    single_video_process(test_video)
