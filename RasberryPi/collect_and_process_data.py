import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import raspi_import
import math


import os


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

"""


# Plot ADC Ch1 from 0 to 100 in X-values

plt.subplot(511)
plt.xlim(0, 100)
plt.plot(data[:, 0])

# Plot ADC Ch2 from 0 to 100 in X-values
plt.subplot(512)
plt.xlim(0, 100)
plt.plot(data[:, 1])

# Plot ADC Ch3 from 0 to 100 in X-values
plt.subplot(513)
plt.xlim(0, 100)
plt.plot(data[:, 2])

# Plot ADC Ch4 from 0 to 100 in X-values
plt.subplot(514)
plt.xlim(0, 100)
plt.plot(data[:, 3])

# Plot ADC Ch5 from 0 to 100 in X-values
plt.subplot(515)
plt.xlim(0, 100)
plt.plot(data[:, 4])
"""
plt.plot(data[:, 0])
plt.plot(data[:, 1])
plt.plot(data[:, 2])


# Swapped data from adc 2 and 3 to get counter clockwise
correlation21 = np.correlate(data[:, 0], data[:, 2])/(31250*31250)
correlation31 = np.correlate(data[:, 0], data[:, 1])/(31250*31250)
correlation32 = np.correlate(data[:, 2], data[:, 2])/(31250*31250)

time_delay = np.array([correlation21, correlation31, correlation32])
position_mic = np.array([[0.035, 0.003], [-0.035, 0.003], [0, -0.002]])

speed_of_sound = 343
xvec = -speed_of_sound*np.linalg.pinv(position_mic).dot(time_delay)
theta = math.atan(xvec[1]/xvec[0])
theta_deg = theta*180/3.14
print(theta, " : ", theta_deg)


# N = Number of samples
# T = Period (1  / N)

N = 31250
T = 1.0/31250.0

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
plt.show()
