from datetime import datetime, UTC
from dataclasses import dataclass


@dataclass
class VideoSimple:
    title: str
    video_id: str
    webpage_url: str
    timestamp: datetime.timestamp

    def fix_timestamp(self):
        if type(self.timestamp) is str:
            self.timestamp = datetime.fromisoformat(self.timestamp)
