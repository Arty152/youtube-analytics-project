import os
import json
from googleapiclient.discovery import build



class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)
    attribute_values = []

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = self.channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_сount = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.view_сount = self.channel['items'][0]['statistics']['viewCount']

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(f'Информация о канале:\n{self.channel}')

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return cls.youtube

    def to_json(self, data: str) -> None:
        """Сохраняет в файл значения атрибутов экземпляра `Channel`"""
        self.attribute_values.append((self.title, self.description, self.url,
                                      self.subscriber_сount, self.video_count, self.view_сount))

        with open("moscowpython.json", "w") as f:
            json.dump(Channel.attribute_values, f)
