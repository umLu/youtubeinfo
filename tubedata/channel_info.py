import pandas as pd
from typing import List, Union, Dict, Optional

from tubedata.utils import (
    get_developer_key,
    create_tubedata_client,
    get_video_captions,
    process_thumbnails,
    create_dataframe_from_items,
)


class ChannelInfo:
    """Class to get information about videos from YouTube channels."""

    def __init__(
        self,
        channel_ids: Union[str, List[str]],
        max_results: int = 10,
        accepted_caption_lang: List[str] = ["pt", "en"],
        developer_key: Optional[str] = None,
    ) -> None:
        """
        Initialize the class to get information about videos from channels.

        Args:
            channel_ids: YouTube channel ID(s).
            max_results: Maximum number of results per channel.
            accepted_caption_lang: List of accepted languages for captions.
            developer_key: YouTube API developer key.
        """
        self._accepted_caption_lang = accepted_caption_lang
        self._developer_key = get_developer_key(developer_key)

        if isinstance(channel_ids, str):
            channel_ids = [channel_ids]

        self._channel_ids = channel_ids
        self._max_results = max_results
        self._youtube = create_tubedata_client(self._developer_key)

        self.raw_data = self._fetch_channel_videos()
        self.df = self._build_dataframe()

    def _fetch_channel_videos(self) -> Dict:
        """
        Get videos from specified channels.

        Returns:
            Dict: Dictionary with data obtained from the API.
        """
        all_data = {}

        for channel_id in self._channel_ids:
            try:
                response = (
                    self._youtube.activities()
                    .list(
                        part="snippet,contentDetails",
                        channelId=channel_id,
                        maxResults=self._max_results,
                    )
                    .execute()
                )

                all_data[channel_id] = response
            except Exception as e:
                print(f"Error fetching videos for channel {channel_id}: {str(e)}")

        return all_data

    def _build_dataframe(self) -> pd.DataFrame:
        """
        Build a DataFrame from the collected data.

        Returns:
            pd.DataFrame: DataFrame with video information and captions.
        """
        video_data = []

        for channel_id, response in self.raw_data.items():
            if "items" not in response:
                continue

            for item in response["items"]:
                if item["snippet"]["type"] != "upload":
                    continue

                # Only process items that have a videoId
                if "upload" not in item.get("contentDetails", {}):
                    continue

                video_id = item["contentDetails"]["upload"].get("videoId")
                if not video_id:
                    continue

                # Extract information from snippet
                snippet = item["snippet"]

                # Build the dictionary with video information
                video_info = {
                    "channelId": channel_id,
                    "videoId": video_id,
                    "title": snippet.get("title"),
                    "description": snippet.get("description"),
                    "publishedAt": snippet.get("publishedAt"),
                    "caption": get_video_captions(
                        video_id, self._accepted_caption_lang
                    ),
                }

                # Process thumbnails
                video_info = process_thumbnails(snippet, video_info)

                video_data.append(video_info)

        # Create DataFrame from collected items
        return create_dataframe_from_items(video_data)
