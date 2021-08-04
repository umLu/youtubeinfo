# Youtube-Info

Make YouTube queries and get text information from videos (including captions) ready for Jupyter Notebooks.

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

### Developer key

**YOUTUBE_DEVELOPER_KEY** has to be created following https://developers.google.com/youtube/registering_an_application?hl=en and can be set as environment variable

### Developer key as environment variable

**Linux**: edit ~/.profile and add as last line of code

```
export YOUTUBE_DEVELOPER_KEY=<YOUTUBE_DEVELOPER_KEY>
```

### Captions

To get captions, use the argument ```captions=True```
```
import youtubeinfo.core as yt
# YOUTUBE_DEVELOPER_KEY is not necessary if was set as environment variable
yt_search = yt.search("Test", caption=True)  
yt_search.df  # A new column with captions "video_caption" will appear
```