from dataclasses import dataclass
from typing import List

from model.channel import Channel
from model.video import Video


@dataclass
class Channels:
    channels: List[Channel]

    def contains_video(self, url: str) -> bool:
        for channel in self.channels:
            if channel.contains_video(url):
                return True
        return False

    def get_or_create_channel(self, channel: str, channel_id: str) -> Channel:
        for c in self.channels:
            if c.channel_id == channel_id:
                return c
        new_channel = Channel(channel, channel_id, [])
        self.channels.append(new_channel)
        return new_channel

    def append_videos(self, videos: List[Video]):
        videos = [video for video in videos if video.comments]
        channel_ids = set([video.channel_id for video in videos])
        for channel_id in channel_ids:
            channel_videos = [video for video in videos if video.channel_id == channel_id]
            channel_name = channel_videos[0].channel
            self.get_or_create_channel(channel_name, channel_id).append_videos(channel_videos)
