import requests
from icecream import ic
ic.disable()

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
                ic(dict_)
                return dict_
            return {}
        else:
            return {}

if __name__ == '__main__':
    import os
    test_channel = 'UCPKT_csvP72boVX0XrMtagQ'
    API_KEY = os.getenv('API_KEY')
    fetch_channel(test_channel, API_KEY)
