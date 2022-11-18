from unittest import TestCase
import utils


class Test(TestCase):
    def test_comment_is_song_list(self):
        self.assertTrue(utils.comment_is_song_list("list\n1:23 Test\n 04:05:06 Test2"))
        self.assertFalse(utils.comment_is_song_list(":(\n"))

    def test_clean_filename(self):
        self.assertEqual(utils.clean_filename('test"<>/:\\|*?:.md'), 'test.md')
