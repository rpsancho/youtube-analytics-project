import json
import os
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.__init_from_api()

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)

    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)

    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)

    def __le__(self, other):
        return int(self.subscriber_count) <= int(other.subscriber_count)

    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)

    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)

    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)

    def __init_from_api(self):
        channel_info = self.get_service().channels().list(
            id=self.__channel_id,
            part='snippet,statistics'
        ).execute()
        self.title = channel_info['items'][0]['snippet']['title']
        self.description = channel_info['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = channel_info['items'][0]['statistics']['subscriberCount']
        self.video_count = channel_info['items'][0]['statistics']['videoCount']
        self.view_count = channel_info['items'][0]['statistics']['viewCount']

    @property
    def channel_id(self):
        return self.__channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        service = self.get_service()
        channel_info = service.channels().list(
            id=self.__channel_id,
            part='snippet,statistics'
        ).execute()
        print(json.dumps(channel_info, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service

    def to_json(self, file_name):
        attr_list = [
            self.__channel_id,
            self.title,
            self.description,
            self.url,
            self.subscriber_count,
            self.video_count,
            self.view_count
        ]
        with open(file_name, "w+") as f:
            json.dump(attr_list, f, ensure_ascii=False)
