from src.backend.tracks.note import Note
from src.backend.tracks.track import Track,TrackGroup
from src.backend.tracks.channel import Channel,ChannelGroup
from enum import Enum
from mido import MidiFile
import array
from typing import List


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
        self.file_name = ""

        self.current_time = 0  # en segs
        self.started_notes = list()
        self.finished_notes = list()


    def load_midi_file(self, file_name: str) -> bool:
        print("Midi2Tracks: load_midi_file: " + file_name)
        self.file_name = file_name
        # Cargar archivo, procesar y generar tracks
        # Si el archivo no pudo cargarse o procesarse:
        #   self.state = STATE.ERROR
        # de lo contrario

        try:
            mid = MidiFile(self.file_name)
        except:
            self.state = STATE.ERROR
            return False

        self.current_time = 0  # en segs
        self.started_notes = list()
        self.finished_notes = list()

        try:
            for msg in mid:
                self.current_time += msg.time
                if not msg.is_meta:
                    if msg.type == 'note_on' and msg.velocity != 0:
                        self.__add_new_started_note(msg)
                    elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                        self.__try_to_finish_note(msg)
                elif msg.type == 'end_of_track':
                    break
            self.__finish_all_notes()
        except:
            self.state = STATE.ERROR
            return False

        self.state = STATE.LOADED
        return True

    def get_array_of_tracks(self) -> TrackGroup:
        print("Midi2Tracks: get_array_of_tracks")
        # NOTA: recordar que la list a devolver debe ser una
        # lista de "track"
        if self.state == STATE.LOADED:
            return self.tracks
        else:
            return []

    def is_valid(self) -> bool:
        return self.state == STATE.LOADED

    #def __note_number_to_frequency(self, note_number: int) -> float:  # resultado en Hz
    #    return 440*pow(2,(note_number-69)/12)

    def __add_new_started_note(self, msg):
        # Si no esta el channel en la lista
        #   Lo coloco
        #   ---
        # Si esta el channel en la lista
        #   Busco la nota
        #   Si esta la nota en la lista
        #       La finalizo
        #       ---
        #   Si no
        #       ---

        # Agrego nueva nota
        is_on_list, channel = self.__is_channel_on_list(msg.channel, self.started_notes)
        if not is_on_list:
            channel = Channel(msg.channel)
            self.started_notes.append(channel)
        else:
            is_on_channel, index = self.__is_note_on_channel(msg.note, channel)
            if is_on_channel:
                self.__finish_this_note(channel, index)
        channel.notes.append(Note(self.current_time, msg.velocity, msg.note))

        return

    def __is_note_on_channel(self,note_number: int, channel: Channel) -> list: # bool, int(index)
        """
        :param note_number: número (int) que indetifica a la nota musical
        :param channel: canal donde buscar la nota musical

        bool: encontró esa nota musical en el canal especificado?\n
        int: indice de la nota musical encontrada dentro de channel.notes
        """
        is_on_channel = False
        index = None

        for i, note in enumerate(channel.notes):
            if note.number == note_number:
                is_on_channel = True
                index = i
                break

        return [is_on_channel,index]

    # comment
    def __is_channel_on_list(self,channel_number: int, channel_group: ChannelGroup) -> list: # bool, Channel
        """
        :param channel_number: número (int) que indetifica al canal
        :param channel_group: self.started_notes o self.finished_notes

        bool: se encontró ese número de canal en algún Channel del channel_group?\n
        Channel: canal miembro del channel_group cuyo número de canal coincide con el especificado
        """
        is_on_list = False
        channel_found = Channel()

        for channel in channel_group:
            if channel.number == channel_number:
                is_on_list = True
                channel_found = channel
                break

        return [is_on_list, channel_found]

    def __finish_this_note(self, channel: Channel, source_index: int):
        note = channel.notes.pop(source_index)
        note.end = self.current_time
        self.__add_new_finished_note(channel.number, note)
        return

    def __add_new_finished_note(self, channel_number: int, note: Note):
        is_on_list, channel = self.__is_channel_on_list(channel_number, self.finished_notes)
        if not is_on_list:
            channel = Channel(channel_number)
            self.finished_notes.append(channel)
        channel.notes.append(note)
        return

    def __try_to_finish_note(self, msg):
        # si se encuentra el channel en la lista de started_notes
        #   Si se encuentra la nota en el channel.notes
        #       Finalizo esa nota
        is_on_list, channel = self.__is_channel_on_list(msg.channel, self.started_notes)
        if is_on_list:
            is_on_channel, index = self.__is_note_on_channel(msg.note, channel)
            if is_on_channel:
                self.__finish_this_note(channel, index)
        return

    def __finish_all_notes(self):
        for channel_source in self.started_notes:
            is_on_list, channel_out = self.__is_channel_on_list(channel_source.number, self.finished_notes)
            if not is_on_list:
                channel_out = Channel(channel_source.number)
                self.finished_notes.append(channel_out)
            for note in channel_source.notes:
                note.end = self.current_time
                channel_out.notes.append(note)
            channel_source.notes = []
        self.started_notes = []

        self.__generate_track_list()

        return

    def __generate_track_list(self):
        self.tracks = []
        for channel in self.finished_notes:
            self.tracks.append(channel.notes)
        return
