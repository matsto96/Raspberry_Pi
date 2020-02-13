#drivers.run_adc("alarm45.bin")
#drivers.transfer_data_from_pi("alarm45.bin")

#Sample period and data
# N = Number of samples
# T = Period (1  / N)
N = 31250 - 100
T = 1.0/31250.0

# Import data from Pi files

sampleP, data = raspi_import.raspi_import("/home/mats/Desktop/data/alarm45.bin")
#print(sampleP)

# Convert 12 bit number to a voltage

data = data/4095*3.3
data = data[100:]
#print(data)

#drivers.plot_all(data)
#plt.show()
#plt.plot(data[:, 2])

# Todo put this in drivers as a function
# Kall fila main, og organiser det slik at kvar dag er ein funksjon
"""data = drivers.filter_data(data)
a = np.array([a for a in range(50)])
plt.scatter(a, data[1400:1450, 0])
plt.scatter(a, data[1400:1450, 1])
plt.scatter(a, data[1400:1450, 2])
#plt.xlim(50, 1000)
#plt.show()"""
plt.figure(3)
plt.title("Raw sound data")
plt.plot(data[:, 0])
plt.plot(data[:, 1])
plt.plot(data[:, 2])
#plt.show()

for a in range(5):
    data[:, a] = data[:, a] - np.mean(data[:, a])



correlation21 = drivers.CCR(data, 0, 1) # 1-0
correlation31 = drivers.CCR(data, 0, 2) # 2-0
correlation32 = drivers.CCR(data, 1, 2) # 2-1

plt.figure(1)
plt.title("Correlation")
drivers.plot_correlation(correlation21)
drivers.plot_correlation(correlation31)
drivers.plot_correlation(correlation32)
#plt.show()

delay21 = drivers.find_delay(correlation21)
delay31 = drivers.find_delay(correlation31)
delay32 = drivers.find_delay(correlation32)


angle = drivers.find_theta(delay21, delay31, delay32)
degrees = drivers.rad_to_deg(angle)

print(delay21, delay31, delay32)
print("Angle: ", angle)
print("Degrees: ", degrees)


# drivers.plot_fft(data, N, T, 5)  # Lab 1


"""

Sann : estimert : avvik
40 : 16 : 24
0 : -23: -23
-40 : -60 : -20
-90 : -83: -7
-130 : -120 : -10
-180 : -160 : 20
150 : 143 : 7
100 : 70 : 30
70 : 41 : 29
20 : -19 : -39

"""
plt.figure(2)
plt.title("Sann verdi (*) og estimert verdi")
plt.plot([math.cos(40/180*math.pi), math.cos(16/180*math.pi)], [math.sin(40/180*math.pi), math.sin(16/180*math.pi)], '--')
plt.plot([math.cos(0/180*math.pi), math.cos(-23/180*math.pi)], [math.sin(0/180*math.pi), math.sin(-23/180*math.pi)], '--')
plt.plot([math.cos(-40/180*math.pi), math.cos(-60/180*math.pi)], [math.sin(-40/180*math.pi), math.sin(-60/180*math.pi)], '--')
plt.plot([math.cos(-90/180*math.pi), math.cos(-83/180*math.pi)], [math.sin(-90/180*math.pi), math.sin(-83/180*math.pi)], '--')
plt.plot([math.cos(-130/180*math.pi), math.cos(-120/180*math.pi)], [math.sin(-130/180*math.pi), math.sin(-120/180*math.pi)], '--')
plt.plot([math.cos(180/180*math.pi), math.cos(160/180*math.pi)], [math.sin(-180/180*math.pi), math.sin(160/180*math.pi)], '--')
plt.plot([math.cos(150/180*math.pi), math.cos(143/180*math.pi)], [math.sin(150/180*math.pi), math.sin(143/180*math.pi)], '--')
plt.plot([math.cos(100/180*math.pi), math.cos(70/180*math.pi)], [math.sin(100/180*math.pi), math.sin(70/180*math.pi)], '--')
plt.plot([math.cos(70/180*math.pi), math.cos(41/180*math.pi)], [math.sin(70/180*math.pi), math.sin(41/180*math.pi)], '--')
plt.plot([math.cos(20/180*math.pi), math.cos(-19/180*math.pi)], [math.sin(20/180*math.pi), math.sin(-19/180*math.pi)], '--')

plt.scatter(math.cos(40/180*math.pi), math.sin(40/180*math.pi))
plt.scatter(math.cos(0/180*math.pi), math.sin(0/180*math.pi))
plt.scatter(math.cos(-40/180*math.pi), math.sin(-40/180*math.pi))
plt.scatter(math.cos(-90/180*math.pi), math.sin(-90/180*math.pi))
plt.scatter(math.cos(-130/180*math.pi), math.sin(-130/180*math.pi))
plt.scatter(math.cos(180/180*math.pi), math.sin(180/180*math.pi))
plt.scatter(math.cos(150/180*math.pi), math.sin(150/180*math.pi))
plt.scatter(math.cos(100/180*math.pi), math.sin(100/180*math.pi))
plt.scatter(math.cos(70/180*math.pi), math.sin(70/180*math.pi))
plt.scatter(math.cos(20/180*math.pi), math.sin(20/180*math.pi))

plt.show()