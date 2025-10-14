import mcp4725_driver as mylp
import signal_generation as sig
import time

amplitude = 3
sig_freq = 20
sampl_freq = 500


try:
    dc = mylp.MCP4725(amplitude)

    while True:
        try:

            fx=sig.get_sin_wave_amplitude(sig_freq, time.time())
            dc.set_voltage(fx*amplitude)
            sig.wait_for_sampling_period(sampl_freq)
        except ValueError:
                print("Не число!\n") 

finally:
    dc.deinit()
