import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import os

def butter_bandpass(lowcut, highcut, fs, order):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def filter_data(data):
    lowcut = 20.0
    highcut = 1020.0
    fs = 31250.0
    for i in range(data.shape[1]):
        data[:, i] = butter_bandpass_filter(data[:, i], lowcut, highcut, fs)

    return data

def CCR(data, ADC_CH1, ADC_CH2):
    #data = data - np.mean(data, axis=0)


    return np.correlate(data[:, ADC_CH1], data[:, ADC_CH2], mode='full')

def find_delay(CCR_data):
    ans = np.argmax(CCR_data)
    return (ans - 31250 + 100)

def find_theta(delay_2_1, delay_3_1, delay_3_2):
    delay_u = delay_2_1 + delay_3_1
    delay_b = delay_2_1 - delay_3_1 - 2 * delay_3_2
    theta = math.atan2(math.sqrt(3) * delay_u, delay_b)
    return theta

def rad_to_deg(radians):
    return radians / math.pi * 180

def plot_all(data):
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
    return True

def plot_fft(data, N, P, num):  # data, number of samples, periode, how many datasets to plot
    # FFT plot of ADC Ch1
    plt.figure(1)
    plt.clf()
    for i in range(num):
        powS = np.abs(np.fft.fft(data[:, i]))
        freqs = np.fft.fftfreq(N, P)
        idx = np.argsort(freqs)
        plt.subplot(511 + i)
        plt.plot(freqs[idx], powS[idx])

    # Enable grid and show plots
    plt.grid()
    plt.show()
    return True

def run_adc(save_file_name):
    # Run script that enters pi'en and runs adc_sampler
    # How: os.system("connect to raspberry-pi (ssh pi...), command to run on raspberry")
    # Command to run on raspberry for adc_sampler: "run adc_sampler as sudo, number of samples, where to save the file, complete path from /home). Remember when loging in to the pi, you start in /home/pi
    command = "ssh pi@raspberrypi.local \"sudo ./Project/adc_sampler 31250 /home/pi/Project/data/" + save_file_name + "\""
    os.system(command)

def transfer_data_from_pi(file_name):
    # scp - secure copy, from where to where full path
    # can also be used to send files to the pi, scp my_file pi....
    command = "scp pi@169.254.210.146:/home/pi/Project/data/" + file_name + " /home/mats/Desktop/data"
    os.system(command)

def plot_correlation(correlation):
    x = np.array([a for a in range(-31249 + 100, 31250 - 100)])
    plt.figure(1)
    plt.plot(x, correlation)
    plt.xlim(-2000, 2000)