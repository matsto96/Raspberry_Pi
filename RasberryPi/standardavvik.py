import math
import statistics as stat

def stdavvik(red_fft, green_fft, blue_fft, red_auto, green_auto, blue_auto):
    data_list = []

    if red_fft > 0:
        data_list.append(red_fft)
    if green_fft > 0:
        data_list.append(green_fft)
    if blue_fft > 0:
        data_list.append(blue_fft)
    if red_auto > 0:
        data_list.append(red_auto)
    if green_auto > 0:
        data_list.append(green_auto)
    if blue_auto > 0:
        data_list.append(blue_auto)

    std = stat.stdev(data_list)

    print("Standardavvik: ", std)


a = [11.39, -13.35, 15.72, -5.54, 14.63]
tot = 0.0
for i in a:
    tot += i
print("Gjennomsnitt: ", tot/len(a))

#Vid1: 21.038199186242153
#Vid2: 1.018233764908632
#Vid3: 24.56488957842066
#Vid4: 0.8555992052357181
#Vid5: 13.57645019878172