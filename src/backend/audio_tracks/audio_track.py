from typing import List
from numpy import ndarray

class AudioTrack(object):
    def __init__(self):
        print("AudioTrack created!")
        self.content = None # puede ser util que sea un ndarray

AudioTrackGroup = List[AudioTrack]
