import unittest
from youtubeinfo.core import search


class YoutubeSearch(unittest.TestCase):

    def test_df_shape(self):
        df_shape = search("Test", maxres=25).df.shape
        self.assertEqual(df_shape[0], 25)
        self.assertEqual(df_shape[1], 12)
