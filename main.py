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


def extract_comments(comments):
    return [extract_comment(comment) for comment in comments if utils.comment_is_song_list(comment["text"])]


def extract_video(video) -> Video:
    return Video(
        video["channel"],
        video["channel_id"],
        video["title"],
        video["id"],
        video["webpage_url"],
        extract_timestamp(video),
        extract_comments(video["comments"])
    )


def process_video(video):
    video = extract_video(video)
    print(video)
    write_video(video)


def extract_channel_or_video(url):
    ydl_opts = {
        "getcomments": True,
        "extractor_retries": 3,
        "ignoreerrors": True,
        "extractor_args": {'youtube': {
            # 'max_comments': ['100'],
            'skip': ['dash', 'hls'],
            'comment_sort': ['top']}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        # json.dump(info, sys.stdout)
        # print()

        if info['_type'] == 'video':
            process_video(info)
        else:
            for video in info["entries"]:
                if video:
                    process_video(video)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        extract_channel_or_video(arg)
