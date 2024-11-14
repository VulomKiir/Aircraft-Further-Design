import math
import matplotlib.pyplot as plt
import numpy as np

# Parameters for plane front view drawings
d_fus = 5.78
span = 56.49
dihedral = 2.1
main_strut_height = 5.78
nose_strut_height = 3.55
y_mlg = 6.50
main_tire_diameter = (50*2.54)/100
main_tire_width = (20*2.54)/100
nose_tire_diameter = (34*2.54)/100
nose_tire_width = (11*2.54)/100

def wing():
    # Plotting the front view of the wing
    x1 = [0, span/2]
    y1 = [1.7 / 2 + main_strut_height, 1.7 / 2 + span/2 * math.tan(math.radians(dihedral)) + main_strut_height]
    plt.plot(x1, y1, color='grey')
    return y1[0]

def main_landing_gear():
    # Plotting the front view of the landing gear
    x1 = [y_mlg, y_mlg]
    y1 = [1.7 / 2 + y_mlg * math.tan(math.radians(dihedral)), main_strut_height + 1.7 / 2 + y_mlg * math.tan(math.radians(dihedral))]
    plt.plot(x1, y1, color='grey')
    return y1[0]

def main_tire_1():
    x1 = [y_mlg, y_mlg + main_tire_width]
    y1 = [main_tire_diameter, main_tire_diameter]
    plt.plot(x1, y1, color='black')
    x2 = x1
    y2 = [0,0]
    plt.plot(x2, y2, color='black')
    x3 = [y_mlg,y_mlg]
    y3 = [0, main_tire_diameter]
    plt.plot(x3, y3, color='black')
    x4 = [y_mlg + main_tire_width,y_mlg + main_tire_width]
    y4 = y3
    plt.plot(x4, y4, color='black')

def main_tire_2():
    x1 = [y_mlg, y_mlg - main_tire_width]
    y1 = [main_tire_diameter, main_tire_diameter]
    plt.plot(x1, y1, color='black')
    x2 = x1
    y2 = [0,0]
    plt.plot(x2, y2, color='black')
    x3 = [y_mlg,y_mlg]
    y3 = [0, main_tire_diameter]
    plt.plot(x3, y3, color='black')
    x4 = [y_mlg - main_tire_width,y_mlg - main_tire_width]
    y4 = y3
    plt.plot(x4, y4, color='black')

def nose_tire():
    x1 = [0, nose_tire_width]
    y1 = [nose_tire_diameter + main_strut_height - nose_strut_height, nose_tire_diameter + main_strut_height - nose_strut_height]
    plt.plot(x1, y1, color='black')
    x2 = x1
    y2 = [0 + main_strut_height - nose_strut_height,0 + main_strut_height - nose_strut_height]
    plt.plot(x2, y2, color='black')
    x3 = [0,0]
    y3 = [0 + main_strut_height - nose_strut_height, nose_tire_diameter + main_strut_height - nose_strut_height]
    plt.plot(x3, y3, color='black')
    x4 = [nose_tire_width, nose_tire_width]
    y4 = y3
    plt.plot(x4, y4, color='black')

def nose_landing_gear():
    # Plotting the front view of the wing
    x1 = [0, 0]
    y1 = [main_strut_height-nose_strut_height, main_strut_height]
    plt.plot(x1, y1, color='grey')
    return y1[0]

def circle(radius, center=(0,0)):
    # Define theta for only the right half (0 to π)
    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)

    # Calculate x and y for the right half of the circle
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)

    # Plotting only the right half of the circle
    plt.plot(x, y, color='blue')
    plt.scatter(*center, color='red')

    # Set equal scaling and labels
    plt.gca().set_aspect('equal', adjustable='box')
    plt.legend()
    plt.grid(True)

def circle2(radius, center = (0,0)):
    # Define theta for only one quarter (0 to π/2)
    theta = np.linspace(np.pi, 3 * np.pi / 2, 100)

    # Calculate x and y for the right half of the circle
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)

    # Plotting only the right half of the circle
    plt.plot(x, y, linestyle= ':', color='green')

# plot
plt.grid()
plt.gca().set_aspect('equal')

circle(d_fus/2, (0,d_fus/2 + main_strut_height))
circle2(main_strut_height, (y_mlg,main_strut_height))
wing()
main_landing_gear()
nose_landing_gear()
main_tire_1()
main_tire_2()
nose_tire()

plt.show()