import utils
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

    def generate_filename(self):
        folder_name = f"youtube/{utils.clean_filename(self.channel)} - {self.channel_id}"
        filename = f"{folder_name}/{utils.clean_filename(self.title)} - {self.video_id}.md"
        return filename

    def generate_markdown_lines(self):
        if len(self.comments) == 0:
            return None

        lines = [f"# {self.title}",
                 f"## {self.channel}",
                 f"### {self.timestamp}",
                 f"{self.webpage_url}"]

        for comment in self.comments:
            lines.append(f"#### {comment.id}")
            lines.extend(comment.text_lines())
            lines.append('')
        return lines
