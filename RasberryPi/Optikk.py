import drivers
import matplotlib.pyplot as plt
import numpy as np
import math


file_name = "/Users/Jostein/Desktop/SensorLab/Video/Videodata"
video_name = "refl_vid10.mp4"

#drivers.take_video(video_name)
drivers.roi_video("/Users/Jostein/Desktop/SensorLab/Video/Refleksjon_video/" + video_name, file_name)  #VideoPi/myCovideo9.mp4    #


data = np.loadtxt(file_name)
data = data - np.mean(data, axis=0)
data = drivers.filter_data(data)


plt.plot(data[:, 0], label='Red channel', color='red')
plt.plot(data[:, 1], label='Green channel', color='green')
plt.plot(data[:, 2], label='Blue channel', color='blue')
plt.legend()
#plt.savefig("/home/mats/Desktop/data/name_file.png")
plt.show()

#drivers.plot_fft_IQ(data[50:, :], data[50:, :].shape[0], 0.04)

red_fft_bpm = drivers.find_pulse(data[50:, :], data[50:, :].shape[0], 0, 0.04)
green_fft_bpm = drivers.find_pulse(data[50:, :], data[50:, :].shape[0], 1, 0.04)
blue_fft_bpm = drivers.find_pulse(data[50:, :], data[50:, :].shape[0], 2, 0.04)

drivers.find_SNR(data[50:, :], 0, 0.04)
drivers.find_SNR(data[50:, :], 1, 0.04)
drivers.find_SNR(data[50:, :], 2, 0.04)

red_autocorr_bpm = drivers.find_pulse_correlation(data[50:, :], 0, 0.04)
green_autocorr_bpm = drivers.find_pulse_correlation(data[50:, :], 1, 0.04)
blue_autocorr_bpm = drivers.find_pulse_correlation(data[50:, :], 2, 0.04)

