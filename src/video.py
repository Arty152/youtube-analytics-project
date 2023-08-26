from src.channel import APIMixin

class Video(APIMixin):
    """Класс для работы с видео из ютуба."""

    def __init__(self, video_id: str) -> None:
        """Видео инициализируется id и далее через API"""
        self.__video_id = video_id
        self._init_from_api()

    def _init_from_api(self):
        """Получаем данные по API и инициализируем ими экземпляр класса."""
        video_response = self.get_service().videos().list(part='snippet,statistics',
                                                          id=self.__video_id
                                                          ).execute()

        self.title = video_response['items'][0]['snippet']['title']
        self.url = f'https://youtu.be/{self.__video_id}'
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']

    def __str__(self) -> str:
        """Шаблон: <название_видео>."""
        return self.title


class PLVideo(Video):
    """Класс для видео, у которого есть плейлист."""

    def __init__(self, video_id: str, plist_id: str) -> None:
        """Инициализируется id видео и плейлиста."""
        super().__init__(video_id)
        self.plist_id = plist_id
