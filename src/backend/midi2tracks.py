from enum import Enum
import array


class STATE(Enum):
    EMPTY = 0
    LOADED = 1
    ERROR = 2

# NOTA: las funcion print se ha usado unicamente para debugueo.
# no es obligatorio conservar esas llamadas

class Midi2Tracks(object):
    def __init__(self):
        print("Midi2Tracks created!")
        self.state = STATE.EMPTY
        self.tracks = []

    def load_midi_file(self, file_name: str):
        print("Midi2Tracks: load_midi_file: " + file_name)
        # Cargar archivo, procesar y generar tracks
        # Si el archivo no pudo cargarse o procesarse:
        #   self.state = STATE.ERROR
        # de lo contrario
        self.state = STATE.LOADED

    def get_array_of_tracks(self) -> list:
        print("Midi2Tracks: get_array_of_tracks")
        # NOTA: recordar que la list a devolver debe ser una
        # lista de "track"
        if self.state == STATE.LOADED:
            return self.tracks
        else:
            return []

    def is_valid(self) -> bool:
        return self.state == STATE.LOADED
