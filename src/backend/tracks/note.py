class Note(object):
    def __init__(self, start=None, end=None, velocity=None, frequency=None):
        print("Note created!")
        self.start = start
        self.end = end
        self.velocity = velocity
        self.frequency = frequency
