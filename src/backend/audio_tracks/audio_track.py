from typing import List


class AudioTrack(object):
    def __init__(self):
        print("AudioTrack created!")
        self.content = []


AudioTrackGroup = List[AudioTrack]
