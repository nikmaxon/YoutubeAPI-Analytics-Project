import datetime
import os
from pprint import pprint
from datetime import timedelta
import isodate
from googleapiclient.discovery import build


class PlayList:
    api_key: str = os.getenv('YouTube API')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.title = self.playlist_info()['items'][0]['snippet']['localized']['title']
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        self.playlist_videos = self.youtube.playlistItems().list(playlistId=self.playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        self.video_ids = [video['contentDetails']['videoId'] for video in self.playlist_videos['items']]
        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(self.video_ids)
                                                    ).execute()

    def playlist_info(self):
        playlist_videos = self.youtube.playlists().list(part='snippet',
                                                        id=self.playlist_id,
                                                        ).execute()
        return playlist_videos

    @property
    def total_duration(self):
        res = timedelta()

        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            res += duration
        return res

    def show_best_video(self):
        likes = 0

        for video_id in self.video_ids:

            video_request = self.youtube.videos().list(
                part='statistics',
                id=video_id
            ).execute()

            like_count = video_request['items'][0]['statistics']['likeCount']

            if int(like_count) > likes:
                likes = int(like_count)
                best_video = f"https://youtu.be/{video_request['items'][0]['id']}"

        return best_video


#pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
#pprint(pl.show_best_video())
