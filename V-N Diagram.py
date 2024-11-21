import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

#Using imperial units, graph is in KEAS
WS_ratio = 6086 * 0.020885      #Weight to Wing area ratio (lbs/ft^2)
rho = 0.316  * 0.0624279606     #Density at cruise(lbs/ft^3)
C_La = 4.456                    #Lift aoa slope (rad) at M = 0.2
MAC = 6.2 * 3.2808              #Mean Aerodynamic Chord length (ft)
gamma = 1.4

#Draw V-n diagram at
Mach = 0

#Laitone correction, valid for Mach up to 0.9
def laitone(Mach, x):
    beta = math.sqrt(1 - Mach ** 2)
    correction_term = Mach ** 2 * (1 + ((gamma - 1) / 2) * Mach ** 2) / (2 * beta)
    return x / (beta + correction_term * x)

#Find C_La at Mach = 0 from C_La from Mach = 0.2
C_La0 = fsolve(lambda x: laitone(0.2, x) - C_La, 0.5)[0]

C_La = laitone(Mach, C_La0)

print(C_La)

#Values read from graph in WP2
AR = 10                         #Aspect Ratio
eff = 0.434                     #Oswald efficiency factor
C_Lmax = 1.63     
C_DatCLmax = 0.0171 + C_Lmax**2/(math.pi * eff * AR)
C_Lmax_neg = -1.67 * 0.8        #Using DATCOM method together with graphs from WP2
C_DatCLmax_neg = 0.0171 + C_Lmax_neg**2/(math.pi * 0.434 * 10)
C_Lmax_HLD = 2.066              #Maximum C_Lmax attained by aircraft, with HLD devices extended

n_max = 2.5                     #Given our aircraft weight
n_min = -1                      #Given our aircraft weight
H = 39000                       #Altitude at cruise in ft

C_Nmax = math.sqrt(C_Lmax**2 + (C_DatCLmax)**2 )
C_Nmin = -math.sqrt(C_Lmax_neg**2 + (C_DatCLmax_neg)**2 )

#Speeds in feet
V_S0 = math.sqrt(2*WS_ratio/(rho*C_Lmax_HLD))   #Stall speed with flaps extended
V_S1 = math.sqrt(2*WS_ratio/(rho*C_Nmax))       #Stall speed with flaps retracted
V_A = 0                                         #Minimum Speed, calculated later on code
V_B = 0                                         #High lift at max aoa - using equation from BS student papers, calculated later
V_C = 239 * 1.68781                             #Cruise Speed
V_D = 1.25*V_C                                  #Dive Speed, taking regulations for minimum value

V_F1 = 1.6 * V_S1           #With wingflaps in take off position at MTOW
V_F2 = 1.8 * V_S1           #With wingflaps in approach position at MLW
V_F3 = 1.8 * V_S0           #With wingflaps in landing position at MLW

V_F = min(V_F1, V_F2, V_F3)


#Maneuver load diagram
V1_array = []
N1_array = []

V2_array = []
N2_array = []

V3_array = []
N3_array = []

V = np.linspace(0,400, 4000)

for v in V:
    n = (0.5 * rho * (v)**2 * C_Nmax)/WS_ratio      #Test some speeds until speed at which n=2.5 is reached
    V1_array = np.append(V1_array, v)               #Append values to array for plotting
    N1_array = np.append(N1_array, n)

    if n >= n_max:
        if v <= V_S1 * n_max**0.5:
            V_A = V_S1 * n_max**0.5      #Minimum value for V_A
        else:
            V_A = v                     #If v at n=2.5 is greater than minimum, then assign that value as V_A
        break
    if n <= 2:
        Vn2 = v

for v in V:
    n = (0.5 * rho * (v)**2 * C_Nmin)/WS_ratio
    V2_array = np.append(V2_array, v)
    N2_array = np.append(N2_array, n)
 
    if n <= n_min:
        break

for v in V:
    n = (0.5 * rho * (v)**2 * C_Lmax_HLD)/WS_ratio
    V3_array = np.append(V3_array, v)
    N3_array = np.append(N3_array, n)
 
    if n >= 2:
        break


V1_array = np.append(V1_array, [V_C, V_D, V_D]) * 0.592484  #Convert values to kt
N1_array = np.append(N1_array, [n_max, n_max, 0])

V2_array = np.append(V2_array, [V_C, V_D]) * 0.592484       #Convert values to kt
N2_array = np.append(N2_array, [n_min, 0])

V3_array = np.append(V3_array, [Vn2]) * 0.592484             #Convert values to kt
N3_array = np.append(N3_array, [2])

plt.figure(figsize=(8, 6))

plt.plot(V1_array, N1_array, 'blue')
plt.plot(V2_array, N2_array, 'blue')
plt.plot(V3_array, N3_array, 'blue')
plt.plot([0, V_S1 * 0.592484], [1, 1], 'gray', linestyle='dashed')
plt.plot([V_S1 * 0.592484, V_S1 * 0.592484], [1, 0], 'gray', linestyle='dashed')
plt.plot([V_A * 0.592484, V_A * 0.592484], [2.5, 0], 'gray', linestyle='dashed')
plt.plot([V_C * 0.592484, V_C * 0.592484], [0, -1], 'gray', linestyle='dashed')
plt.plot([0, V_D * 0.592484], [0, 0], 'black', linestyle='dashed')
plt.ylim(-1.2,3.2)
plt.xlabel('Airspeed, KEAS')
plt.ylabel('Load factor, n')

#Gust diagram

mu_g = (2*WS_ratio)/(rho * C_La * MAC * 32.2)

K = (0.88 * mu_g)/(5.3 + mu_g)
'''
a = (0.5*rho*C_Nmax)
b = -(C_la * K * 48)/(498)
c = -WS_ratio
V_B = (-b + math.sqrt(b**2 - 4*a*c))/(2*a)      #V_B may not be less than the speed determined from the intersection of the C_N_max line and the gust line marked V_B, Roskam
'''

U_ref = (44-20.86)/(15000-60000) * (H - 15000) + 44    #Linearization from values given in CS-25.341 (a)(5)

V_B = V_S1 * (1 + (K * U_ref * V_C * C_La)/(498*WS_ratio))**0.5  #Given by CS-25 book 1 

if V_B >= V_C - 1.32 * U_ref:                    #V_C >= V_B + 1.32 * U_ref
    V_B = V_C - 1.32 * U_ref

#High aoa, Cruise, Dive
u_hat = np.array([48, 34, 17])                  #Obtained from statistical data
speeds = np.array([V_B,V_C,V_D])


delta_n = (rho * speeds * C_La * K * u_hat )/(2 * WS_ratio)

n_lim = n_max
if n_max < 1+ delta_n[1]:               #Get the limiting load factor, checking if the gust diagram values exceed n_max
    n_lim = 1+ delta_n[1]

V_S1 *= 0.592484
V_A *= 0.592484
V_B *= 0.592484
V_C *= 0.592484
V_D *= 0.592484

V3_array = [0, V_B, V_C, V_D, V_D, V_C, V_B, 0]
N3_array = [1, delta_n[0]+1, delta_n[1]+1, delta_n[2]+1, 1-delta_n[2], 1-delta_n[1], 1-delta_n[0], 1]

plt.plot(V3_array, N3_array, 'red')
#plt.plot([0, V_B], [1, 1+ delta_n[0]], 'orange', linestyle='dashed')
plt.plot([0, V_C], [1, 1+ delta_n[1]], 'orange', linestyle='dashed')
plt.plot([0, V_D], [1, 1+ delta_n[2]], 'orange', linestyle='dashed')
#plt.plot([0, V_D], [1, 1], 'orange', linestyle='dashed')
#plt.plot([0, V_B], [1, 1- delta_n[0]], 'orange', linestyle='dashed')
plt.plot([0, V_C], [1, 1- delta_n[1]], 'orange', linestyle='dashed')
plt.plot([0, V_D], [1, 1- delta_n[2]], 'orange', linestyle='dashed')
plt.plot([V_B, V_B], [1+ delta_n[0], 1- delta_n[0]], 'gray', linestyle='dashed')
plt.plot([V_C, V_C], [1+ delta_n[1], 1- delta_n[1]], 'gray', linestyle='dashed')

print(1+ delta_n[1])

plt.xlabel('Airspeed, KEAS')
plt.ylabel('Load factor, n')
plt.ylim(-1.2,3.5)
plt.show()


