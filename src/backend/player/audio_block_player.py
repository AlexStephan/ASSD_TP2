from src.backend.audio_tracks.audio_block import AudioBlock

class AudioBlockPlayer(object):
    def __init__(self):
        print("AudioBlockPlayer created!")

    def play_audio_block(self, audio_block: AudioBlock):
        print("AudioBlockPlayer: play_audio_block")
