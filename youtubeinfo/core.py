import os
import time
from apiclient.discovery import build
from apiclient.errors import HttpError
import requests
import pandas as pd
from youtube_transcript_api import YouTubeTranscriptApi
from youtubeinfo.config.constants import YOUTUBE_API_SERVICE_NAME
from youtubeinfo.config.constants import YOUTUBE_API_VERSION
from youtubeinfo.config.constants import YOUTUBE_API_URL


class Search:
    """Main class for YouTube search."""

    DEFAULT_MAX_RES = 50

    def __init__(self,
                 term: str,
                 caption: bool = False,
                 maxres: int = 50,
                 accepted_caption_lang: list = ['en'],
                 item_type: str = "video",
                 developer_key: str = None) -> None:
        self._accepted_caption_lang = accepted_caption_lang
        if developer_key is None:
            try:
                self._developer_key = os.environ['YOUTUBE_DEVELOPER_KEY']
            except KeyError:
                raise ValueError("YouTube Developer Key not found")
        else:
            self._developer_key = developer_key
        self.raw = self._consolidate_search(term, maxres, item_type)
        self.df = self._build_dataframe(item_type=item_type, caption=caption)

    def _consolidate_search(self,
                            term: str,
                            maxres: int,
                            item_type: str) -> list:
        if maxres <= self.DEFAULT_MAX_RES:
            results = maxres
            maxres = 0
        else:
            results = self.DEFAULT_MAX_RES
            maxres -= self.DEFAULT_MAX_RES

        search_list = self._search_from_term(term, results, item_type)
        consolidated_search = [search_list]
        while 'nextPageToken' in search_list.keys() and maxres > 0:
            time.sleep(0.1)  # Avoid request overload
            consolidated_search.append(
                self._search_from_term(term,
                                       results,
                                       page_token=search_list['nextPageToken'])
                )
            maxres -= self.DEFAULT_MAX_RES
        return consolidated_search

    def _search_from_term(self,
                          term: str,
                          maxres: int = 50,
                          item_type: str = "video",
                          page_token: str = None) -> dict:
        try:
            search_list = self._search_request(term, maxres, page_token, item_type)
            # Validate response
            if isinstance(search_list, dict):
                if not set(search_list.keys()).issuperset(
                    set(['kind',
                         'etag',
                         'regionCode',
                         'pageInfo',
                         'items'])):
                    raise KeyError
            else:
                raise TypeError
        except HttpError as e:
            print("An HTTP error %d"
                  " occurred:\n%s" % (e.resp.status, e.content))
            raise
        return search_list

    def _search_request(self,
                        term: str,
                        maxres: int = 50,
                        page_token: str = None,
                        item_type: str = "video") -> dict:
        """Query YouTube."""
        youtube = build(YOUTUBE_API_SERVICE_NAME,
                        YOUTUBE_API_VERSION,
                        developerKey=self._developer_key)
        search_response = youtube.search().list(
            q=term,
            part="id,snippet",
            maxResults=maxres,
            pageToken=page_token,
            type=item_type,
            safeSearch="none"
        ).execute()
        return search_response

    def _build_dataframe(self,
                         item_type: str = "video",
                         caption: bool = False):
        appended_data = []
        for search_req in self.raw:
            for search_item in search_req['items']:
                try:
                    if item_type == "video":
                        id_key = 'videoId'
                    elif item_type == "channel":
                        id_key = 'channelId'
                    else:
                        continue
                    if not (
                        'id' in search_item and
                        id_key in search_item['id'] and
                        'snippet' in search_item
                    ):
                        continue
                    item_id = search_item['id'][id_key]

                    search_results = search_item['snippet']
                    search_results.pop("thumbnails", None)
                    search_results[id_key] = item_id

                    if item_type == "video":
                        item_stats = self.get_statistics(item_id)
                        item_stats[id_key] = item_id

                        if caption:
                            _, video_caption = self.get_captions(item_id)
                            caption_dict = {'video_caption': video_caption}
                            item_metadata = {
                                **search_results, 
                                **item_stats,
                                **caption_dict
                            }
                        else:
                            item_metadata = {
                                **search_results,
                                **item_stats
                            }
                    else:
                        item_metadata = {**search_results}

                    item_metadata = pd.DataFrame.from_dict([item_metadata])
                    appended_data.append(item_metadata)

                except Exception:
                    continue

        if len(appended_data):
            appended_data = pd.concat(appended_data)

            if item_type == "video":
                appended_data.dropna(axis=0,
                                     how='any',
                                     inplace=True,
                                     subset=['likeCount',
                                             'viewCount'])
                df_youtube = appended_data.astype({"likeCount": int,
                                                   "viewCount": int})
            else:
                df_youtube = appended_data

            df_youtube['publishedAt'] = pd.to_datetime(
                df_youtube['publishedAt'])
            df_youtube.set_index(id_key, inplace=True)
            return df_youtube
        else:
            print('No results. The DataFrame attribute will be None')
            return None

    def get_statistics(self,
                       video_id: str) -> dict:
        ploads = {'part': 'statistics',
                  'id': video_id,
                  'key': self._developer_key}
        r = requests.get(YOUTUBE_API_URL,
                         params=ploads,
                         timeout=180)
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
