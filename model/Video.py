from model.Comment import Comment
from datetime import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Video:
    channel: str
    channel_id: str
    title: str
    video_id: str
    webpage_url: str
    timestamp: datetime.timestamp
    comments: List[Comment]
