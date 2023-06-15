import requests
from icecream import ic
ic.disable()

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
            likes = data[0]["statistics"].get("likeCount",0)
            comments = data[0]["statistics"].get("commentCount",0)
            dict_ = {"views":[views], "likes":[likes], "comments":[comments]}
            # ic(dict_)
            return dict_
        return {}
    else:
        return {}

if __name__ == '__main__':
    import os
    test_video = 'SGqg_ZzThDU'
    API_KEY = os.getenv('API_KEY')
    fetch_stats(test_video, API_KEY)
