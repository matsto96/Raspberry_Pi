import numpy as np
import math
import matplotlib.pyplot as plt

def CCR(data, ADC_CH1, ADC_CH2):
    return np.correlate(data[:, ADC_CH1], data[:, ADC_CH2], mode='full')

def find_delay(CCR_data):
    ans = np.where(CCR_data == np.max(CCR_data))
    return (ans[0] - 31250)

def find_theta(delay_2_1, delay_3_1, delay_3_2):
    delay = abs((delay_2_1 + delay_3_1))/(delay_2_1 - delay_3_1 - 2 * delay_3_2)
    theta = math.atan((math.sqrt(3) * delay))
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
