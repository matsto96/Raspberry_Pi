import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import os
import scipy.signal as scisi


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
    lowcut = 0.5
    highcut = 3
    fs = 25.0
    for i in range(data.shape[1]):
        data[:, i] = butter_bandpass_filter(data[:, i], lowcut, highcut, fs)

    return data

def CCR(data, ADC_CH1, ADC_CH2):
    #data = data - np.mean(data, axis=0)


    return np.correlate(data[:, ADC_CH1], data[:, ADC_CH2], mode='full')

def find_delay(CCR_data):
    ans = np.argmax(CCR_data)
    return (ans - 31250)

def find_theta(delay_2_1, delay_3_1, delay_3_2):
    delay_u = delay_2_1 + delay_3_1
    delay_b = delay_2_1 - delay_3_1 - 2 * delay_3_2
    theta = math.atan2(math.sqrt(3) * delay_u, delay_b)
    return theta

def rad_to_deg(radians):
    return radians / math.pi * 180

def plot_all(data, xlim=100):
    # Plot ADC Ch1 from 0 to 100 in X-values

    plt.subplot(511)
    plt.xlim(0, xlim)
    plt.plot(data[:, 0])

    # Plot ADC Ch2 from 0 to 100 in X-values
    plt.subplot(512)
    plt.xlim(0, xlim)
    plt.plot(data[:, 1])

    # Plot ADC Ch3 from 0 to 100 in X-values
    plt.subplot(513)
    plt.xlim(0, xlim)
    plt.plot(data[:, 2])

    # Plot ADC Ch4 from 0 to 100 in X-values
    plt.subplot(514)
    plt.xlim(0, xlim)
    plt.plot(data[:, 3])

    # Plot ADC Ch5 from 0 to 100 in X-values
    plt.subplot(515)
    plt.xlim(0, xlim)
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

def velocity_radarData(data):
    N = 31250
    P = 1 / N

    powS = np.abs(np.fft.fft(data[:, 0]))
    freqs = np.fft.fftfreq(N, P)

    max_freq = freqs[np.argmax(powS)]
    while abs(max_freq) < 15:
        powS[np.argmax(powS)] = 0
        max_freq = freqs[np.argmax(powS)]

    velocity = abs(max_freq) / 160.87

    correlate = CCR(data, 0, 1)
    delay = find_delay(correlate)

    if delay < 0:
        velocity = velocity
    elif delay > 0:
        velocity = -velocity

    return velocity

def plot_radar_velocity(data):
    velocity = velocity_radarData(data)
    plt.figure(1)
    plt.clf()
    plt.plot(velocity)
    plt.xlabel('Step')
    plt.ylabel('Velocity')
    plt.title('Calculated velocity from radar data')

def radar_log(velocity, log_name='measurement'):
    f = open(log_name, 'a')

    while True:
        try:
            input1 = input("\"True\" velocity (measured by other means): ")
            break
        except ValueError:
            print("Not a valid number. Use \'.\' not \',\'.")

    f.write(str(velocity))
    f.write("\n")
    f.write(input1)
    f.write("\n")
    f.close()

def analyse_log(log_name='measurement'):
    radar_velocity = []
    real_velocity = []
    f = open(log_name, 'r')
    line = f.readline()
    while line:
        radar_velocity.append(round(float(line.strip('\n')), 3))
        line = f.readline()
        real_velocity.append(float(line.strip('\n')))
        line = f.readline()

    radar_velocity = np.asarray(radar_velocity)
    real_velocity = np.asarray(real_velocity)
    standard_avvik = np.sqrt(np.mean(np.square(radar_velocity - real_velocity)))
    print(standard_avvik)
    plt.figure(1)
    plt.clf()
    x = np.array([a for a in range(len(radar_velocity))])
    plt.errorbar(x, radar_velocity, standard_avvik, linestyle='None', marker='^', capsize=3, label='Radar')
    plt.scatter([], [])  # To get different color on radar and measured
    plt.scatter(x, real_velocity, label='Measured')
    plt.xlabel('Measurement nr.')
    plt.ylabel('Velocity in m/s')
    plt.title('Radar vs measured velocity, with standard deviation')
    plt.legend()
    plt.show()


def remove_DC(data, dc):
    return data - dc

def plot_fft_IQ(data, N, P):
    data = data[:, :]
    # FFT plot of ADC Ch1
    plt.figure(1)
    plt.clf()
    letter = 'I'
    for i in range(3):
        powS = np.abs(np.fft.fft(data[:, i]))
        freqs = np.fft.fftfreq(N, P)
        idx = np.argsort(freqs)
        plt.plot(freqs[idx], 20*np.log(powS[idx]), label=letter)
        letter = 'Q'

    # Enable grid and show plots
    plt.grid()
    plt.xlim(0, 15)
    plt.legend()
    plt.show()
    return True

def collect_cam_data(old, name):
    if not old:
        run_adc(name)
        transfer_data_from_pi(name)


def roi_video(input, output):
    os.system("python /home/mats/PycharmProjects/RasberryPi/read_video_and_extract_roi.py " + input + " " + output)

def take_video(name):
    # Take video
    command = "ssh pi@raspberrypi.local \"sudo raspivid -t 10000 -v -o pivideo.h264\""
    os.system(command)

    # Convert to MP4
    command = "ssh pi@raspberrypi.local \"sudo MP4Box -add pivideo.h264 /home/pi/Project/data/" + name + "\""
    os.system(command)

    # Delete h264 file
    command = "ssh pi@raspberrypi.local \"sudo rm pivideo.h264 \""
    os.system(command)

    # Copy file to laptop
    command = "scp pi@169.254.210.146:/home/pi/Project/data/" + name + " /home/mats/Desktop/data"
    os.system(command)

    command = "ssh pi@raspberrypi.local \"sudo rm /home/pi/Project/data/" + name + "\""
    os.system(command)


def take_photo(name):
    # Take video
    command = "ssh pi@raspberrypi.local \"sudo raspistill -v -o /home/pi/Project/data/" + name + "\""
    os.system(command)

    # Copy file to laptop
    command = "scp pi@169.254.210.146:/home/pi/Project/data/" + name + " /home/mats/Desktop/data"
    os.system(command)

def find_pulse(data, N, P):
    data = data[:, 0]

    powS = np.abs(np.fft.fft(data))
    freqs = np.fft.fftfreq(N, P)
    idx = np.argsort(freqs)
    peaks = scisi.find_peaks(powS, distance=2)
    pulses = np.zeros((len(peaks[0]), 1))
    i = 0
    for a in peaks[0]:
        if powS[a] > 0.4*np.max(powS):
            pulses[i] = freqs[a]
            i += 1

    pulses = pulses[pulses > 0]
    pulses = pulses*60
    print("Puls frekvenser, Slag i minuttet: ", pulses)

