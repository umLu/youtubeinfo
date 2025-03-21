import unittest
from youtubeinfo.core import search


class YoutubeSearch(unittest.TestCase):

    def test_df_shape(self):
        df_shape = search("Test", maxres=25).df.shape
        self.assertTrue(df_shape[0] >= 1)
        self.assertEqual(df_shape[1], 11)

    def test_caption(self):
        df_caption = search("Test", caption=True).df['video_caption']
        self.assertTrue(
            len([_ for _ in df_caption.to_list() if _ is None]) > 0
            )
