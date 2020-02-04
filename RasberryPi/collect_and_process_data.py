import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import raspi_import
import drivers


import os

# N = Number of samples
# T = Period (1  / N)
N = 31250
T = 1.0/31250.0


# Run script that enters pi'en and runs adc_sampler
# How: os.system("connect to raspberry-pi (ssh pi...), command to run on raspberry")
# Command to run on raspberry for adc_sampler: "run adc_sampler as sudo, number of samples, where to save the file, complete path from /home). Remember when loging in to the pi, you start in /home/pi
os.system("ssh pi@raspberrypi.local sudo \"./Project/adc_sampler 31250 /home/pi/Project/data/adcData.bin\"")
# scp - secure copy, from where to where full path
# can also be used to send files to the pi, scp my_file pi....
os.system("scp pi@169.254.210.146:/home/pi/Project/data/adcData.bin /home/mats/Desktop/data")


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



# FFT plot of ADC Ch1
powS = np.abs(np.fft.fft(data[:, 0]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)

plt.figure(2)
plt.subplot(511)
plt.plot(freqs[idx], powS[idx])

# FFT plot of ADC Ch2
plt.subplot(512)
powS = np.abs(np.fft.fft(data[:, 1]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

# FFT plot of ADC Ch3
plt.subplot(513)
powS = np.abs(np.fft.fft(data[:, 2]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

# FFT plot of ADC Ch4
plt.subplot(514)
powS = np.abs(np.fft.fft(data[:, 3]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

# FFT plot of ADC Ch5
plt.subplot(515)
powS = np.abs(np.fft.fft(data[:, 4]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

#Enable grid and show plots
plt.grid()
#plt.show()
