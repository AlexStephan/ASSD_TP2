class Note(object):
    def __init__(self, start=None, velocity=None, number=None, end=None):
        print("Note created!")
        self.start = start          # segs
        self.velocity = velocity    # amplitud
        self.number = number
        if self.number is not None:
            self.frequency = 440*pow(2,(self.number-69)/12)
        else:
            self.frequency = None   # Hz

        self.end = end              # segs
