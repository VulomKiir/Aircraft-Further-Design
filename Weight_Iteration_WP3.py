import math
from math import pi, cos, tan, atan


# --------------------------|| Conversion  ||--------------------------
conv_d = 3.281                  # feet per meter
conv_w = 0.4536                 # lbs per kg


# ------------------|| Iteration of Weight Estimation ||------------------
perc_tol_p = 1                # maximum acceptable percentage margin between Class I and Class II
perc_tol = perc_tol_p/100       # Ratio


# -------------|| Class I Weight estimation - ADSEE ||-------------
# WING PARAMETERS - from WP2
S_div_Swet = 6     # ADSEE Reader page 105 - fig. 6.2
aspect_ratio = 10  # From WP2 iteration
wing_area = 319.1  # From WP2 iteration
wing_span = 56.49  # From WP2 iteration

# TLAR
Payload_mass = 27670        # kg  # Given
cruise_height = 11887       # m  # Given
Design_range = 13797000     # m  # Given
R_div = 250000              # m
f_con = 0.05                # contingency
endurance_time = 45*60      # seconds  # Assumed

# WETTED AREA
Swet = S_div_Swet * wing_area

# AERODYNAMIC PARAMETERS
coef_equiv_fric = 0.00264                               # Reader page 105 - fig. 6.3
coeff_zero_lift_drag = coef_equiv_fric * S_div_Swet     # Reader page 104 eq. 6.15
parasite_drag = 0.0075                                  # Reader page 106
span_eff = 0.97                                         # Reader page 106
oswald = 1/(math.pi * aspect_ratio * parasite_drag + 1/span_eff)                    # Reader page 106 eq. 6.17
L_div_D = 0.5*math.sqrt((math.pi * aspect_ratio * oswald)/coeff_zero_lift_drag)     # Reader page 102 eq. 6.12

# PROPULSION PARAMETERS
bypass = 9.61       # From engine selection WP3.1
TSFC = 13.5e-6      # From engine selection WP3.1

# CRUISE CONDITIONS
Cruise_temp = 216.65  # K
Cruise_sos = math.sqrt(1.4*287*Cruise_temp)
Cruise_mach_speed = 0.82
Cruise_speed = Cruise_mach_speed * Cruise_sos  # m/s
fuel_specific_energy = 43e6  # Reader page 109 example 6.3
e_fxn_engxn_p = Cruise_speed/TSFC  # Reader page 109 eq. 6.21
engine_eff = e_fxn_engxn_p/fuel_specific_energy  # Reader page 109

# RANGE CALCULATIONS
R_lost = (1/0.7) * L_div_D * (cruise_height + ((pow(Cruise_speed, 2))/(2*9.81)))  # Reader page 111 eq. 6.24
R_eq = (Design_range + R_lost) * (1+f_con) + 1.2 * R_div + endurance_time * Cruise_speed  # Reader page 111 eq. 6.25 # m
exponent = -R_eq/(engine_eff * (fuel_specific_energy/9.81) * L_div_D)

# –– MASS ––
# FUEL MASS FRACTION
FMR = round(1 - pow(math.e, exponent), 4)  # Reader page 101 eq. 6.5
print("Fuel mass fraction is:", FMR)


# -------------|| Class II Weight estimation - Torenbeek ||-------------
# -----| INPUT |-----
# --| Basic geometry and factors |--
b = 56.49 * conv_d              # Wingspan
T_ratio = 0.3                   # Taper ratio
C_r = 8.69 * conv_d             # Root chord length
Ang_LE = 30.83 * pi/180
Ang_c2 = atan(tan(Ang_LE) - C_r/b * (1-T_ratio))
b = 56.49 * conv_d              # Wingspan
S = 319.1 * conv_d ** 2         # Wing area
t_r = 0.1194*C_r                # Maximum thickness of wing root chord
n_ult = 2.5*1.5                 # Ultimate load factor = load factor * 1.5, looks like its 2.5

# --| Tail geometry |--
S_h = 70.98 * conv_d**2
S_v = 67.90 * conv_d**2
Ang_c2h = 0.39
Ang_c2v = 0.236
V_D = 300                       #--knots--    # Design dive speed, KEAS

# --| Fuselage geometry |--
w_f = 5.78 * conv_d             # Maximum fuselage width
h_f = 5.78 * conv_d             # Maximum fuselage height
l_h = 30.65 * conv_d            # Distance from wing c/4 to HTail c/4
S_fgs = 1900 * conv_d**2        # Fuselage gross shell area

# --| Other |--
T_TO = 640000/4.448             # Total required take-off thrust - from WP3.1


# -----| Calculations |-----
# --| Horizontal tail |--
# Torenbeek empennage and Fuselage Weight estimations for transport airplanes with design dive speeds above 250kts
K_h = 1.1  # For a variable incidence stabilizer
HTailW = K_h * S_h * (3.81 * (S_h**0.2 * V_D)/(1000*(cos(Ang_c2h))**0.5) - 0.287)

# --| Vertical tail |--
K_v = 1  # For fuselage mounted HTail
VTailW = K_v * S_v * (3.81 * (S_v**0.2 * V_D)/(1000*(cos(Ang_c2v))**0.5) - 0.287)

# --| Fuselage |--
K_f = 1.08 * 1.07  # Pressurized fuselage and fuselage with a main gear attached
FusW = 0.021 * K_f*(V_D * l_h/(w_f + h_f))**0.5 * S_fgs**1.2

# --| Nacelle |--
# Torenbeek Nacelle Weight estimation method
NacW = 0.065 * T_TO
# --| Engine |--
eng_w = 7.28 * 10**3/conv_w


# --| Wing |--
# ------------------|| Class I - II Iteration ||------------------
# --| Intermediate |--
W_AllButWing = HTailW + VTailW + FusW + NacW + eng_w

# --| Iteration |--
running = True
x = 0
iterations_count = 0
while running:

    # Class I
    EMTOR_0 = 0.4841                    # Empty to Max Take Off Ratio
    EMTOR_th = round(EMTOR_0 + x, 5)
    WMTO = Payload_mass / (1 - EMTOR_th - FMR) + 731
    WEmpty_0 = (EMTOR_0 * WMTO)/conv_w  # lbs
    WFuel = (FMR * WMTO)/conv_w         # lbs
    WingWeight_0 = WEmpty_0 - W_AllButWing  # Wing Weight based on Class I est.

    # Class II
    W_TO = WMTO/conv_w                  # Take-off weight
    W_F = WFuel/conv_w                  # Fuel weight
    W_MZF = W_TO - W_F                  # Maximum zero fuel weight
    # Torenbeek Wing Weight estimation method for transport airplanes with take-off weights above 12 500 lbs (accounts for HLDs and ailerons)
    WingWeight = 0.0017 * W_MZF * (b/cos(Ang_c2))**0.75 * (1 + (6.3*cos(Ang_c2)/b)**0.5) * n_ult**0.55 * (b*S/(t_r * W_MZF*cos(Ang_c2)))**0.3
    WingWeight *= 0.95                  # Correction as airplane has 2 wing-mounted engines
    WingWeight *= 1.02                  # Correction as airplane has Fowler flaps
    WEmpty = WingWeight + W_AllButWing  # Empty mass based on Class II - Torenbeek
    EMTOR_N = round(WEmpty/WMTO, 5)     # Empty mass to Max Take off ratio based on Torenbeek - generally higher than _i
    Margin = (EMTOR_N - EMTOR_th) / EMTOR_th    # ratio of how much we're off (needs to be below perc_tol)
    print("th Mass ratio is:", EMTOR_th)        # print to check
    print("Class II mass ratio is:", EMTOR_N)   # "
    print("Margin is:", round(Margin, 5))       # "
    print()
    if abs(Margin) >= perc_tol:         # is not smaller, so need to keep looping
        x += 100/54674
        iterations_count += 1
        if iterations_count >= 50:
            print("Could not converge to a value after 50 iterations")
            running = False
        else:
            running = True
    else:
        print("The values converge after", iterations_count, "iterations")
        WingWeight_F = WingWeight
        EMTOR_F = (EMTOR_th + EMTOR_N) / 2  # take average of those two
        WMTO_F = Payload_mass / (1 - EMTOR_F - FMR) + 731
        WEmpty_F = (EMTOR_F * WMTO_F)/conv_w  # lbs
        WFuel = (FMR * WMTO_F)/conv_w  # lbs

        running = False

print()
# ---| Results |---
print("----| Converged values for the weight estimations |----")
print("Empty- to Max take off mass ratio is", round(EMTOR_F, 4))
print("Maximum take off mass is", int(WMTO_F), "kg")
print("Empty mass is", int(WEmpty_F), "lbs", "or", int(WEmpty_F*conv_w), "kg")
print("Fuel mass is", int(WFuel), "lbs, or", int(WFuel*conv_w), "kg")
print()
Tot_weight = WingWeight + HTailW + VTailW + FusW + NacW + eng_w
print("Wing weight is:", int(WingWeight_F), "lbs, or", int(WingWeight_F*conv_w), "kg")
print("Horizontal Tail weight is:", int(HTailW), "lbs, or", int(HTailW*conv_w), "kg")
print("Vertical Tail weight is:", int(VTailW), "lbs, or", int(VTailW*conv_w), "kg")
print("Fuselage weight is:", int(FusW), "lbs, or", int(FusW*conv_w), "kg")
print("Nacelle weight is:", int(NacW), "lbs, or", int(NacW*conv_w), "kg")
print("Engine weight is:", int(eng_w), "lbs, or", int(eng_w*conv_w), "kg")
print("Total empty weight is:", int(Tot_weight), "lbs, or", int(Tot_weight*conv_w), "kg")
