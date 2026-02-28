#!/usr/bin/env python3
import json
import sys
import logging
import time
from typing import List

import yt_dlp

import data_reader
import utils
from model.channel import Channel
from model.channels import Channels
from model.video import Video
from model.video_simple import VideoSimple
from video_mapper import process_video
from video_url_fetcher import fetch_videos


def extract_entry(entry) -> List[Video]:
    if entry.get('_type') == 'playlist':
        videos = []
        for sub_entry in entry["entries"]:
            if sub_entry:
                videos.extend(extract_entry(sub_entry))
        return videos
    else:
        return process_video(entry)


def extract_url(video: VideoSimple) -> List[Video]:
    ydl_opts = {
        # "debug_printtraffic": True,
        "getcomments": True,
        "extractor_retries": 2,
        "ignoreerrors": True,
        'skip_download': True,
        # 'cookiesfrombrowser': ('firefox', ),
        "extractor_args": {'youtube': {
            'player_client': ['android'],
            'player_skip': ['configs', 'js', 'initial_data'],
            'skip': ['https', 'dash', 'hls'],
            'comment_sort': ['top']
        }}
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video.webpage_url, download=False)
        info = ydl.sanitize_info(info)
        # print(json.dumps(info))
        if info:
            print("Extracted something?")
            entry = extract_entry(info)
            if entry:
                if len(entry) == 1:
                    print("Extracted a thing!")
                else:
                    print("Extracted {} things!".format(len(entry)))
            else:
                print("Extracted no thing!")
            return entry
        else:
            print("Extracted nothing!")
    return []


def extract_urls(data: Channels, url: str, since) -> List[Video]:
    video_list = fetch_videos(data, url, since)

    start = time.time()
    videos: List[List[Video]] = utils.parallel_process(extract_url, video_list)
    end = time.time()
    length = end - start
    print("It took", length, "seconds!")
    return [v for vs in videos for v in vs]


def write_channels(data: Channels, videos: List[Video]):
    data.append_videos(videos)
    for channel in data.channels:
        write_file(channel)


def write_file(channel: Channel):
    filename = 'data/' + channel.channel + ' - ' + channel.channel_id + '.json'
    with utils.create_and_write_file(filename) as file:
        file.write(utils.videos_to_json_string(channel.videos))


def main(days_ago, urls):
    now = utils.now()
    since = utils.minus_days(now, days_ago)

    data: Channels = data_reader.read_data_files()
    videos: List[Video] = [v for url in urls for v in extract_urls(data, url, since)]
    print("Processed videos: ", len(videos))
    write_channels(data, videos)


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    days_ago_arg = sys.argv[1]
    url_args = sys.argv[2:]
    main(days_ago_arg, url_args)
