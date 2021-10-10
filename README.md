# Youtube-Info

[![PyPI version](https://badge.fury.io/py/youtubeinfo.svg)](https://badge.fury.io/py/youtubeinfo)

Make YouTube queries and get information from videos (including captions, likes, titles, etc.) ready for Jupyter Notebooks.

## Installation

```shell
pip install youtubeinfo
```

## USAGE

Create a search object
```python
import youtubeinfo.core as yt
yt_search = yt.search("Test", developer_key=<YOUR_YOUTUBE_DEVELOPER_KEY>)
yt_search.df  # DataFrame with YouTube infos (likes, views, title, etc.)
```
__Output example:__
| videoId   | publishedAt               | channelId    | title                 | … | viewCount | likeCount | dislikeCount | favoriteCount | commentCount |
|-----------|---------------------------|--------------|-----------------------|---|-----------|-----------|--------------|---------------|--------------|
| abcde1234 | 2021-06-01 10:00:00+00:00 | abcde1234abc | Video title example 1 | … | 100000    | 6000      | 30           | 0             | 200          |
| abcde1235 | 2021-06-01 11:00:00+00:00 | abcde1234abc | Video title example 2 | … | 200000    | 5000      | 40           | 1             | 210          |
| abcde1236 | 2021-06-01 12:00:00+00:00 | abcde1234abd | Video title example 3 | … | 100000    | 4000      | 50           | 0             | 150          |
| …         | …                         | …            | …                     | … | …         | …         | …            | …             | …            |

### Developer key

To use ```youtubeinfo``` a Google YouTube developer key needs to be created following https://developers.google.com/youtube/registering_an_application?hl=en and can be set as environment variable.

### Developer key as environment variable

**Linux**: edit ~/.profile and add as last line of code:

```bash
export YOUTUBE_DEVELOPER_KEY=<YOUR_YOUTUBE_DEVELOPER_KEY>
```

### Captions

To get captions, use the argument ```captions=True```
```python
import youtubeinfo.core as yt
# YOUTUBE_DEVELOPER_KEY is not necessary if was set as environment variable
yt_search = yt.search("Test", caption=True)
yt_search.df  # A new column with captions "video_caption" will appear
```
__Output example:__
| videoId   | publishedAt               | channelId    | title                 | … | commentCount | video_caption                                            |
|-----------|---------------------------|--------------|-----------------------|---|--------------|----------------------------------------------------------|
| abcde1234 | 2021-06-01 10:00:00+00:00 | abcde1234abc | Video title example 1 | … | 200          | What they say; words and more words; thanks for watching |
| abcde1235 | 2021-06-01 11:00:00+00:00 | abcde1234abc | Video title example 2 | … | 210          | None                                                     |
| abcde1236 | 2021-06-01 12:00:00+00:00 | abcde1234abd | Video title example 3 | … | 150          | Words and more words and more words; thanks for watching |
| …         | …                         | …            | …                     | … | …            | …                                                        |
