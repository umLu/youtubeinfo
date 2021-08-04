# Youtube-Data

Make YouTube queiries and get data from videos ready for Jupyter Notebooks.

## USAGE

Create a search object
```
import youtubedata.core as yt
yt_search = yt.search("Test", developer_key=<YOUTUBE_DEVELOPER_KEY>)
yt_search.df  # DataFrame with YouTube data (likes, views, title, etc.)
```