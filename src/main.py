#!/usr/bin/env python3
import json
import sys

import yt_dlp
import utils
from datetime import datetime
from model.comment import Comment
from model.video import Video


def write_video(video: Video):
    try:
        file_lines = video.generate_markdown_lines()
        if file_lines:
            filename = video.generate_filename()
            write_file(filename, file_lines)
    except IOError as e:
        print(f"Failed to write video {video.video_id} - {video.title}")
        print(e)


def write_file(filename, lines):
    with utils.create_and_write_file(filename) as file:
        file.write("\n\n".join(lines))


def extract_timestamp(video):
    date_format = "%Y%m%d"
    if video["release_timestamp"]:
        return datetime.utcfromtimestamp(video["release_timestamp"])
    elif video["upload_date"]:
        return datetime.strptime(video["upload_date"], date_format)
    else:
        return None


def extract_comment(comment):
    return Comment(comment["id"], comment["text"])


def extract_comments(video):
    if video["comments"]:
        comments = video["comments"]
        return [extract_comment(comment) for comment in comments if utils.comment_is_song_list(comment["text"])]
    else:
        return []


def extract_video(video) -> Video:
    return Video(
        video["channel"],
        video["channel_id"],
        video["title"],
        video["id"],
        video["webpage_url"],
        extract_timestamp(video),
        extract_comments(video)
    )


def process_video(video):
    video = extract_video(video)
    write_video(video)


def extract_entry(entry):
    if entry.get('_type') == 'playlist':
        for sub_entry in entry["entries"]:
            if sub_entry:
                extract_entry(sub_entry)
    else:
        process_video(entry)


def extract_url(url):
    ydl_opts = {
        "getcomments": True,
        "extractor_retries": 3,
        "ignoreerrors": True,
        "extractor_args": {'youtube': {
            # 'max_comments': ['100'],
            'skip': ['dash'],
            'comment_sort': ['top']}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        # json.dump(info, sys.stdout)
        # print()
        extract_entry(info)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        extract_url(arg)
