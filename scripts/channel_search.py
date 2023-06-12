from youtubesearchpython import *
from single_video import single_video_process

channel_name = 'PewDiePie'

channelsSearch = ChannelsSearch(channel_name, limit = 1)

channel_id = channelsSearch.result()["result"][0]["id"]
playlist = Playlist(playlist_from_channel_id(channel_id))

print(f'Videos Retrieved: {len(playlist.videos)}')


while playlist.hasMoreVideos and len(playlist.videos) < 10:
    print('Getting more videos...')
    playlist.getNextVideos()
    print(f'Videos Retrieved: {len(playlist.videos)}')

print('Done')

ids = []
for video in playlist.videos:
    ids.append(video["id"])
ids = ids[:10]

for video in ids:
    info, comment = single_video_process(video)
    print(info)
