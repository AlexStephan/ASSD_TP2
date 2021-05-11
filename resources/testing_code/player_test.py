import sounddevice as sd
import numpy as np

def callback_sound_test(outdata: np.ndarray, frames: int, time, status):
    outdata.fill(0)
    print(f"frames = {frames}")
