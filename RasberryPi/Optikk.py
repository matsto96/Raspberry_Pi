import drivers
import matplotlib.pyplot as plt
import numpy as np

file_name = "/home/mats/Desktop/data/refldata10"
video_name = "refl_vid10.mp4"

#drivers.take_video(video_name)
drivers.roi_video("/home/mats/Desktop/data/Refleksjon_video/" + video_name, file_name)  #VideoPi/myCovideo9.mp4    #


data = np.loadtxt(file_name)
data = data - np.mean(data, axis=0)
data = drivers.filter_data(data)


plt.plot(data[:, 0], label='First chan')
plt.plot(data[:, 1], label='Second chan')
plt.plot(data[:, 2], label='Third chan')
plt.legend()
#plt.savefig("/home/mats/Desktop/data/name_file.png")
plt.show()

drivers.plot_fft_IQ(data[50:, :], data[50:, :].shape[0], 0.04)

drivers.find_pulse(data[50:, :], data[50:, :].shape[0], 0.04)

drivers.find_pulse_correlation(data[50:, :], 0.04)

