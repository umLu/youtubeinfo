"""
TubeData - A YouTube Data Analysis Library

A Python package for retrieving YouTube data, including video statistics, captions, and channel information. TubeData outputs results in a user-friendly pandas DataFrame format, making it ideal for data analysis workflows — especially in Jupyter Notebooks.
"""

from tubedata.search import Search
from tubedata.channel_info import ChannelInfo

__version__ = "0.3.0"
__license__ = "GNU General Public License v3 (GPLv3)"
__url__ = "https://github.com/umLu/tubedata"
__all__ = ["Search", "ChannelInfo"]
