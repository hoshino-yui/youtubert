from unittest import TestCase
import main


class Test(TestCase):
    def test_comment_is_song_list(self):
        self.assertTrue(main.comment_is_song_list("list\n1:23 Test\n 04:05:06 Test2"))
        self.assertFalse(main.comment_is_song_list(":(\n"))
