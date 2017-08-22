# coding: utf-8
import numpy as np
import scipy.io.wavfile
import os
from itertools import chain

def walsh_transform(x):
    def flatten(l):
        return list(chain.from_iterable(l))

    n = len(x)
    if(n == 1):
        return x
    else:
        x0 = walsh_transform( [(a+b) for a, b in zip(x, x[n/2:])] )
        x1 = walsh_transform( [(a-b) for a, b,in zip(x, x[n/2:])] )
        return flatten(zip(x0, x1))

if __name__ == '__main__':
    resolution = 2**16
    max_n = 2**10
    samplerate = 44100
    gain = (2**14)

    os.mkdir("wav")

    for n in xrange(max_n):
        # translate to gray code
        g = n ^ (n>>1)

        # walsh spectrum
        spectrum = np.zeros((resolution,))
        spectrum[g] = 1

        # inverse transform
        write_frames = np.array( walsh_transform(spectrum) )*gain

        # write
        scipy.io.wavfile.write(
            'wav/walsh_%04d_%d.wav' % (n,resolution),
            samplerate,
            write_frames.astype(np.int16))
