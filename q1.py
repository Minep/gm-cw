import math
import numpy as np

S = 2000
N = 30

def s_prior(x, y):
    return 1 / S

def p_v_s1_s2(v, d1, d2):
    c = (v - (1 / (d1 + 0.1) + 1 / (d2 + 0.1))) / 0.25
    return 1 / (0.25 * math.sqrt( 2 * math.pi)) * math.exp(-0.5 * c * c)

def prepare_data():
    station_readings = []
    station_loc = []
    loc = []
    with open("EarthquakeExerciseData.txt") as dat:
        obs = dat.readlines()
        for i, v in enumerate(obs):
            theta = 2 * math.pi * (i + 1) / 30
            v = float(v.strip())
            station_readings.append(v)
            station_loc.append(np.array([math.cos(theta), math.sin(theta)]))
    for i in range(1, S + 1):
        theta = 25 * 2 * math.pi * i / S
        r = i / S
        pos = r * np.array([math.cos(theta), math.sin(theta)])
        loc.append(pos)

    return (np.array(station_readings), np.array(station_loc), np.array(loc))

def p_v_table(V, V_loc, S_loc):
    T = np.zeros(S, S, N)
    for i in range(S):
        for j in range(S):
            for k in range(V):
                d1 = V_loc[k] - S_loc[i]
                d2 = V_loc[k] - S_loc[j]
                T[i,j,k] = p_v_s1_s2(V[k], d1 @ d1.T, d2 @ d2.T)

    return T