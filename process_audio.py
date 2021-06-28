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


CHUNK = 1024
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

start = time.time()
elapsed = 0
vol_last_5 = []
while elapsed < 5:
    elapsed = time.time() - start

    data = stream.read(CHUNK)

    input_vol = get_volume_db(data)
    output_vol = volume.GetMasterVolumeLevel()

    vol_last_5.append(input_vol - output_vol)

array = np.array(vol_last_5)

range_ = array.max() - array.min()
array = array - array.min()
array = array / range_

print(array.mean())
print(array)
