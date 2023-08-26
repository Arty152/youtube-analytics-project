from src.channel import APIMixin


class Video(APIMixin):
    """
    Класс для работы с видео из YouTube.
    Attributes:
        __video_id (str): ID видео.
        title (str): Название видео.
        url (str): URL видео.
        view_count (int): Количество просмотров видео.
        like_count (int): Количество лайков видео.
    """

    def __init__(self, video_id: str) -> None:
        """
        Инициализирует объект Video с заданным ID видео.
        Args:
            video_id (str): ID видео на YouTube.
        """
        self.__video_id = video_id
        self._init_from_api()

    @property
    def video_id(self) -> str:
        return self.__video_id

    def _init_from_api(self):
        """
        Получает данные о видео через API и инициализирует атрибуты класса.
        """
        video_response = self.get_service().videos().list(part='snippet,statistics',
                                                          id=self.video_id
                                                          ).execute()

        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self) -> str:
        return f'{self.title}'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.video_id}')"


class PLVideo(Video):
    """
    Класс для работы с видео, которое принадлежит к плейлисту на YouTube.
    Attributes:
        plist_id (str): ID плейлиста, к которому относится видео.
    """
    def __init__(self, video_id: str, plist_id: str) -> None:
        """
        Инициализирует объект PLVideo с заданным ID видео и плейлиста.
        Args:
            video_id (str): ID видео на YouTube.
            plist_id (str): ID плейлиста на YouTube.
        """
        super().__init__(video_id)
        self.plist_id = plist_id

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.video_id}', '{self.plist_id}')"