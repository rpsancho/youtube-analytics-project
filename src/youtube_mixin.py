import os
from googleapiclient.discovery import build


class YoutubeMixin:

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self):
        pass

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service
