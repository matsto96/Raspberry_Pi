import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import raspi_import
import math
import os

import drivers
# N = Number of samples
# T = Period (1  / N)
N = 31250
T = 1.0/31250.0



##os.system("ssh pi@raspberrypi.local sudo \"./Project/adc_sampler 31250 /home/pi/Project/data/adcData.bin\"")
##os.system("scp pi@169.254.210.146:/home/pi/Project/data/adcData.bin /home/mats/Desktop/data")

#drivers.run_adc("adcData.bin")"
#drivers.transfer_data_from_pi("adcData.bin")

#Sample period and data

# Import data from Pi files

sampleP, data = raspi_import.raspi_import("/home/mats/Desktop/data/adcData.bin")
print(sampleP)

# Convert 12 bit number to a voltage

data = data/4095*3.3
print(data)

drivers.plot_all(data)
plt.show()
#plt.plot(data[:, 2])

# Todo put this in drivers as a function
# Kall fila main, og organiser det slik at kvar dag er ein funksjon
correlation21 = drivers.CCR(data, 1, 0)
correlation31 = drivers.CCR(data, 2, 0)
correlation32 = drivers.CCR(data, 2, 1)


delay21 = drivers.find_delay(correlation21)
delay31 = drivers.find_delay(correlation31)
delay32 = drivers.find_delay(correlation32)

angle = drivers.find_theta(delay21, delay31, delay32)
degrees = drivers.rad_to_deg(angle)


correlation21 = np.correlate(data[:, 0], data[:, 1])
correlation31 = np.correlate(data[:, 0], data[:, 2])
correlation32 = np.correlate(data[:, 1], data[:, 2])
print(correlation21, correlation31, correlation32)
print("Angle: ", angle)
print("Degrees: ", degrees)


drivers.plot_fft(data, N, T, 5)
