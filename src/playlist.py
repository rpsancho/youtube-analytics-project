import isodate
from src.video import Video
from src.youtube_mixin import YoutubeMixin


class PlayList(YoutubeMixin):

    def __init__(self, playlist_id):
        super().__init__()
        self.__playlist_id = playlist_id
        self.__init_from_api()

    def __init_from_api(self):
        playlist_info = self.get_service().playlists().list(
            id=self.__playlist_id,
            part='snippet',
            maxResults=50,
        ).execute()
        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.__playlist_id}'

    @property
    def total_duration(self):

        video_ids: list[str] = self.get_video_list()

        video_response = self.get_service().videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)
        ).execute()

        duration = isodate.duration.timedelta(0, 0, 0, 0, 0, 0, 0)

        for video in video_response['items']:
            iso_dur = isodate.parse_duration(video['contentDetails']['duration'])
            duration += iso_dur
        return duration

    def show_best_video(self):

        video_ids: list[str] = self.get_video_list()

        like_count_max = 0
        best_video_id = ''

        for video_id in video_ids:
            video = Video(video_id)
            like_count = int(video.like_count)
            if like_count > like_count_max:
                like_count_max = like_count
                best_video_id = video.video_id
        best_video = Video(best_video_id)
        return best_video.url

    def get_video_list(self):

        playlist_videos = self.get_service().playlistItems().list(
            playlistId=self.__playlist_id,
            part='contentDetails',
            maxResults=50,
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        return video_ids
