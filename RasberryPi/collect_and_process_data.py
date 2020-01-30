import numpy as np
from scipy import fft
import matplotlib.pyplot as plt
import raspi_import


import os


# Run script that enters pi'en and runs adc_sampler
os.system("ssh pi@raspberrypi.local sudo \"./Project/adc_sampler 31250 /home/pi/Project/data/testData.bin\"")
os.system("scp pi@169.254.210.146:/home/pi/Project/data/adcData.bin /home/mats/Desktop/data")

sampleP, data = raspi_import.raspi_import("/home/mats/Desktop/data/adcData.bin")
print(sampleP)
data = data/4095*3.3
print(data)
plt.subplot(511)
plt.xlim(0, 100)
plt.plot(data[:, 0])
plt.subplot(512)
plt.xlim(0, 100)
plt.plot(data[:, 1])
plt.subplot(513)
plt.xlim(0, 100)
plt.plot(data[:, 2])
plt.subplot(514)
plt.xlim(0, 100)
plt.plot(data[:, 3])
plt.subplot(515)
plt.xlim(0, 100)
plt.plot(data[:, 4])



N = 31250
T = 1.0/31250.0

powS = np.abs(np.fft.fft(data[:, 0]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)

plt.figure(2)
plt.subplot(511)
plt.plot(freqs[idx], powS[idx])

plt.subplot(512)
powS = np.abs(np.fft.fft(data[:, 1]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

plt.subplot(513)
powS = np.abs(np.fft.fft(data[:, 2]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

plt.subplot(514)
powS = np.abs(np.fft.fft(data[:, 3]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])

plt.subplot(515)
powS = np.abs(np.fft.fft(data[:, 4]))
freqs = np.fft.fftfreq(N, T)
idx = np.argsort(freqs)
plt.plot(freqs[idx], powS[idx])
plt.grid()
plt.show()
