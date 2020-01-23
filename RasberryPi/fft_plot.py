import matplotlib.pyplot as plt
import numpy as np

x, y = np.loadtxt("NAME OF DATA FILE")

plt.plot(np.fft.fft(y))
plt.title('Data from Raspberry Pi - FFT-plot')
plt.show()