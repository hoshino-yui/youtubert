from dataclasses import dataclass
from typing import List

from model.video import Video


@dataclass
class Channel:
    channel: str
    channel_id: str
    videos: List[Video]

    def contains_video(self, url: str) -> bool:
        for video in self.videos:
            if video.webpage_url == url:
                return True
        return False

    def sort_videos(self):
        self.videos.sort(key=lambda video: str(video.timestamp))

    def append_videos(self, videos: List[Video]):
        self.videos.extend(videos)
        self.sort_videos()
