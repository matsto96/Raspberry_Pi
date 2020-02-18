import drivers
import raspi_import
import matplotlib.pyplot as plt
import math

import numpy as np
carrier_freq = 24.125*1000000000   # 24.125 GHz

path = "/home/mats/Desktop/data/"
file_name = "radar"
file_end = ".bin"

"""
# For getting multiple samples after each other
num_runs = 1  #How many runs needed#
for num_run in range(num_runs):
    drivers.run_adc(file_name + str(num_run) + file_end)
    drivers.transfer_data_from_pi(file_name + str(num_run) + file_end)
"""
get_data = True
if get_data:
    drivers.run_adc(file_name + file_end)
    drivers.transfer_data_from_pi(file_name + file_end)
    dc = 1.65
    samplePeriod, data = raspi_import.raspi_import(path + file_name + file_end)
    data = data/4095*3.3
    data = drivers.remove_DC(data, dc)

    drivers.plot_all(data, 10000)
    plt.show()

    #drivers.plot_radar_velocity(data[:, 0:2])
    #plt.show()

    N = 31250
    P = 1/N

    powS = np.abs(np.fft.fft(data[:, 0]))
    freqs = np.fft.fftfreq(N, P)

    max_freq = freqs[np.argmax(powS)]
    velocity = abs(max_freq) / 160.87

    correlate = drivers.CCR(data, 0, 1)
    delay = drivers.find_delay(correlate)

    if delay < 0:
        velocity = velocity
    elif delay > 0:
        velocity = -velocity
    print("Vel: ", velocity)

    drivers.radar_log(velocity)
else:
    drivers.analyse_log()

"""
I: ADC1
Q: ADC2

"""