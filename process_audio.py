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


def normalize(vol_data):
    array = np.array(vol_data)

    range_ = array.max() - array.min()
    array = array - array.min()
    array = array / range_
    return array * 100


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
    vol_data = []
    while elapsed < seconds:
        elapsed = time.time() - start

        data = stream.read(CHUNK)

        input_vol = get_volume_db(data)
        output_vol = volume.GetMasterVolumeLevel()

        vol_data.append(input_vol - output_vol)

    vol_data = normalize(vol_data)
    return vol_data.mean()
