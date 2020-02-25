import drivers
import raspi_import
import matplotlib.pyplot as plt


import numpy as np

path = "/home/mats/Desktop/data/"
file_name = "radar"
file_end = ".bin"

N = 31250
P = 1 / N

# Only this variables need to be changed while running
get_data = False            # True: run the program on the PI, to get a sample      # False: calculate the standard deviation for the measurements done so far (from log)
save_file = 'car_measurement'   # Default is 'measurement'       # If you want to have a separate dataset.

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

    velocity = drivers.velocity_radarData(data)
    print("Velocity: ", velocity)
    drivers.plot_fft_IQ(data, N, P)

    drivers.radar_log(velocity, save_file)
else:
    drivers.analyse_log(save_file)

"""
I: ADC1
Q: ADC2

"""

"""
# For getting multiple samples after each other
num_runs = 1  #How many runs needed#
for num_run in range(num_runs):
    drivers.run_adc(file_name + str(num_run) + file_end)
    drivers.transfer_data_from_pi(file_name + str(num_run) + file_end)
    samplePeriod, data = raspi_import.raspi_import(path + file_name + file_end)
"""