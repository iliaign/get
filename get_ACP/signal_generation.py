import numpy as np
import time

def get_sin_wave_amp(freq, time):
    y = np.sin(2*np.pi*freq*time)
    y=(y+1)/2
    return y

def wait_for_sampling_period(samplig_frequency):
    time.wait(samplig_frequency)
