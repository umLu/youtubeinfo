import unittest
from tubedata import ChannelInfo


class TestChannelInfo(unittest.TestCase):
    """Tests for the ChannelInfo class."""

    # Youtube channel ID for testing
    TEST_CHANNEL_ID = "UCBR8-60-B28hp2BmDPdntcQ"

    def test_init_with_list(self):
        """Tests initialization with channel ID as list."""
        channel_info = ChannelInfo([self.TEST_CHANNEL_ID], max_results=5)

        self.assertEqual(len(channel_info._channel_ids), 1)
        self.assertEqual(channel_info._channel_ids[0], self.TEST_CHANNEL_ID)

    def test_dataframe_structure(self):
        """Tests the structure of the resulting DataFrame."""
        channel_info = ChannelInfo(self.TEST_CHANNEL_ID, max_results=5)

        self.assertTrue(len(channel_info.df) > 0)

        expected_columns = {
            "channelId",
            "videoId",
            "title",
            "description",
            "publishedAt",
            "caption",
        }
        df_columns = channel_info.df.columns
        self.assertTrue(expected_columns.issubset(set(df_columns)))

    def test_captions(self):
        """Tests of captions."""
        channel_info = ChannelInfo(
            self.TEST_CHANNEL_ID, max_results=5, accepted_caption_lang=["pt", "en"]
        )

        self.assertIn("caption", channel_info.df.columns)


if __name__ == "__main__":
    unittest.main()
