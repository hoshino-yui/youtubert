#!/usr/bin/env python3
import sys
import logging
import multiprocessing
from typing import List

import yt_dlp
import utils
from datetime import datetime
from model.comment import Comment
from model.video import Video


WORKERS = 16


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


def process_video(video) -> List[Video]:
    video = extract_video(video)
    if video:
        return [video]
    else:
        return []


def extract_entry(entry) -> List[Video]:
    if entry.get('_type') == 'playlist':
        videos = []
        for sub_entry in entry["entries"]:
            if sub_entry:
                videos.extend(extract_entry(sub_entry))
        return videos
    else:
        return process_video(entry)


def extract_url(url) -> List[Video]:
    ydl_opts = {
        "getcomments": True,
        "extractor_retries": 3,
        "ignoreerrors": True,
        "extractor_args": {'youtube': {
            'skip': ['dash'],
            'comment_sort': ['top']}}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        if info:
            return extract_entry(info)
        else:
            return []


def process_urls(info):
    if info["_type"] == 'playlist':
        return [video for playlist in info['entries'] for video in process_urls(playlist)]
    elif info["_type"] == 'url':
        return [info['url']]


def extract_urls(url) -> List[Video]:
    ydl_opts = {
        "extractor_retries": 3,
        "ignoreerrors": True,
        'extract_flat': True
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        urls = process_urls(info)
        with multiprocessing.Pool(processes=WORKERS) as pool:
            videos: List[List[Video]] = pool.map(extract_url, urls)
            return [v for vs in videos for v in vs]


def write_channels(videos: List[Video]):
    videos = [video for video in videos if video.comments]
    videos = sorted(videos, key=lambda v: v.timestamp)
    channel_ids = set([video.channel_id for video in videos])
    for channel_id in channel_ids:
        channel_videos = [video for video in videos if video.channel_id == channel_id]
        write_file(channel_videos)


def write_file(videos: List[Video]):
    channel_id = videos[0].channel_id
    channel_name = videos[0].channel
    filename = 'data/' + channel_name + ' - ' + channel_id + '.json'
    with utils.create_and_write_file(filename) as file:
        file.write(utils.videos_to_json_string(videos))


def main(urls):
    videos: List[Video] = [v for url in urls for v in extract_urls(url)]
    print("Processed videos: ", len(videos))
    write_channels(videos)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    args = sys.argv[1:]
    main(args)
