import math
import librosa
import numpy as np
from scipy import stats
import pyloudnorm as pyln

# CHUNK = 1024
# SR = 44100
# frame_length = 2048
# hop_length = 512

trumpet, sr = librosa.load(librosa.ex("fishin"), offset=95, duration=10)
brahms, sr2 = librosa.load(librosa.ex("fishin"), offset=90, duration=10)
talking, sr4 = librosa.load("Data/talking.wav", offset=10, duration=10)
party, sr3 = librosa.load("Data/party.wav", offset=5, duration=10)

trumpet_spec = np.abs(librosa.stft(trumpet))
brahms_spec = np.abs(librosa.stft(brahms))
party_spec = np.abs(librosa.stft(party))
talking_spec = np.abs(librosa.stft(talking))


def get_zscore(array1, array2):
    return (array1.mean() - array2.mean()) / math.sqrt(array1.std() + array2.std())


def get_diff_mean(array1, array2):
    diffs = array1 - array2
    return diffs.mean()


# measure the loudness first
meter = pyln.Meter(sr4) # create BS.1770 meter
loudness = meter.integrated_loudness(party)
print(loudness)

# print(librosa.amplitude_to_db(trumpet, amin=trumpet.min()))