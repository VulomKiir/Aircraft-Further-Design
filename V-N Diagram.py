import numpy as np
import math
import matplotlib.pyplot as plt

#Using imperial units, graph is in KEAS
WS_ratio = 6086 * 0.020885      #Weight to Wing area ratio (lbs/ft^2)
rho = 0.316  * 0.0624279606     #Density at cruise(lbs/ft^3)
C_la = 4.87                     #Lift aoa slope (rad)
MAC = 6.2 * 3.2808              #Mean Aerodynamic Chord length (ft)

#Values read from graph in WP2
C_Lmax = 2.066      
C_DatCLmax = 0.0375
C_Lmax_neg = -1.67
C_DatCLmax_neg = 0.035

n_max = 2.5                     #Given our aircraft weight
n_min = -1                      #Given our aircraft weight
H = 39000                       #Altitude at cruise in ft

C_Nmax = math.sqrt(C_Lmax**2 + (C_DatCLmax)**2 )
C_Nmin = -math.sqrt(C_Lmax_neg**2 + (C_DatCLmax_neg)**2 )

#Speeds in feet
V_S = math.sqrt(2*WS_ratio/(rho*C_Nmax))     #+1g stall speed
V_A = 0                                      #Minimum Speed, calculated later on code
V_B = 0                                      #High lift at max aoa - using equation from BS student papers, calculated later
V_C = 239 * 1.68781                          #Cruise Speed
V_D = 1.25*V_C                               #Dive Speed, taking regulations for minimum value

#Maneuver load diagram
V1_array = []
N1_array = []

V2_array = []
N2_array = []

V = np.linspace(0,400, 4000)

for v in V:
    n = (0.5 * rho * (v)**2 * C_Nmax)/WS_ratio      #Test some speeds until speed at which n=2.5 is reached
    V1_array = np.append(V1_array, v)               #Append values to array for plotting
    N1_array = np.append(N1_array, n)

    if n >= n_max:
        if v <= V_S * n_max**0.5:
            V_A = V_S * n_max**0.5      #Minimum value for V_A
        else:
            V_A = v                     #If v at n=2.5 is greater than minimum, then assign that value as V_A
        break

for v in V:
    n = (0.5 * rho * (v)**2 * C_Nmin)/WS_ratio
    V2_array = np.append(V2_array, v)
    N2_array = np.append(N2_array, n)
 
    if n <= n_min:
        break

V1_array = np.append(V1_array, [V_C, V_D, V_D]) * 0.592484  #Convert values to kt
N1_array = np.append(N1_array, [n_max, n_max, 0])

V2_array = np.append(V2_array, [V_C, V_D]) * 0.592484       #Convert values to kt
N2_array = np.append(N2_array, [n_min, 0])

plt.figure(figsize=(8, 6))

plt.plot(V1_array, N1_array, 'blue')
plt.plot(V2_array, N2_array, 'blue')
plt.plot([0, V_S * 0.592484], [1, 1], 'gray', linestyle='dashed')
plt.plot([V_S * 0.592484, V_S * 0.592484], [1, 0], 'gray', linestyle='dashed')
plt.plot([V_A * 0.592484, V_A * 0.592484], [2.5, 0], 'gray', linestyle='dashed')
plt.plot([V_C * 0.592484, V_C * 0.592484], [0, -1], 'gray', linestyle='dashed')
plt.plot([0, V_D * 0.592484], [0, 0], 'black', linestyle='dashed')
plt.ylim(-1.2,3.2)
plt.xlabel('Airspeed, KEAS')
plt.ylabel('Load factor, n')

#Gust diagram
mu_g = (2*WS_ratio)/(rho * C_la * MAC * 32.2)

K = (0.88 * mu_g)/(5.3 + mu_g)

U_ref = (44-20.86)/(15000-60000) * (H - 15000) + 44            #Linearization from values given in CS-25.341 (a)(5)

V_B = V_S * (1 + (K * U_ref * V_C * C_la)/(498*WS_ratio))**0.5  #Given by CS-25 book 1 

if V_B >= V_C - 1.32 * U_ref:                    #V_C >= V_B + 1.32 * U_ref
    V_B = V_C - 1.32 * U_ref

#High aoa, Cruise, Dive
u_hat = np.array([48, 34, 17])                  #Obtained from statistical data
speeds = np.array([V_B,V_C,V_D])


delta_n = (rho * speeds * C_la * K * u_hat )/(2 * WS_ratio)

n_lim = n_max
if n_max < 1+ delta_n[1]:               #Get the limiting load factor, checking if the gust diagram values exceed n_max
    n_lim = 1+ delta_n[1]

V_S *= 0.592484
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

plt.xlabel('Airspeed, KEAS')
plt.ylabel('Load factor, n')
plt.ylim(-1.2,3.2)
plt.show()
