import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
import os
import scipy.signal as scisi
import statistics as stat


#-------------------------------------------------------------- Raspberry funksjoner --------------------------------------------------------------------------
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

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------- Fra: https://stackoverflow.com/questions/12093594/how-to-implement-band-pass-butterworth-filter-with-scipy-signal-butter     ------------------------

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

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------- Funksjoner for Lab 2 ----------------------------------------------------------------------------

def CCR(data, ADC_CH1, ADC_CH2):
    # Korrelasjon mellom kanaler
    return np.correlate(data[:, ADC_CH1], data[:, ADC_CH2], mode='full')

def find_delay(CCR_data):
    # Finner delayet på data ved å ta den største toppen av korrelasjonen. Siden Korrelasjonen ikke er null-sentrert, trekker vi fra lengden til den orginale data = CCR_data/2 = 31250 i dette tilfellet.
    # Kunne brukt len(CCR_data)/2 for å gjøre det mer generelt
    ans = np.argmax(CCR_data)
    return (ans - 31250)

def find_theta(delay_2_1, delay_3_1, delay_3_2):
    # Finner vinkelen til lydkilden basert på delays (radianer).
    delay_u = delay_2_1 + delay_3_1
    delay_b = delay_2_1 - delay_3_1 - 2 * delay_3_2
    theta = math.atan2(math.sqrt(3) * delay_u, delay_b)
    return theta

def rad_to_deg(radians):
    # Gjør om fra radianer til grader
    return radians / math.pi * 180

def plot_all(data, xlim=100):
    # Plotter alle kanalene. Forventer 5 kanaler.

    # Plot ADC Ch1 fra 0 til 100 i X-verdi
    plt.subplot(511)
    plt.xlim(0, xlim)
    plt.plot(data[:, 0])

    # Plot ADC Ch2 fra 0 til 100 i X-verdi
    plt.subplot(512)
    plt.xlim(0, xlim)
    plt.plot(data[:, 1])

    # Plot ADC Ch3 fra 0 til 100 i X-verdi
    plt.subplot(513)
    plt.xlim(0, xlim)
    plt.plot(data[:, 2])

    # Plot ADC Ch4 fra 0 til 100 i X-verdi
    plt.subplot(514)
    plt.xlim(0, xlim)
    plt.plot(data[:, 3])

    # Plot ADC Ch5 fra 0 til 100 i X-verdi
    plt.subplot(515)
    plt.xlim(0, xlim)
    plt.plot(data[:, 4])
    return True

def plot_fft(data, N, P, num):  # data, antall samples, periode, antall dataset som skal plottes
    # FFT plot of ADC Chx
    plt.figure(1)
    plt.clf()
    for i in range(num):
        powS = np.abs(np.fft.fft(data[:, i]))
        freqs = np.fft.fftfreq(N, P)
        idx = np.argsort(freqs)
        for a in idx:
            if abs(freqs[a]) < 10:
                powS[a] = 0
        plt.subplot(511 + i)
        plt.plot(freqs[idx], powS[idx])
    # Enable grid and show plots
    plt.grid()
    plt.show()
    return True

def plot_correlation(correlation):
    # Plotter korrelasjon. Null sentrert.
    x = np.array([a for a in range(-31249, 31250)])
    plt.figure(1)
    plt.plot(x, correlation)
    plt.xlim(-2000, 2000)
#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------- Funksjoner for Lab 3 ----------------------------------------------------------------------------

def velocity_radarData(data):
    # Finner hastigheten til objekt
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
    # Plot av hastighet. Ikke brukt?
    velocity = velocity_radarData(data)
    plt.figure(1)
    plt.clf()
    plt.plot(velocity)
    plt.xlabel('Step')
    plt.ylabel('Velocity')
    plt.title('Calculated velocity from radar data')

def radar_log(velocity, log_name='measurement'):
    # Lagrer hastigheten i en egen fil for å finne standardavvik senere. Input fra konsol om reell hastighet.
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
    # Leser loggen, rekner standardavvik og plotter radar data opp mot reell data, med standardavvik
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
    # Fjerner dc bidraget fra data:
    return data - dc

def plot_fft_IQ(data, N, P):
    # FFT plot for radar data, I og Q kanal
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

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------- Funksjoner for Lab 4 ----------------------------------------------------------------------------

def roi_video(input, output):
    # Kaller på den utleverte read_video_and_extract_roi filen.
    #os.system("python /home/mats/PycharmProjects/RasberryPi/read_video_and_extract_roi.py " + input + " " + output)
    os.system("python /Users/Jostein/Desktop/SensorLab/Raspberry_Pi/RasberryPi/read_video_and_extract_roi.py " + input + " " + output)

def take_video(name):
    # Funksjon som tar video, gjør det om til MP4 og kopierer filen fra Pi'en til PC.

    # Take video
    command = "ssh pi@raspberrypi.local \"sudo raspivid -t 10000 -v -o pivideo.h264\""
    os.system(command)

    # Convert to MP4
    command = "ssh pi@raspberrypi.local \"sudo MP4Box -add pivideo.h264 /home/pi/Project/data/" + name + "\""
    os.system(command)

    # Delete h264 file. Important, otherwise new videos will have problems.
    command = "ssh pi@raspberrypi.local \"sudo rm pivideo.h264 \""
    os.system(command)

    # Copy file to laptop
    command = "scp pi@169.254.210.146:/home/pi/Project/data/" + name + " /home/mats/Desktop/data"
    os.system(command)

    command = "ssh pi@raspberrypi.local \"sudo rm /home/pi/Project/data/" + name + "\""
    os.system(command)


def take_photo(name):
    # Enkel funksjon for å ta bilde. Bare brukt til å teste at kamera virker
    command = "ssh pi@raspberrypi.local \"sudo raspistill -v -o /home/pi/Project/data/" + name + "\""
    os.system(command)

    # Copy file to laptop
    command = "scp pi@169.254.210.146:/home/pi/Project/data/" + name + " /home/mats/Desktop/data"
    os.system(command)

def find_pulse(data, N, channel, P):
    # Bruker FFT for å finne pulsen
    data = data[:, channel]

    powS = np.abs(np.fft.fft(data))
    freqs = np.fft.fftfreq(N, P)
    idx = np.argsort(freqs)
    peaks = scisi.find_peaks(powS, distance=2)
    pulses = np.zeros((len(peaks[0]), 1))
    i = 0
    for a in peaks[0]:
        if a > data.shape[0]:
            break
        elif powS[a] > 0.4*np.max(powS):
            pulses[i] = freqs[a]
            i += 1

    pulses = pulses[pulses > 0]
    pulses_bpm = pulses*60

    if channel == 0:
        print('FFT Red BPM: ', pulses_bpm)
    if channel == 1:
        print('FFT Green BPM: ', pulses_bpm)
    if channel == 2:
        print('FFT Blue BPM: ', pulses_bpm)

    return pulses_bpm

def find_pulse_correlation(data, channel, fps):
    # Finne puls ved korrelasjon
    corr = np.correlate(data[:, channel], data[:, channel], mode='full') #lag korrolasjon med seg selv
    corr_peaks, corr_dict = scisi.find_peaks(corr) #finn peaks i korrolasjonen
    
    difference_corr = np.array([]) #lag array for alle forskjellene

    for n in range(1, (len(corr_peaks)-1)):
        difference_corr = np.append(difference_corr, (corr_peaks[n+1]-corr_peaks[n])) #Regn ut forskjellen mellom peaks

    corr_bpm = np.mean(60 / ((difference_corr * fps))) #Finn puls ved hjelp av gjennomsnittet av delay mellom peaks

    if channel == 0:
        print('Cross Red BPM: ', corr_bpm)
    if channel == 1:
        print('Cross Green BPM: ', corr_bpm)
    if channel == 2:
        print('Cross Blue BPM: ', corr_bpm)

    return corr_bpm


def find_SNR(data, channel, period):
    samples = data.shape[0]
    freq = np.fft.fftfreq(samples, period)
    spectrum = np.fft.fft(data, axis=0)

    roi = np.where((freq >= 0.5) & (freq < 4))
    spec_roi = spectrum[roi]
    max_freq = np.argmax(spec_roi[:, channel])

    fft_dbm = 10*np.log10(np.abs(spec_roi[:, channel]**2)/spec_roi[:, channel].shape[0])

    S = np.abs(fft_dbm[max_freq])
    N = np.abs(np.mean(fft_dbm))
    SNR = S - N

    if channel == 0:
        print('SNR Red: ', SNR)
    if channel == 1:
        print('SNR Green: ', SNR)
    if channel == 2:
        print('SNR Blue: ', SNR)

def find_standard_deviation(red_fft, green_fft, blue_fft, red_autocorr, green_autocorr, blue_autocorr):
    data_list = []


    data_list.append(red_fft)
    data_list.append(green_fft)
    data_list.append(blue_fft)
    data_list.append(red_autocorr)
    data_list.append(green_autocorr)
    data_list.append(blue_autocorr)

    print("Data_list: ", data_list)

    std = stat.stdev(data_list)
    print("STD: ", std)

