import os
from googleapiclient.discovery import build


class Video:

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id: str):
        self.__video_id = video_id
        self.__init_from_api()

    def __init_from_api(self):
        video_info = self.get_service().videos().list(
            part='snippet,statistics',
            id=self.__video_id
        ).execute()
        self.title = video_info['items'][0]['snippet']['title']
        self.description = video_info['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/watch?v={self.__video_id}'
        self.view_count = video_info['items'][0]['statistics']['viewCount']
        self.like_count = video_info['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f"{self.title}"

    @property
    def video_id(self):
        return self.__video_id

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str):
        super().__init__(video_id)
        self.__playlist_id = playlist_id

    @property
    def playlist_id(self):
        return self.__playlist_id
