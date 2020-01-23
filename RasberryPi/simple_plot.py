import matplotlib.pyplot as plt
import numpy as np

x, y = np.loadtxt("NAME OF DATA FILE")

plt.plot(x, y, label='Signal')
plt.title('Data from Raspberry Pi')
plt.show()