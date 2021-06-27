import struct
import pyaudio
import math

def rms(data_):
    count = len(data_) / 2
    format_ = "%dh" % count
    shorts = struct.unpack(format_, data_)
    sum_squares = 0.0
    for sample in shorts:
        n = sample * (1.0 / 32768)
        sum_squares += n * n

    return math.sqrt(sum_squares / count)


CHUNK = 1024
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=44100,
                input=True,
                frames_per_buffer=CHUNK)
while True:
    data = stream.read(CHUNK)
    conversion = rms(data) * 4
    if conversion > 1:
        conversion = 1

    print((round(conversion, 1)))
