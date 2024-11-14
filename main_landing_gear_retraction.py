import math
import matplotlib.pyplot as plt

WingSpan = 56.49
Angle_le = 30.83 * math.pi/180
# YMAC = 11.6
MAC_length = 6.2
c_t = 2.6
c_r = 9.8

M_cruise = 0.82     # From REQ-CRUISE-01
AspectRatio = 10   # From Class I weight estimation
WingArea = 319.1      # From Matching Diagram

def angle_of_quarter_chord_line(MachAtCruise):
    return math.acos(1.16/(MachAtCruise+0.5))

def angle_of_leading_edge(angle_of_quarter_chord_line, ChordLengthAtRoot, WingSpan, TaperRatio):
    return math.atan(math.tan(angle_of_quarter_chord_line) - (ChordLengthAtRoot*(TaperRatio-1)/(2*WingSpan)))

def wing_span(aspect_ratio, S):
    return math.sqrt(aspect_ratio*S)

#must be less than 80m

def taper_ratio(angle_of_quarter_chord_line):
    return 0.2*(2-angle_of_quarter_chord_line)

def root_chord(taper_ratio, S, b):
    return (2*S)/((1+taper_ratio)*b)

def mean_geometric_chord(root_chord, taper_ratio):
    return (2/3)*root_chord*((1 + taper_ratio + (taper_ratio)**2)/( 1 + taper_ratio))    #Given in slides

def YLEMGC(wing_span, taper_ratio):
    return (wing_span/6) * ( 1 + 2*taper_ratio)/(1 + taper_ratio)     #Given in slides

def XLEMGC(YLEMGC, AngleOfLeadingEdge):
    return YLEMGC * math.tan(AngleOfLeadingEdge)

def dihedral(QuarterChordAngle):
    return 3 - 0.1*QuarterChordAngle + 2

def ARmax(TaperRatio, QChordAngle):
    return math.floor(7.72*(2-TaperRatio)*math.exp(-0.043*QChordAngle))

def Strut(x, y, dist):
    x_l = [x, x - dist]
    y_l = [y, y]
    plt.plot(x_l, y_l, color="grey")

def circle(center, radius):

    circle = plt.Circle(center, radius, color='blue', fill=False, linestyle='-')

    ax = plt.gca()
    ax.add_patch(circle)

    ax.set_aspect('equal', 'box')

# Plotting yehudi
def yahoo():
    x = [5.78 / 2, 10]
    y = [12.5, 12.5]
    plt.plot(x, y, color="blue")

#Calculated values
Angle_c4 = 28.5*math.pi/180
DihedralAngle = dihedral(Angle_c4*180/math.pi)
TaperRatio = 0.3
WingSpan = wing_span(AspectRatio, WingArea)
c_r = root_chord(TaperRatio, WingArea, WingSpan)
c_t = TaperRatio * c_r
Angle_le = angle_of_leading_edge(Angle_c4, c_r, WingSpan, TaperRatio)
MAC_length = mean_geometric_chord(c_r, TaperRatio)
YMAC = YLEMGC(WingSpan, TaperRatio)
XMAC = XLEMGC(YMAC, Angle_le)

print('Quarter Chord Angle:', Angle_c4*180/math.pi)
print('Leading Edge Angle:', Angle_le*180/math.pi)
print('Wing span:', WingSpan)
print('Taper Ratio:', TaperRatio)
print('Root Chord length:', c_r)
print('Tip Chord length:', c_t)
print('Dihedral Angle:', DihedralAngle)
print('Offset:', math.tan(Angle_le)* WingSpan /2)
print('MAC length and X, Y Position:',MAC_length, XMAC, YMAC)
print('Max AR:', ARmax(TaperRatio, Angle_c4), 'Actual AR:', AspectRatio )

x = [0, WingSpan/2, WingSpan/2, 0,0]
y = [0, math.tan(Angle_le)*WingSpan/2,  math.tan(Angle_le)*WingSpan/2 + c_t, c_r,0]

xmac = [YMAC, YMAC]
ymac = [math.tan(Angle_le)*(YMAC), math.tan(Angle_le)*(YMAC) + MAC_length]

xland = [6.46]
#yland = [math.tan(Angle_le)*(YMAC) + 4.094]
a = 30.4 + 2.17 - 28.44
print('a:', a)
yland = [math.tan(Angle_le)*(YMAC) + a]

D_fus = 5.78

xfus = [D_fus/2, D_fus/2]
yfus = [0, 20]

plt.grid()
plt.plot(x, y, label = "Wing outline")
#plt.plot(xmac, ymac, color="grey", label = 'MAC')
plt.plot(xmac, ymac, label = 'Landing gear position', color="grey")
#plt.plot(xland, yland, marker = 'o',  markerfacecolor="green", label = 'Landing gear position')
plt.scatter(xland, yland, color="black")
plt.plot(xfus, yfus, color="grey")
Strut(6.46, math.tan(Angle_le)*(YMAC) + a, 5.78)
yahoo()

# Plotting the wheels
bottom_x = 6.46 - 5.78
bottom_y = math.tan(Angle_le)*(YMAC) + a

tire_dimensions_mw = [50 * 2.54, 20 * 2.54]  # [inches to cm]

x_1 = bottom_x
temp_val = tire_dimensions_mw[0] / 200
y_1 = bottom_y + temp_val
y_2 = bottom_y - temp_val

circle((x_1, y_1), tire_dimensions_mw[0] / 200)
circle((x_1, y_2), tire_dimensions_mw[0] / 200)


plt.xlabel("Distance (m)")
plt.ylabel("Distance (m)")
plt.gca().invert_yaxis()
plt.show()

