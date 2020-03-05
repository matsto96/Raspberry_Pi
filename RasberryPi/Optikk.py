import drivers
import raspi_import
import matplotlib.pyplot as plt
import numpy as np
import scipy
"""
path = "/home/mats/Desktop/data/"
file_name = "video.bin"


redo = False
plot_data = False
print_stats = True
roi = False


data = drivers.collect_cam_data(redo, path + file_name)
pros_data = drivers.process_cam_data(data)


if plot_data:
    drivers.plot_cam()

if print_stats:
    drivers.print_stats()

if roi:
    input_video_path = path + file_name
    output_data_path = path + "roi"

    drivers.roi_video(input_video_path, output_data_path)

"""
"""
raspivid -t 30000 -w 640 -h 480 -fps 25 -b 1200000 -p 0,0,640,480 -o pivideo.h264
MP4Box -add pivideo.h264 pivideo.mp4
"""
file_name = "/home/mats/Desktop/data/video_data2"

#drivers.take_video("myvideo.mp4")
#drivers.roi_video("/home/mats/Desktop/data/myvideo.mp4", file_name)


data = np.loadtxt(file_name)
data = data - np.mean(data, axis=0)

data = drivers.filter_data(data)

plt.plot(data[:, 0], label='First chan')
plt.plot(data[:, 1], label='Second chan')
plt.plot(data[:, 2], label='Third chan')
plt.legend()
plt.show()

drivers.plot_fft_IQ(data[50:, :], 243, 0.04)

drivers.find_pulse(data[50:, :], 243, 0.04)