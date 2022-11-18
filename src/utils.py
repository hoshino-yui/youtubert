import re
import os.path
from pathlib import Path


def comment_is_song_list(text):
    return "\n" in text and re.search(r"\d:\d\d", text)


def clean_filename(filename):
    return re.sub(r'[/\\<>:|?*"]', '', filename)


def create_and_write_file(filename):
    Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
    return Path(filename).open('w')

