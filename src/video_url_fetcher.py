#!/usr/bin/env python3
import json
from typing import List
import yt_dlp

import video_mapper
from model.channels import Channels
from model.video_simple import VideoSimple


def process_urls(info) -> List[VideoSimple]:
    if info["_type"] == 'playlist':
        return [video for playlist in info['entries'] for video in process_urls(playlist)]
    elif info["_type"] == 'url':
        return video_mapper.process_video_simple(info)
    elif info["_type"] == 'video':
        return video_mapper.process_video_simple(info)
    else:
        raise RuntimeError(f"Unsupported type {info['_type']}")


def skip_existing(data, videos: List[VideoSimple]) -> List[VideoSimple]:
    filtered_videos = []
    skipped = []
    for v in videos:
        if data.contains_video(v.webpage_url):
            skipped.append(v.webpage_url)
            print("skipping existing:", v.webpage_url)
        else:
            filtered_videos.append(v)
    print("skipped existing:", len(skipped))
    return filtered_videos


def filter_timestamp(videos: List[VideoSimple], start_timestamp) -> List[VideoSimple]:
    filtered_videos = []
    skipped = []
    for v in videos:
        if v.timestamp and v.timestamp < start_timestamp:
            skipped.append(v.webpage_url)
            print(f"skipping due to timestamp ({v.timestamp} < {start_timestamp}):", v.webpage_url)
        else:
            filtered_videos.append(v)
    print("skipped due to timestamp:", len(skipped))
    return filtered_videos


def fetch_videos(data: Channels, url: str, since) -> List[VideoSimple]:
    ydl_opts = {
        # "debug_printtraffic": True,
        "extractor_retries": 3,
        "ignoreerrors": True,
        "extract_flat": True,
        "extractor_args": {
            'youtubetab': {
                'approximate_date': 'True'
            }
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        info = ydl.sanitize_info(info)
        videos = process_urls(info)
        videos = skip_existing(data, videos)
        videos = filter_timestamp(videos, since)
        # urls = random.sample(urls, 20)
        # print(json.dumps(info))
        print("Videos to process: ", len(videos))
        return videos
