from src.channel import APIMixin
import datetime
import isodate


class PlayList(APIMixin):
    """Класс для работы в плейлистами на YouTube.
    Attributes:
        title (str): Название плейлиста.
        url (str): Ссылка на плейлист на YouTube.
    """

    def __init__(self, playlist_id: str) -> None:
        """
        Инициализирует ID плейлиста и результатами запроса по API.
        Args:
            playlist_id: ID плейлиста.
        """
        self.__playlist_id = playlist_id
        self._init_from_api()

    def _init_from_api(self) -> None:
        """Получаем данные по API и инициализируем ими экземпляр класса."""
        playlist_info = self.get_service().playlists().list(id=self.__playlist_id,
                                                            part='snippet').execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    def _get_playlist_videos(self) -> dict:
        """Получает ответ API на запрос всех видео плейлиста.
        Returns:
            dict: Ответ API на запрос всех видео плейлиста."""
        return self.get_service().playlistItems().list(playlistId=self.__playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50).execute()

    def set_list_video(self) -> list:
        """
        Формирует список ID видео в плейлисте.
        Returns:
            list: Список ID видео.
        """
        list_video = []
        [list_video.append(video['contentDetails']['videoId']) for video in self._get_playlist_videos()['items']]
        return list_video

    def get_duration_playlist(self) -> dict:
        """
        Получает данные о длительности видео в плейлисте.
        Returns:
            dict: Информация о длительности видео.
        """
        list_ids = self.set_list_video()
        return self.get_service().videos().list(part='contentDetails,statistics',
                                                id=','.join(list_ids)).execute()

    @property
    def total_duration(self) -> datetime.timedelta:
        """
        Возвращает суммарную длительность плейлиста в формате 'datetime.timedelta' (hh:mm:ss).
        Returns:
            datetime.timedelta: Суммарная длительность плейлиста.
        """
        return sum([isodate.parse_duration(video['contentDetails']['duration'])
                    for video in self.get_duration_playlist()['items']], datetime.timedelta())
        # datetime.timedelta()
        # for video in self.get_duration_playlist()['items']:
        #     duration += isodate.parse_duration(video['contentDetails']['duration'])
        # return duration

    def show_best_video(self) -> str:
        """
        Поиск и вывод наилучшего видео по количеству лайков.
        :return: URL наилучшего видео.
        """
        like_count = 0
        for video in self.get_duration_playlist()['items']:
            max_like = int(video['statistics']['likeCount'])
            if max_like > like_count:
                like_count = max_like
        if video['id']:
            return f"https://youtu.be/{video['id']}"
        return None
