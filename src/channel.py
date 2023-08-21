import os
import json
from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv('YOUTUBE_API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.init_from_api()

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return int(self.subscriber_сount) + int(other.subscriber_сount)

    def __sub__(self, other):
        return int(self.subscriber_сount) - int(other.subscriber_сount)

    def __gt__(self, other):
        return int(self.subscriber_сount) > int(other.subscriber_сount)

    def __ge__(self, other):
        return int(self.subscriber_сount) >= int(other.subscriber_сount)

    def __lt__(self, other):
        return int(self.subscriber_сount) < int(other.subscriber_сount)

    def __le__(self, other):
        return int(self.subscriber_сount) < int(other.subscriber_сount)

    def __eq__(self, other):
        return int(self.subscriber_сount) == int(other.subscriber_сount)

    @property
    def channel_id(self):
        return self.__channel_id

    # @channel_id.setter
    # def channel_id(self, value):
    #     self.__channel_id = value

    def init_from_api(self):
        youtube = self.get_service()
        channel = youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
        self.subscriber_сount = channel['items'][0]['statistics']['subscriberCount']
        self.video_count = channel['items'][0]['statistics']['videoCount']
        self.view_сount = channel['items'][0]['statistics']['viewCount']

    @property
    def url(self):
        """Возвращает ссылку на канал."""
        return f"https://www.youtube.com/channel/{self.__channel_id}"


    @url.setter
    def url(self, value):
        self.__url = value

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
