import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np

# Constants
beta = 0.79
MTOW = 198000 * 9.81  # [N]
landing_weight = MTOW * beta  # [N]
LCN = 85  # value taken from type of pavement

# Parameters for landing gear positioning
most_aft_x = 30.4
l_tail_cone = 19.07
l_nose_cone = 9.83
len_cones = 35.97
d_fus = 5.78
l_nose = 4.5

def fuselage():
    # Lower side of the fuselage
    x_fus = [l_nose_cone, len_cones + l_nose_cone]
    y_fus_lower = [0, 0]
    y_fus_higher = [d_fus, d_fus]

    # Tail cone - 4 deg
    x_tail_cone = [l_nose_cone + len_cones, l_nose_cone + len_cones + l_tail_cone]
    y_tail_cone = [0, 0.5 * d_fus + math.tan(4*math.pi/180) * l_tail_cone]

    x_tail_cone_upper = [l_nose_cone + len_cones, l_nose_cone + len_cones + l_tail_cone]
    y_tail_cone_upper = [d_fus, 0.5 * d_fus + math.tan(4*math.pi/180) * l_tail_cone]

    plt.plot(x_fus, y_fus_lower, color='black')
    plt.plot(x_fus, y_fus_higher, color='black')
    plt.plot(x_tail_cone, y_tail_cone, color='black')
    plt.plot(x_tail_cone_upper, y_tail_cone_upper, color='black')

    #Most aft pos
    plt.scatter(most_aft_x, 0.5 * d_fus, s=5, color='blue')


def scrape_angle():
    # min 15.5 deg from the point connecting the lower side of the cabin to the tail conde
    dx = (5 + 0.5 * d_fus + math.tan(4*math.pi/180) * l_tail_cone)/math.tan(15.5*math.pi/180)
    x = [l_nose_cone + len_cones + l_tail_cone - dx, l_nose_cone + len_cones + l_tail_cone]
    y = [-5, 0.5 * d_fus + math.tan(4*math.pi/180) * l_tail_cone]
    return x, y


def scrape_aft():
    # the line from aft CG with angle = scrape angle
    x = [most_aft_x, most_aft_x + 8.5*math.tan(15.5 * math.pi/180)]
    y = [d_fus/2, d_fus/2 - 8.5]
    plt.plot(x, y, color='grey', linestyle='dotted')
    return x, y


def line_intersection(line1, line2):
    x1, y1, x2, y2 = line1
    x3, y3, x4, y4 = line2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return None

    numerator_x = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    numerator_y = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)

    intersection_x = numerator_x / denominator
    intersection_y = numerator_y / denominator

    return (intersection_x, intersection_y)


def intersection():#
    xl1, yl1 = scrape_angle()
    line1 = [xl1[0], yl1[0], xl1[1], yl1[1]]  # Scrape angle line
    xl2, yl2 = scrape_aft()
    line2 = [xl2[0], yl2[0], xl2[1], yl2[1]]  # Aft cg - scrape angle line
    x_0, y_0 = line_intersection(line1, line2)
    x = [x_0, x_0 + 0.2*math.cos(15.5 * math.pi/180)*math.sin(15.5 *math.pi/180)]
    y = [y_0, y_0 - 0.2*math.cos(15.5 * math.pi/180) ** 2]
    print('Nose wheel: ', x[1], y[1])
    circle((x_0 + 0.2*math.cos(15.5 * math.pi/180)*math.sin(15.5 *math.pi/180), y_0 - 0.2*math.cos(15.5 * math.pi/180) ** 2),
           tire_dimensions_mw[0] / 200)

    plt.scatter(x[0], y[0], s=5, color='black')
    plt.scatter(x[1], y[1], s=5, color='red')
    return x[1] - most_aft_x, y[1], x[1]


def wing():
    # Plotting the position of MAC
    x = [28.4, 34.64]
    y = [1.7 / 2, 1.7 / 2]
    plt.plot(x, y, color='grey')
    return y[0]


def nose_cone():
    t = np.linspace(math.pi / 2, math.pi * 3/2, 100)
    a = l_nose_cone
    b = 0.5 * d_fus

    x = a * np.cos(t)
    y = 0.5 * d_fus + b * np.sin(t)
    plt.plot(x + l_nose_cone, y, color='black')

    '''x = [0, l_nose_cone]
    y = [0, 0]
    plt.plot(x, y, color='black')'''


def number_of_main_wheels():
    f = landing_weight / MTOW
    return math.ceil((f * MTOW / 210000) / 4) * 4


def max_tire_pressure():
    p = 430 * math.log(LCN) - 680
    return p


def struts(nose_wheel_cord):
    # Main wheels struts
    _, my0, mx0 = intersection()
    my1 = wing()
    plt.plot([mx0, mx0], [my0, my1], color='black')

    # Nose wheels struts
    nx0, ny0 = nose_wheel_cord
    plt.plot([nx0, nx0], [ny0, 0 + 0.3], color='black')

# Wheel sizing
N_main_wheels = number_of_main_wheels()
N_nose_wheels = 2
number_of_struts = 2
tire_pressure_max = max_tire_pressure()  # [kPa]
tire_dimensions_mw = [50 * 2.54, 20 * 2.54]  # [inches to cm]
tire_dimensions_nw = [34 * 2.54, 11 * 2.54]  # [inches to cm]


def nose_wheel(ln):
    x = [most_aft_x - ln, most_aft_x - ln]
    _, y_1, _ = intersection()
    y_1 = y_1 - tire_dimensions_mw[0] / 200 + tire_dimensions_nw[0] / 200
    y = [y_1, 0]


def three_deg():
    lm, _, _ = intersection()
    print(f'lm = {lm}')
    _, y_1, x_1 = intersection()
    y_1 -= tire_dimensions_mw[0] / 200
    x = [0, x_1]
    y = [y_1 + tire_dimensions_nw[0] / 200 + math.tan(3 * math.pi/180) * (lm + most_aft_x), y_1]
    return x[0], y[0], x[1], y[1]


def circle(center, radius):
    circle = Circle(center, radius, color='blue', fill=False, linestyle='-')

    ax = plt.gca()
    ax.add_patch(circle)

    ax.set_aspect('equal', 'box')

def circle2(radius, center = (0,0)):
    # Define theta for only one quarter (0 to π/2)
    theta = np.linspace(3 * np.pi / 2, 2*np.pi + 0.1, 100)

    # Calculate x and y for the right bottom quarter of the circle
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)

    # Plotting only the right bottom quarter of the circle
    plt.plot(x, y, linestyle= ':', color='green')

# Wheel positioning
P_mw = 0.92 * MTOW / N_main_wheels  # static load main wheel[N]
P_nw = 0.08 * MTOW / N_nose_wheels  # static load nose wheel[N]

# plot
plt.grid()
plt.gca().set_aspect('equal')
scrape_angle()
fuselage()
scrape_aft()
lm, _, _ = intersection()
ln = (1/0.08 - 1) * lm
print('ln: ', ln, 'lm: ', lm)
wing()
nose_cone()
nose_wheel(ln)

line_three_deg = [_, _, _, _]
line_three_deg[0], line_three_deg[1], line_three_deg[2], line_three_deg[3] = three_deg()
nose_wheel_l = line_intersection([most_aft_x - ln, -5,  most_aft_x - ln, 0], line_three_deg)
nose_wheel_y = nose_wheel_l[1] + tire_dimensions_nw[0] / 200
nose_wheel_l2 = [nose_wheel_l[0], nose_wheel_y]
print(nose_wheel_l, nose_wheel_y)
circle(nose_wheel_l2, tire_dimensions_nw[0] / 200)

circle2(3.55, (most_aft_x - ln, -0.2))

struts(nose_wheel_l2)
plt.show()