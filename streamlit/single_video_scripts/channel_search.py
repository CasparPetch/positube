from youtubesearchpython import *
import pandas as pd

# my function import
from single_video import single_video_process

from icecream import ic
ic.disable()


def grab_channel(channel_name):
    num_videos = 10
    print("hello")
    # channel_name = 'PewDiePie'

    channelsSearch = ChannelsSearch(channel_name, limit = 1)
    ic(channelsSearch)

    channel_id = channelsSearch.result()["result"][0]["id"]
    ic(channel_id)
    playlist = Playlist(playlist_from_channel_id(channel_id))
    ic(playlist)
    ic(len(playlist.videos))

    print(f'Videos Retrieved: {len(playlist.videos)}')


    while playlist.hasMoreVideos and len(playlist.videos) < num_videos:
        print('Getting more videos...')
        playlist.getNextVideos()
        print(f'Videos Retrieved: {len(playlist.videos)}')

    print('Done')
    ic(len(playlist.videos))

    ids = []
    for video in playlist.videos:
        ids.append(video["id"])
    ids = ids[:num_videos]
    ic(ids)

    infos = []
    comments = []
    for video in ids:
        info, comment = single_video_process(video)
        infos.append(info)
        comments.append(comment)
    return pd.concat(comments), pd.concat(infos)

# grab_channel("PewDiePie")
