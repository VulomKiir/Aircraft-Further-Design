import math
from scipy import integrate
import matplotlib.pyplot as plt
import numpy as np

#known
S = 319
b = 56.49
mac = 6.2
X_aftcg = 32.7830

X_h =  20.60448 #(67.6ft)
X_v =  19.81 #(65ft)

f = 64.87 #fuselage length
K = 1.4
D = 5.78 #fuselage diameter

#statistical
Vol_h = 1.1 #0.94ft
Vol_v = 0.11 #0.067ft

l_vt = 0.45 * f #should be ~45% of the fuselage length 

def arm(K, mac, S, D, Vol_h):
    l_ht = K * math.sqrt((4*mac*S*Vol_h)/(math.pi*D))
    return(l_ht)
l_ht = arm(K, mac, S, D, Vol_h)
#should be ~47% of the fuselage length


def hor(Vol_h, S, mac, l_ht):
    S_h = Vol_h * S * mac / l_ht
    return(S_h)

def ver(Vol_v, S, b, l_vt):
    S_v = Vol_v * S * b / l_vt
    return(S_v)

S_v = ver(Vol_v, S, b, l_vt)
S_h = hor(Vol_h, S, mac, l_ht)


print("Horizontal tail moment arm:", l_ht) #c/4 interects with it, most aft cg
print("Vertical tail moment arm", l_vt) 
print(f"Vertical Tail Area (S_v): {S_v:.4f}")
print(f"Horizontal Tail Area (S_h): {S_h:.4f}")

#based on the reference aircrafts
#vertical tail
AR_v = 1.8
taper_ratiov = 0.3
lesweep_v = 0.610865 #40deg, leading edge sweep

#horizontal tail
AR_h = 3.5
taper_ratioh = 0.4
quartersweep_h =  #30deg
lesweep_h =  #34.98 deg


 
def b_v(AR_v, S_v):
    b_v = math.sqrt(AR_v * S_v)
    return b_v
def c_rv(taper_ratiov, S_v, b_v):
    c_rv = (2 * S_v) / ((1 + taper_ratiov) * b_v)
    return c_rv
def c_tv(taper_ratiov, cr_v):
    c_tv = taper_ratiov * cr_v
    return c_tv
def mac_v(c_rv, TR):
    mac_v = (2/3) * c_rv * ((1 + taper_ratiov + (taper_ratiov)**2) / (1 + taper_ratiov)) 
    return mac_v
def ymac_v(b_v, taper_ratiov):
    ymac_v = (b_v / 6) * (1 + 2 * taper_ratiov) / (1 + taper_ratiov)  
    return ymac_v

def b_h(AR_h, S_h):
    b_h = math.sqrt(AR_h * S_h)
    return b_h
def c_rh(taper_ratioh, S_h, b_h):
    c_rh = (2 * S_h) / ((1 + taper_ratioh) * b_h)
    return c_rh
def c_th(taper_ratioh, cr_h):
    c_th = taper_ratioh * cr_h
    return c_th
def mac_h(c_rh, taper_ratioh):
    mac_h = (2/3) * c_rh * ((1 + taper_ratioh + (taper_ratioh)**2) / (1 + taper_ratioh)) 
    return mac_h
def ymac_h(b_h, taper_ratioh):
    ymac_h = (b_h / 6) * (1 + 2 * taper_ratioh) / (1 + taper_ratioh)  
    return ymac_h


b_v_val = b_v(AR_v, S_v)
c_rv_val = c_rv(taper_ratiov, S_v, b_v_val)
c_tv_val = c_tv(taper_ratiov, c_rv_val)
mac_v_val = mac_v(c_rv_val, taper_ratiov)
ymac_v_val = ymac_v(b_v_val, taper_ratiov)
print("\nVertical Tail Planform Values:")
print(f"Wingspan (b_v): {b_v_val:}")
print(f"Root Chord (c_rv): {c_rv_val:}")
print(f"Tip Chord (c_tv): {c_tv_val:}")
print(f"Mean Aerodynamic Chord (MAC) (mac_v): {mac_v_val:}")
print(f"y-location of MAC (ymac_v): {ymac_v_val:}")
b_h_val = b_h(AR_h, S_h)
c_rh_val = c_rh(taper_ratioh, S_h, b_h_val)
c_th_val = c_th(taper_ratioh, c_rh_val)
mac_h_val = mac_h(c_rh_val, taper_ratioh)
ymac_h_val = ymac_h(b_h_val, taper_ratioh)
print("\nHorizontal Tail Planform Values:")
print(f"Wingspan (b_h): {b_h_val:}")
print(f"Root Chord (c_rh): {c_rh_val:}")
print(f"Tip Chord (c_th): {c_th_val:}")
print(f"Mean Aerodynamic Chord (MAC) (mac_h): {mac_h_val:}")
print(f"y-location of MAC (ymac_h): {ymac_h_val:}")
