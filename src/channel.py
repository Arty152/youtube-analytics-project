import os
import json
from googleapiclient.discovery import build


class APIMixin:
    """Класс-миксин для предоставления доступа к API."""
    __API_KEY: str = os.getenv('YOUTUBE_API_KEY')

    @classmethod
    def get_service(cls) -> build:
        """
        Возвращает объект для работы с YouTube API.
        Returns:
            build: Объект для работы с YouTube API.
        """
        service = build('youtube', 'v3', developerKey=cls.__API_KEY)
        return service


class Channel(APIMixin):
    """
    Класс для представления YouTube-канала.
    Attributes:
        title (str): Название канала.
        description (str): Описание канала.
        url (str): URL канала на YouTube.
        subscriber_count (int): Количество подписчиков на канале.
        video_count (int): Количество видео на канале.
        view_count (int): Общее количество просмотров канала.
    """

    def __init__(self, channel_id: str) -> None:
        """
       Инициализирует экземпляр класса с использованием ID канала.
       Args:
           channel_id (str): ID канала на YouTube.
       """

        self.__channel_id = channel_id
        self._init_from_api()


    def _init_from_api(self) -> None:
        """Получаем данные по API и инициализируем ими экземпляр класса."""
        channel = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = channel['items'][0]['snippet']['title']
        self.description = channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.subscriber_count = int(channel['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(channel['items'][0]['statistics']['videoCount'])
        self.view_count = int(channel['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f'{self.title} ({self.url})'


    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)


    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)


    def __gt__(self, other):
        return int(self.subscriber_count) > int(other.subscriber_count)


    def __ge__(self, other):
        return int(self.subscriber_count) >= int(other.subscriber_count)


    def __lt__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)


    def __le__(self, other):
        return int(self.subscriber_count) < int(other.subscriber_count)


    def __eq__(self, other):
        return int(self.subscriber_count) == int(other.subscriber_count)


    @property
    def channel_id(self) -> str:
        """
        Возвращает ID канала.
        Returns:
            str: ID канала на YouTube.
        """
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))


    def to_json(self, filename: str) -> None:
        """
        Сохраняет данные экземпляра класса в файл в формате JSON.
        Args:
            filename (str): Имя файла, в который будут сохранены данные.
        """
        dict_to_write = {
            'channel_id': self.__channel_id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count,
        }
        with open(filename, 'w') as fp:
            json.dump(dict_to_write, fp)
