from typing import List
from src.backend.tracks.track import Track


class Channel(object):
    def __init__(self, i: int = None, notes: Track = None):
        self.number = i  # numero de canal
        if notes is None:
            self.notes = []
        else:
            self.notes = notes


ChannelGroup = List[Channel]
