import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.init_from_api()

    @property
    def channel_id(self):
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, value):
        self.__channel_id = value

    def init_from_api(self):
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_сount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_сount = channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_info = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        print(f'Информация о канале:\n{json.dumps(channel_info, indent=4, ensure_ascii=False)}')

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        service = build('youtube', 'v3', developerKey=cls.api_key)
        return service

    def to_json(self, file_name: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        attribute_values = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_сount,
            'video_count': self.video_count,
            'view_count': self.view_сount
        }

        with open(file_name, "w", encoding='utf-8') as f:
            json.dump(attribute_values, f, indent=4, ensure_ascii=False)
