from src.backend.tracks.note import Note
from typing import List

# NOTA: las funcion print se ha usado unicamente para debugueo.
# no es obligatorio conservar esas llamadas


class Track(object):
    def __init__(self):
        print("Track created!")
        self.notes = []     # Esto deberia llenarse con objetos tipo "Note"
        #                     Cómo? no lo se, capaz con funciones mismas
        #                     de Track, quisas con funciones de midi2tracks
        #                     lo decide quien se encargue de esto.


TrackGroup = List[Track]

