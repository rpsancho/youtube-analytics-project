from datetime import datetime
import isodate
from src.youtube_mixin import YoutubeMixin


class PlayList(YoutubeMixin):

    def __init__(self, playlist_id):
        super().__init__()
        self.playlist_id = playlist_id
        self.__init_from_api()

    def __init_from_api(self):
        playlist_info = self.get_service().playlists().list(
            id=self.playlist_id,
            part='snippet',
            maxResults=50,
        ).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    @property
    def total_duration(self):
        playlist_videos = self.get_service().playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = self.get_service().videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()
        duration = 0
        for video in video_response['items']:
            iso_duration = isodate.parse_duration(video['contentDetails']['duration'])
            duration += datetime.fromisoformat(iso_duration)
        return duration

    # @total_duration.setter
    # def total_duration(self, response):
    #     for video in response['items']:
    #         # YouTube video duration is in ISO 8601 format
    #         iso_8601_duration = video['contentDetails']['duration']
    #         # duration = isodate.parse_duration(iso_8601_duration)
    #     return self.duration

    def show_best_video(self):
        pass
