#!/usr/bin/env python3
from datetime import datetime, UTC
from typing import List

from model.comment import Comment
import utils
from model.video import Video
from model.video_simple import VideoSimple


def extract_timestamp(video):
    date_format = "%Y%m%d"
    if "release_timestamp" in video and video["release_timestamp"]:
        derived_timestamp = datetime.fromtimestamp(video["release_timestamp"], UTC)
        print("Extracting timestamp from release_timestamp", video["release_timestamp"], derived_timestamp)
        return derived_timestamp
    elif "timestamp" in video and video["timestamp"]:
        derived_timestamp = datetime.fromtimestamp(video["timestamp"], UTC)
        print("Extracting timestamp from timestamp", video["timestamp"], derived_timestamp)
        return derived_timestamp
    elif "upload_date" in video and video["upload_date"]:
        derived_timestamp = datetime.strptime(video["upload_date"], date_format).replace(tzinfo=UTC)
        print("Extracting timestamp from upload_date", video["upload_date"], derived_timestamp)
        return derived_timestamp
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


def extract_video_simple(video) -> [VideoSimple]:
    if "channel" not in video:
        print("Skipping video without channel", video)
        return None
    timestamp = extract_timestamp(video)
    if not timestamp:
        print("Skipping video without timestamp", video)
        return None
    url = video["url"] if "url" in video else video["webpage_url"] if "webpage_url" in video else video["original_url"]
    return VideoSimple(
        video["channel"],
        video["channel_id"],
        video["title"],
        video["id"],
        url,
        timestamp
    )


def process_video_simple(video) -> List[VideoSimple]:
    try:
        video_simple = extract_video_simple(video)
        if video_simple:
            return [video_simple]
        else:
            return []
    except Exception as e:
        print("Exception processing video simple", video, e)
        raise Exception("Exception processing video simple")


def process_video(video) -> List[Video]:
    try:
        video = extract_video(video)
        if video:
            return [video]
        else:
            return []
    except Exception as e:
        print("Exception processing video", video, e)
        raise Exception("Exception processing video")

