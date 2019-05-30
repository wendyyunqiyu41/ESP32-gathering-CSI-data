import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
import math

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
x = []
y = []

def animate(i, x, y):  
    colors = (0, 0, 0)

    allData = []
    real = []
    index = list(range(0, 64))
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

    x = np.array(index)
    y = np.array(magnitude)

    ax.scatter(x, y)
    ax.plot(x, y)
    plt.title('Scat Test')
    plt.xlabel('Index')
    plt.ylabel('Magnitude')
    plt.pause(0.0001)
    ax.clear()

ani = animation.FuncAnimation(fig, animate, fargs=(x, y), interval=1)
plt.show()
