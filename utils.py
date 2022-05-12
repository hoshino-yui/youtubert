import re


def comment_is_song_list(text):
    return "\n" in text and re.search(r"\d:\d\d", text)


def clean_filename(filename):
    return re.sub(r'[/\\<>:|?*"]', '', filename)
