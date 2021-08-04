from apiclient.discovery import build
from apiclient.errors import HttpError
import requests
import pandas as pd
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtubeinfo.config.constants import YOUTUBE_API_SERVICE_NAME
from youtubeinfo.config.constants import YOUTUBE_API_VERSION
from youtubeinfo.config.constants import YOUTUBE_API_URL


class search:
    """Main class for YouTube search."""

    def __init__(self,
                 term: str,
                 caption: bool = False,
                 maxres: int = 50,
                 accepted_caption_lang: list = ['en'],
                 developer_key: str = None) -> None:
        if developer_key is None:
            self._developer_key = os.environ['YOUTUBE_DEVELOPER_KEY']
        else:
            self._developer_key = developer_key
        self._accepted_caption_lang = accepted_caption_lang
        self.raw = self._search_from_term(term, maxres)
        self.df = self._build_dataframe(caption=caption)

    def _search_from_term(self,
                          term: str,
                          maxres: int = 50):
        try:
            search_list = self._search_request(term, maxres)
        except HttpError as e:
            print("An HTTP error %d"
                  " occurred:\n%s" % (e.resp.status, e.content))
            raise
        return search_list

    def _search_request(self,
                        term: str,
                        maxres: int = 50):
        """Query Youtube."""
        youtube = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        developerKey=self._developer_key)

        # Call the search.list method to retrieve results matching the
        # specified query term.
        search_response = youtube.search().list(
            q=term,
            part="id,snippet",
            maxResults=maxres
        ).execute()
        return search_response

    def _build_dataframe(self,
                         caption: bool = False):
        appended_data = []
        for search_item in self.raw['items']:
            video_id = search_item['id']['videoId']
            search_results = search_item['snippet']
            search_results.pop("thumbnails", None)
            search_results['videoId'] = video_id
            video_statistics = self.get_statistics(video_id)
            video_statistics['videoId'] = video_id
            if caption:
                _, video_caption = self.get_captions(video_id)
                video_caption = {'video_caption': video_caption}
                video_metadata = {**search_results,
                                  **video_statistics,
                                  **video_caption}
            else:
                video_metadata = {**search_results,
                                  **video_statistics}

            video_metadata = pd.DataFrame.from_dict([video_metadata])
            appended_data.append(video_metadata)
        appended_data = pd.concat(appended_data)
        appended_data.dropna(axis=0,
                             how='any',
                             inplace=True,
                             subset=['likeCount',
                                     'dislikeCount',
                                     'viewCount'])
        df_youtube = appended_data.astype({"likeCount": int,
                                           "dislikeCount": int,
                                           "viewCount": int})
        df_youtube['publishedAt'] = pd.to_datetime(
            df_youtube['publishedAt'])
        df_youtube.set_index('videoId',
                             inplace=True)
        return df_youtube

    def get_statistics(self,
                       video_id: str) -> dict:
        ploads = {'part': 'statistics',
                  'id': video_id,
                  'key': self._developer_key}
        r = requests.get(YOUTUBE_API_URL,
                         params=ploads)
        return r.json()['items'][0]['statistics']

    def get_captions(self,
                     video_id: str) -> str:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.\
                find_transcript(self._accepted_caption_lang)
            language = transcript.language_code

            caption = transcript.fetch()
            df_caption = pd.DataFrame.from_dict(caption)
            video_caption = '; '.join(df_caption['text'])
        except Exception:
            language = None
            video_caption = None
        return language, video_caption
