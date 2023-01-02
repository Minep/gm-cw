import numpy as np
import math

def time(minutes, hours = None):
    # min -> hours
    if hours == None:
        return [minutes // 60, minutes % 60]
    # hours -> mins
    else:
        return [0, hours*60 + minutes]

def part_a():
    p_d = {
        0: 0.7,
        5: 0.8,
        10: 0.9,
        15: 0.97,
        20: 0.99
    }
    N = [3, 5, 10]
    depart_time = time(minutes = 5, hours=21)[1]
    T0 = []
    print("\n part a: ")
    for n in N:
        for t in p_d.keys():
            marginal = p_d[t] ** n
            if marginal >= 0.9:
                print("for n = ", n, " need to ask ", t, " minutes earlier.")
                time_in_mins = depart_time - t
                T0.append(time(time_in_mins))
                break
    print(T0)

def part_b():
    
    p_d = {
        0: 0.7,
        5: 0.8,
        10: 0.9,
        15: 0.97,
        20: 0.99
    }
    p_d_z = {
        0: 0.5,
        5: 0.7,
        10: 0.8,
        15: 0.9,
        20: 0.95
    }
    p_z = 2/3
    # p(d) = sum_{z} p(d|z)*p(z)
    N = [3, 5, 10]
    T = [15, 20, 20]
    print("\n part b: ")
    for n, t in zip(N, T):
            p_on_time = (p_z * p_d[t] + (1-p_z) * p_d_z[t])**n
            print(1 - p_on_time)

def binomial(p, all, true):
    comb = math.factorial(all)/(math.factorial(true) * math.factorial(all-true)) 
    p = comb * p**true * (1-p)**(all-true)
    return p

def bonus():
    """
    Calculate p(X|miss) = p(X) * p(miss|X) / p(miss)
    X -> number of friends not punctual
    """
    # at N = 5, part a gives 20 minutes in advance
    p_d = 0.99
    p_d_z = 0.95
    # prior of x friends not punctual p(X=x)
    X = [0, 1, 2, 3, 4, 5]
    all = len(X) - 1
    p_not_punctual = 1/3
    p_x = [binomial(p_not_punctual, all, x) for x in X]

    # likelihood p(miss|X) = 1 - p(ontime|X)
    p_miss_x = [1 - p_d**(all - x) * p_d_z**x for x in X]

    # p(miss)
    p_miss = 1 - ((1 - p_not_punctual) * p_d + p_not_punctual * p_d_z)**5

    p_x_miss = np.multiply(p_x, p_miss_x) / p_miss

    print("\n bonus: ")
    print(p_x_miss)


if __name__ == "__main__":
    part_a()
    part_b()
    bonus()
