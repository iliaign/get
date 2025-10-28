import signal_generation as sig
import pwn_dac as pwm
import time

amplitude = 3
sig_freq = 10
sampl_freq = 100


try:
    dc = pwm.PWM_DAC(12, 500, 3.290, True)
    while True:
        try:

            fx=sig.get_triangle_wave_amplitude(sig_freq, time.time())
            dc.set_voltage(fx*amplitude)
            sig.wait_for_sampling_period(sampl_freq)
        except ValueError:
                print("Не число!\n") 

finally:
    dc.deinit()