import struct
import pyaudio
import math
import time
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

CHUNK = 1024


def get_volume_db(data_):
    count = len(data_) / 2
    format_ = "%dh" % count
    shorts = struct.unpack(format_, data_)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n

    return 20 * math.log10(math.sqrt(sum_squares / count))


def normalize_audio(values, calibration):
    return 100 * ((values - calibration) / -calibration)


def get_normalized_loudness(input_vol):
    # bug, only gets absolute min when mic turns on for first time
    mic = normalize_audio(np.array(input_vol), input_vol[0])
    return mic.mean()


def get_loudness_last(seconds):
    # get input audio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK)

    # Get volume controls of laptop
    # devices = AudioUtilities.GetSpeakers()
    # interface = devices.Activate(
    #     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    # volume = cast(interface, POINTER(IAudioEndpointVolume))

    # tell console it's listening
    print("Listening for " + str(seconds) + " seconds...")

    start = time.time()
    elapsed = 0
    mic_vol = []
    while elapsed < seconds:
        elapsed = time.time() - start

        data = stream.read(CHUNK)

        input_vol = get_volume_db(data)

        mic_vol.append(input_vol)

    print(mic_vol)
    return get_normalized_loudness(mic_vol)


print(get_loudness_last(10))
