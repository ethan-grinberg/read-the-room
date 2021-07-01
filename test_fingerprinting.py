import math

import librosa
import time
import pyaudio
import struct
import numpy as np

CHUNK = 1024
SR = 44100
frame_length = 2048
hop_length = 512


# def get_stft_from_mic():
#     p = pyaudio.PyAudio()
#     stream = p.open(format=pyaudio.paInt16,
#                     channels=2,
#                     rate=44100,
#                     input=True,
#                     frames_per_buffer=frame_length)
#
#     start = time.time()
#     elapsed = 0
#     chromas = np.array([])
#     while elapsed < 5:
#         elapsed = time.time() - start
#
#         data = stream.read(frame_length)
#         count = len(data) / 2
#         format_ = "%dh" % count
#         shorts = struct.unpack(format_, data)
#         array = np.array(shorts)
#         array = array * 1.0
#         block = librosa.feature.chroma_stft(array)
#         np.append(chromas, block)
#
#     return chromas
#
#
#
# chromas1 = get_stft_from_mic()
# chromas2 = get_stft_from_mic()
#
#

trumpet, sr1 = librosa.load(librosa.ex("fishin"), offset=95, duration=10)
# brahms, sr2 = librosa.load(librosa.ex("fishin"), offset=90, duration=5.0)
talking, sr4 = librosa.load("Data/talking.wav", offset=10, duration=10)
party, sr3 = librosa.load("Data/party.wav", offset=5, duration=10)

trumpet_spec = np.abs(librosa.stft(trumpet))
# brahms_spec = np.abs(librosa.stft(brahms))
party_spec = np.abs(librosa.stft(party))
talking_spec = np.abs(librosa.stft(talking))


def get_zscore(array1, array2):
    return (array1.mean() - array2.mean()) / math.sqrt(array1.std() + array2.std())


def get_diff_mean(array1, array2):
    diffs = array1 - array2
    return diffs.mean()


print(100 * (1 - abs(get_diff_mean(trumpet_spec, party_spec))))
print(100 * (1 - abs(get_diff_mean(talking_spec, party_spec))))

# print(str(get_zscore(trumpet_spec, brahms_spec)))
