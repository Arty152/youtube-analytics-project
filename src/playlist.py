from src.channel import Channel
from src.video import PLVideo
import datetime
import isodate


class PlayList(Channel):
    """
    Класс для представления YouTube плейлиста.
    Этот класс предоставляет функциональность для работы с плейлистами на YouTube. Он наследует методы и
    функциональность от класса Channel, который, содержит методы для взаимодействия с YouTube API.
    """

    def __init__(self, playlist_id):
        """
        Экземпляр инициализируется id плейлиста.
        :param playlist_id: ID плейлиста на YouTube.
        """
        self.playlist_id = playlist_id
        self.title = self.get_playlists_data()['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

    def get_playlists_data(self):
        """
        Получение данных о плейлисте.
        :return: Словарь с данными о плейлисте.
        """
        return Channel.get_service().playlists().list(id=self.playlist_id,
                                                      part='contentDetails,snippet',
                                                      maxResults=50).execute()

    def get_video_data(self):
        """
        Получение данных о видео в плейлисте.
        :return: Словарь с данными о видео.
        """
        return Channel.get_service().playlistItems().list(playlistId=self.playlist_id,
                                                          part='contentDetails',
                                                          maxResults=50).execute()

    def set_list_video(self):
        """
        Формирование списка видео в плейлисте.
        :return: Список объектов PLVideo.
        """
        list_video = []
        for video in self.get_video_data()['items']:
            list_video.append(PLVideo(video['contentDetails']['videoId'], self.playlist_id))
        return list_video

    def get_duration_playlist(self):
        """
        Получение данных о длительности видео в плейлисте.
        :return: Список с данными о видео.
        """
        list_id = []
        for video in self.set_list_video():
            list_id.append(video.video_id)
        data_items = Channel.get_service().videos().list(part='contentDetails,statistics',
                                                         id=','.join(list_id)).execute()
        return data_items['items']

    @property
    def total_duration(self):
        """
        Вычисление общей длительности плейлиста.
        :return: Общая длительность плейлиста.
        """
        total_duration = datetime.timedelta(0)
        for video in self.get_duration_playlist():
            duration = isodate.parse_duration(video['contentDetails']['duration'])
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Поиск и вывод наилучшего видео по количеству лайков.
        :return: URL наилучшего видео.
        """
        like_count = 0
        best_video_id = None
        for video in self.get_duration_playlist():
            max_like = int(video['statistics']['likeCount'])
            if max_like > like_count:
                like_count = max_like
                best_video_id = video['id']
        if best_video_id:
            return f"https://youtu.be/{video['id']}"
        return None


