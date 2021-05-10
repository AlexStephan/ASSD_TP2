from src.backend.audio_tracks.audio_track import AudioTrack


class AudioSaver(object):
    def __init__(self):
        print("AudioSaver created!")

    def save_wav_file(self, audio_track: AudioTrack, filename: str) -> bool:
        # Intentar guardar el track de audio como .wav
        # Si salio bien, devolver True, sino, devolver False
        return True
