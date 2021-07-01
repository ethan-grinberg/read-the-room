import librosa
import time
import pyaudio
import struct
import numpy as np

CHUNK = 1024
SR = 44100
frame_length = 2048
hop_length = 512


def get_stft_from_mic():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=frame_length)

    start = time.time()
    elapsed = 0
    chromas = np.array([])
    while elapsed < 5:
        elapsed = time.time() - start

        data = stream.read(frame_length)
        count = len(data) / 2
        format_ = "%dh" % count
        shorts = struct.unpack(format_, data)
        array = np.array(shorts)
        array = array * 1.0
        block = librosa.feature.chroma_stft(array)
        np.append(chromas, block)

    return chromas



chromas1 = get_stft_from_mic()
chromas2 = get_stft_from_mic()

diffs = chromas1 - chromas2
similarity_coefficient = np.sum(diffs)
print(similarity_coefficient)
