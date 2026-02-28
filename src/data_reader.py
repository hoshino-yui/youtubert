import json
import os
from typing import List

from model.channel import Channel
from model.channels import Channels
from model.video import Video


def list_files() -> List[str]:
    filenames = os.listdir("data")
    filenames = [f for f in filenames if f.endswith(".json")]
    return filenames


def parse_filename(filename: str):
    channel, channel_id = filename.rstrip(".json").rsplit(" - ", maxsplit=1)
    return channel, channel_id


def read_file(filename: str) -> Channel:
    channel, channel_id = parse_filename(filename)

    with open("data/" + filename, "r") as f:
        data = f.read()
        loaded = json.loads(data)
        videos = [Video(**v) for v in loaded]
        c = Channel(channel, channel_id, videos)

        for video in c.videos:
            video.fix_timestamp()

        return c


def read_data_files() -> Channels:
    filenames = list_files()
    channels = Channels([read_file(filename) for filename in filenames])
    return channels


def main():
    filenames = list_files()
    channels = {}
    for filename in filenames:
        channel, channel_id = parse_filename(filename)
        channels[channel_id] = channel
    print(json.dumps(channels, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
