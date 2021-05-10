from src.backend.audio_tracks.audio_track import AudioTrack


class AudioTrack2Spectrum(object):
    def __init__(self):
        print("AudioTrack2Spectrum created!")

    def get_spectrum(self, audio_track:AudioTrack, config: list):
        print("AudioTrack2Spectrum get_spectrum")
