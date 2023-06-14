import requests
from icecream import ic
ic.disable()

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

def fetch_details(video_id, api_key):
        url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
        ic(url)
        response = requests.get(url)
    #     print(response.status_code)
        try:
            data = response.json()
        except ValueError:
            print(f"{url} failed!")
        error = data.get("error",False)
        if not error:
            data = data.get("items",False)
            ic(data)
            if data:
                date = data[0]["snippet"]["publishedAt"]
                channel_id = data[0]["snippet"]["channelId"]
                title = data[0]["snippet"]["title"]
                description = data[0]["snippet"]["description"]
                thumbnail = data[0]["snippet"]["thumbnails"].get("maxres",{0:0}).get("url",0)
                channel_title = data[0]["snippet"]["channelTitle"]
                tags = data[0]["snippet"].get("tags",[""])
                genre = genre_dict[data[0]["snippet"]["categoryId"]]
                language = data[0]["snippet"].get("defaultAudioLanguage","")
                dict_ = {"date":date, "channel_id":channel_id, "title":title, "description":description, "thumbnail":thumbnail,"channel_title":channel_title, "tags":[tags], "genre":genre, "language":language}
                ic(dict_)
                return dict_
            return {}
        else:
            return {}

if __name__ == '__main__':
    import os
    test_video = 'SGqg_ZzThDU'
    API_KEY = os.getenv('API_KEY')
    fetch_details(test_video, API_KEY)
