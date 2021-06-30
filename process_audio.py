import struct
import pyaudio
import math
import time
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_volume_db(data_):
    count = len(data_) / 2
    format_ = "%dh" % count
    shorts = struct.unpack(format_, data_)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n

    return 20 * math.log10(math.sqrt(sum_squares / count))


MAX_VOL = -15.0
MIN_VOL_SPK = -63.5
MIN_VOL_MIC = -95.0


def normalize_audio(min_, values):
    range_ = MAX_VOL - min_
    values = (values - min_) / range_
    return values * 100


def get_normalized_loudness(input_vol, output_vol):
    mic = normalize_audio(MIN_VOL_MIC, np.array(input_vol))
    spkr = normalize_audio(MIN_VOL_SPK, np.array(output_vol))
    # loudness = mic - spkr
    return mic.mean()


CHUNK = 1024


def get_loudness_last(seconds):
    # get input audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Get volume controls of laptop
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    # tell console it's listening
    print("Listening for " + str(seconds) + " seconds...")

    start = time.time()
    elapsed = 0
    mic_vol = []
    spk_vol = []
    while elapsed < seconds:
        elapsed = time.time() - start

        data = stream.read(CHUNK)

        input_vol = get_volume_db(data)
        output_vol = volume.GetMasterVolumeLevel()

        mic_vol.append(input_vol)
        spk_vol.append(output_vol)

    return get_normalized_loudness(mic_vol, spk_vol)
