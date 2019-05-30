#over the air flashing
import math

while 1:
    real = []
    imaginary = []
    magnitude = []
    phaseArray = []

    tStamp = raw_input().strip().split()
    allData = raw_input().strip().split()

    counter = 0

    # Filling real and imaginary arrays
    for x in allData:
        if counter % 2 == 0:
            imaginary.append(int(x))
            counter += 1
        else:
            real.append(int(x))
            counter += 1

    # Calculating magnitude and phase
    for i in range(len(real)):

        # Calculating Magnitude
        mag = math.sqrt(real[i]**2 + imaginary[i]**2)
        mag = '%.2f' % round(mag, 2)
        mag = float(mag)
        magnitude.append(mag)

        # Calculating Phase 
        if real[i] == 0:
            real[i] = 0.00000000001
            phase = math.atan(imaginary[i] / real[i])
            phase = '%.2f' % round(phase, 2)
            phase = float(phase)
            phase = math.degrees(phase)
            phaseArray.append(phase)
        
        else:
            phase = math.atan(imaginary[i] / real[i])
            phase = '%.2f' % round(phase, 2)
            phase = float(phase)
            phase = math.degrees(phase)
            phaseArray.append(phase)

    print (tStamp)
    print (magnitude)
    print (phaseArray)
