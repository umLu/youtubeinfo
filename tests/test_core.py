import unittest
from youtubeinfo import Search


class YoutubeSearch(unittest.TestCase):

    def test_df_shape(self):
        df_shape = Search("Test", maxres=25).df
        self.assertTrue(df_shape.shape[0] >= 1)
        self.assertEqual(df_shape.shape[1], 11)

    def test_caption(self):
        df_caption = Search("Test", caption=True).df['video_caption']
        self.assertTrue(
            len([_ for _ in df_caption.to_list() if _ is None]) > 0
            )

    def test_channel(self):
        df_channel = Search("Test", item_type="channel").df
        self.assertTrue(df_channel.shape[0] >= 1)
        self.assertEqual(df_channel.shape[1], 6)

    def test_big_shape(self):
        df_shape = Search("Test", maxres=100).df.shape
        self.assertTrue(df_shape[0] >= 50)
