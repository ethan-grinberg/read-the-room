import struct
import pyaudio
import math
import time
import numpy as np

CHUNK = 1024
MAX_VOL = 90


class AudioProcessor:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.MIN_RMS = self.calibrate_mic()

    def calibrate_mic(self):
        stream = self.p.open(format=pyaudio.paInt16,
                             channels=2,
                             rate=44100,
                             input=True,
                             frames_per_buffer=CHUNK)

        # get min rms value
        data = stream.read(CHUNK)
        min_rms = self.get_volume_rms(data)

        # stop stream
        stream.stop_stream()
        stream.close()
        return min_rms

    @staticmethod
    def get_volume_rms(data_):
        count = len(data_) / 2
        format_ = "%dh" % count
        shorts = struct.unpack(format_, data_)
        sum_squares = 0.0
        for sample in shorts:
            n = sample * (1.0 / 32768)
            sum_squares += n * n

        return math.sqrt(sum_squares / count)

    def convert_to_db(self, rms):
        return 20 * math.log10(rms / self.MIN_RMS)

    @staticmethod
    def get_normalized_loudness(input_vol):
        # TODO decide if it should be median or mean
        # TODO maybe don't normalize
        mean = np.array(input_vol).mean()
        return (mean / MAX_VOL) * 100

    def get_loudness_last(self, seconds):
        stream = self.p.open(format=pyaudio.paInt16,
                             channels=2,
                             rate=44100,
                             input=True,
                             frames_per_buffer=CHUNK)

        # tell console it's listening
        print("Listening for " + str(seconds) + " seconds...")

        start = time.time()
        elapsed = 0
        mic_vol = []
        while elapsed < seconds:
            elapsed = time.time() - start

            data = stream.read(CHUNK)
            input_vol = self.convert_to_db(self.get_volume_rms(data))
            mic_vol.append(input_vol)

        # stop stream
        stream.stop_stream()
        stream.close()

        # don't include the first couple values as the mic wakes up
        return self.get_normalized_loudness(mic_vol[3:])

