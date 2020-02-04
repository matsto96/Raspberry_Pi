import numpy as np

def CCR(data, ADC_CH1, ADC_CH2):
    return np.correlate(data[:, ADC_CH1], data[:, ADC_CH2])

def find_delay(CCR_data, frequency):
    for i in range(CCR_data):
        max_val = -1
        max_index = -1
        if CCR_data[i] > max_val:
            max_val = CCR_data[i]
            max_index = i
    return i / frequency

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
    return true
