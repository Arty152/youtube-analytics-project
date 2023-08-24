from src.channel import Channel
import pprint
channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'


playlists = Channel.get_service().playlists().list(channelId=channel_id,
                                                   part='contentDetails,snippet',
                                                   maxResults=50,
                                                   ).execute()

playlist_Id = playlists['items'][0]['id']

playlist_videos = Channel.get_service().playlistItems().list(playlistId=playlist_Id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()

video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
print(video_ids)


print(playlist_Id)
pprint.pprint(playlist_videos)