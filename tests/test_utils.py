import unittest
import os
import pandas as pd
from tubeframes.utils import (
    get_dev_key,
    create_tubeframes_client,
    get_video_captions,
    get_video_statistics,
    create_df_from_items,
)


class TestUtilsFunctions(unittest.TestCase):
    """Tests for utility functions."""

    # YouTube video for test
    TEST_VIDEO_ID = "_GuOjXYl5ew"

    def setUp(self):
        """Set up the test environment."""
        # If YOUTUBE_DEVELOPER_KEY is not set in environment, skip tests
        if "YOUTUBE_DEVELOPER_KEY" not in os.environ:
            self.skipTest("YOUTUBE_DEVELOPER_KEY environment variable not set")
        self.developer_key = os.environ["YOUTUBE_DEVELOPER_KEY"]

    def test_get_dev_key_from_env(self):
        """Test getting developer key from environment."""
        key = get_dev_key()
        self.assertEqual(key, self.developer_key)

    def test_get_dev_key_from_param(self):
        """Test getting developer key from parameter."""
        test_key = "test_key_value"
        key = get_dev_key(test_key)
        self.assertEqual(key, test_key)

    def test_create_tubeframes_client(self):
        """Test creating tubeframes client."""
        client = create_tubeframes_client(self.developer_key)
        self.assertTrue(hasattr(client, "search"))
        self.assertTrue(hasattr(client, "videos"))
        self.assertTrue(hasattr(client, "activities"))

    def test_get_video_statistics(self):
        """Test getting video statistics."""
        stats = get_video_statistics(self.TEST_VIDEO_ID, self.developer_key)
        # Check if statistics has expected fields
        self.assertIn("viewCount", stats)
        self.assertIn("likeCount", stats)

    def test_get_video_captions(self):
        """Test getting video captions."""
        captions = get_video_captions(self.TEST_VIDEO_ID, ["en"])
        self.assertTrue(captions is None or isinstance(captions, str))

    def test_create_df_from_items(self):
        """Test creating DataFrame from items."""
        # Test with empty list
        df = create_df_from_items([])
        self.assertTrue(df.empty)

        # Test with multiple items
        items = [
            {"title": "Video 1", "publishedAt": "2022-01-01T00:00:00Z"},
            {"title": "Video 2", "publishedAt": "2022-01-02T00:00:00Z"},
        ]
        df = create_df_from_items(items)
        self.assertEqual(len(df), 2)
        self.assertIn("title", df.columns)
        self.assertIn("publishedAt", df.columns)
        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(df["publishedAt"])
            or isinstance(df["publishedAt"].iloc[0], pd.Timestamp)
        )

        # Test with items missing publishedAt
        items = [{"title": "Video 1"}, {"title": "Video 2"}]
        df = create_df_from_items(items)
        self.assertEqual(len(df), 2)
        self.assertNotIn("publishedAt", df.columns)


if __name__ == "__main__":
    unittest.main()
