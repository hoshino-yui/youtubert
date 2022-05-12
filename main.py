#!/usr/bin/env python3
import json
import re
import sys

import yt_dlp
from datetime import datetime
from pathlib import Path
from model.Comment import Comment
from model.Video import Video
from typing import List


def comment_is_song_list(text):
    return "\n" in text and re.search(r"\d:\d\d", text)


def write_video(video: Video):
    try:
        write_file(video.channel,
                   video.channel_id,
                   video.title,
                   video.video_id,
                   video.webpage_url,
                   video.timestamp,
                   video.comments)
    except IOError as e:
        print(f"Failed to write video {video.video_id} - {video.title}")
        print(e)


def write_file(channel, channel_id, title, video_id, webpage_url, timestamp, comments: List[Comment]):
    if len(comments) == 0:
        return

    channel = channel.replace("/", "")
    title = title.replace("/", "")
    folder_name = f"youtube/{channel} - {channel_id}"
    filename = f"{folder_name}/{title} - {video_id}.md"
    Path(folder_name).mkdir(parents=True, exist_ok=True)
    with Path(filename).open('w') as file:
        file.write(f"## {title}\n")
        file.write(f"### {timestamp}\n")
        file.write(f"{webpage_url}\n")
        for comment in comments:
            file.write(f"#### {comment.id}\n")
            file.write(f"{comment.text_markdown()}\n")
            file.write("\n")


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
    return [extract_comment(comment) for comment in comments if comment_is_song_list(comment["text"])]


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
    print()
    print(video)
    write_video(video)


def extract_channel_or_video(url):
    ydl_opts = {
        "getcomments": True,
        "extractor_retries": 3,
        "ignoreerrors": True,
        "extractor_args": {'youtube': {
            # 'max_comments': ['100'],
            'comment_sort': ['top']}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        # json.dump(info, sys.stdout)

        if info['_type'] == 'video':
            process_video(info)
        else:
            for video in filter(None, info["entries"]):
                process_video(video)


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        extract_channel_or_video(arg)
