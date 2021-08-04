# Youtube-Info

Make YouTube queiries and get data from videos ready for Jupyter Notebooks.

## Installation

```
pip install youtubeinfo
```

## USAGE

Create a search object
```
import youtubeinfo.core as yt
yt_search = yt.search("Test", developer_key=<YOUTUBE_DEVELOPER_KEY>)
yt_search.df  # DataFrame with YouTube info (likes, views, title, etc.)
```