import math as m
import numpy as np
import matplotlib.pyplot as plt

# Functions
def calc_Re(indicator, rho, V, l_wing, l_fus,l_eng, miu):
    if indicator == 'w':
        Re = (rho * V * l_wing) / miu
    if indicator == 'f':
        Re = (rho * V * l_fus) / miu
    if indicator == 'e':
        Re = (rho * V * l_eng) / miu
    return Re

def C_f(indicator, Re, M):
    c_flam = 1.328 / m.sqrt(Re)
    c_ftur = 0.455 / ((m.log(Re, 10) ** 2.58) * ((1 + 0.144 * M ** 2)) ** 0.65)
    if indicator == 'w':
        Cf = 0.05 * c_flam + 0.95 * c_ftur
    if indicator == 'f':
        Cf = 0.1 * c_flam + 0.9 * c_ftur
    if indicator == 'e':
        Cf = 0.1 * c_flam + 0.9 * c_ftur
    return Cf

def FF(indicator, t_c, x_c, M, lam_m, l_fus, d_fus, l_eng, d_eng):
    if indicator == 'w':
        FF = (1 + (0.6 / x_c) * t_c + 100 * t_c ** 4) * (1.34 * (M ** 0.18) * (m.cos(lam_m) ** 0.28))
    if indicator == 'f':
        FF = 1 + 60 / ((l_fus/d_fus) ** 3) + (l_fus/d_fus) / 400
    if indicator == 'e':
        FF = 1 + 0.35/ (l_eng/d_eng)
    return FF

def IF(indicator):
    if indicator == 'w':
        IF = 1.25
    if indicator == 'f':
        IF = 1
    if indicator == 'e':
        IF = 1.3
    return IF

def C_w(k_a, lam_le, Cl, t_c, M):
    M_dd = k_a / m.cos(lam_le) - t_c / (m.cos(lam_le) ** 2) - Cl / (10 * (m.cos(lam_le) ** 3))
    M_cr = M_dd - (0.1 / 80) ** (1 / 3)
    if M < M_cr:
        C_w = 0
    if M_cr <= M <= M_dd:
        C_w = 0.002 * (1 + 2.5 * ((M_dd - M) / 0.05)) ** (-1)
    if M_dd < M:
        C_w = 0.002 * (1 + ((M - M_dd) / 0.05)) ** 2.5
    return C_w

def S_w(indicator, D, L1, L2, L3, S_exp,l_eng,d_eng):
    if indicator == 'w':
        S_w = 2 * 1.07 * S_exp
    if indicator == 'f':
        S_w = (m.pi * D / 4) * ((1 / (3 * (L1 ** 2))) * (((4 * (L1 ** 2) + (D ** 2) / 4) ** 1.5) - (D ** 3) / 8) - D + (4 * L2 )+ 2 * m.sqrt((L3 ** 2) + ((D ** 2 )/ 4)))
    if indicator == 'e':
        S_w = l_eng * d_eng * m.pi * 2
    return S_w

# Variables
lam_m = 27.45 * m.pi / 180
lam_le = 30.8 * m.pi / 180
S_exp = 319.1
rho = 0.316
V = 241.96
M = 0.82
miu = 0.0000142
k = 0.152 * 10 ** (-5)
k_a = 0.95
l_fus = 64.87
l_wing = 5.65
l_eng = 6.4
d_fus = 5.78
d_eng = 3.94
L1 = 4.5
L3 = 12.3981
L2 = l_fus - L1 - L3
t_c = 0.1194
x_c = 0.355
AR = 10
ind = ['w', 'f','e']
Cl = 0.6299
Cc = 0
A_max = d_fus**2 * m.pi/4
A_base = d_fus * l_fus
upsweep = 0 #change

# Function input
for i in range(len(ind)):
    indicator = ind[i]
    Re_val = calc_Re(indicator, rho, V, l_wing, l_fus,l_eng, miu)
    C_f_val = C_f(indicator, Re_val, M)
    FF_val = FF(indicator, t_c, x_c, M, lam_m, l_fus, d_fus, l_eng, d_eng)
    IF_val = IF(indicator)
    S_w_val = S_w(indicator, d_fus, L1, L2, L3, S_exp,l_eng,d_eng)
    #Add values
    Cc += C_f_val * FF_val * IF_val * S_w_val

C_w_val = C_w(k_a, lam_le, Cl, t_c, M)
# Final calculation
C_D0 = (1 / S_exp) * Cc + C_w_val
print("Zero lift drag coefficient is:", C_D0)

#drag polar
def k_k(AR,lam_le):
    e = 4.61*(1-0.045*AR**0.68)*(m.cos(lam_le)**0.15)-3.1
    k = 1/(m.pi*AR*e)
    return k
k = k_k(AR, lam_le)
x = np.linspace(-1, 2, 400)
y = C_D0 + k * x**2
C_D = C_D0 + k*Cl**2
print("Drag coefficient is:", C_D)

#Drag
D = C_D * 0.5 * rho * V**2 * S_exp
print("Drag is:", D)
#plotting
plt.plot(x, y, label=f'Drag Polar')
plt.xlabel('C_L')
plt.ylabel('C_D')
plt.title('Drag Polar')
plt.show()
