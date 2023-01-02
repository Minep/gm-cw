import numpy as np
import pandas as pd
import sys

def counter(sequence, i, j):
    """
    Given a sequence, find the number of times where vt = i, vt-1 = j
    """
    count = 0
    for index in range(sequence.shape[0]-1):
        if sequence[index] == j and sequence[index+1] == i:
            count += 1
    return count

def likelihood(p_h_new, p_v1_h, T):
    like = 0
    for i in range(data.shape[0]):
        v1_index = int(data[i, 0])
        marginal = 0
        for k in range(3):
            rest = 1
            for j in range(1, data.shape[1]):
                vj_index = int(data[i,j])
                vj_prev = int(data[i,j-1])
                rest *= T[k][vj_index, vj_prev]
            marginal += p_h_new[k] * p_v1_h[v1_index, k] * rest
        like += np.log(marginal)
    return like

def EM(data):
    """
    Model the three station sequence as three markov chain with different transition/emission matrix
    """
    # number of sequences
    N = data.shape[0]

    for interatoin in range(10):
        # initialize T for 3 hidden stations (h, vt, vt-1)
        T = []
        for i in range(3):
            Ti = np.random.randint(low=1, high = 10, size=(3,3))
            Ti = Ti / np.sum(Ti, axis = 0)
            T.append(Ti)

        # initialize first term v1 (v1, h)
        p_v1_h = np.random.randint(low=1, high = 10, size=(3,3))
        p_v1_h = p_v1_h / np.sum(p_v1_h, axis = 0)
        
        # initialize p(h | v^n 1:T)
        p_h_vn = np.random.randint(low=1, high = 10, size=(N, 3))
        p_h_vn = p_h_vn / np.sum(p_h_vn, axis=1).reshape((N,1))

        old_l = -np.inf
        for x in range(20):
            p_h_new = np.sum(p_h_vn, axis = 0)
            p_h_new = p_h_new / np.sum(p_h_new)

            for k in range(len(T)):
                for i in range(T[k].shape[0]):

                    for j in range(T[k].shape[1]):
                        count = np.zeros((N, 1))
                        for n in range(N):
                            count[n] = counter(data[n], i, j)
                        T[k][i,j] = p_h_vn[:, k].dot(count)
                    
                    count_first = np.zeros((N, 1))
                    for n in range(N):
                        count_first[n] = (data[n, 0] == i)
                    p_v1_h[i,k] = p_h_vn[:, k].dot(count_first)

            # normalize T and p_v1_h
            for i in range(3):
                T[i] = T[i] / np.sum(T[i], axis = 0)
            p_v1_h = p_v1_h / np.sum(p_v1_h, axis=0)

            # e_step
            for n in range(N):
                for k in range(3):
                    v1 = int(data[n, 0])
                    product = p_h_new[k] * p_v1_h[v1,k]
                    for t in range(data.shape[1]-1):
                        product *= T[k][int(data[n,t+1]), int(data[n,t])]
                    p_h_vn[n,k] = product

            # normalize
            p_h_vn = p_h_vn / np.sum(p_h_vn, axis=1).reshape((N,1))

            # calculate likelihood to test convergence
            new_l = likelihood(p_h_new, p_v1_h, T)
            if new_l - old_l < 0.01:
                break
            old_l = new_l
            print(".", end='')
            sys.stdout.flush() 
        # test global maximum
        if new_l >= -45300:
            break

    print("\np_h:")
    print(p_h_new)
    print("T:")
    print(T)
    print("v1:")
    print(p_v1_h)

    print("log likelihood of the data:")
    # prod(i rows) { sum(all H) p(H) x p(vi,1|H) x prod(jth column) [p(vi,j | vi,j-1, TH)] } 
    print(likelihood(p_h_new, p_v1_h, T))

    print("post: ")
    print(p_h_vn[:10].round(5))

def EM_uniform(data):
    """
    Model the three station sequence as three markov chain with different transition/emission matrix
    """
    # number of sequences
    N = data.shape[0]

    # initialize T for 3 hidden stations (h, vt, vt-1)
    T = []
    for i in range(3):
        Ti = np.full((3,3),1)
        Ti = Ti / np.sum(Ti, axis = 0)
        T.append(Ti)

    # initialize first term v1 (v1, h)
    p_v1_h = np.full((3,3),1)
    p_v1_h = p_v1_h / np.sum(p_v1_h, axis = 0)
    
    # initialize p(h | v^n 1:T)
    p_h_vn = np.full((N,3),1)
    p_h_vn = p_h_vn / np.sum(p_h_vn, axis=1).reshape((N,1))

    for x in range(20):
        p_h_new = np.sum(p_h_vn, axis = 0)
        p_h_new = p_h_new / np.sum(p_h_new)

        for k in range(len(T)):
            for i in range(T[k].shape[0]):

                for j in range(T[k].shape[1]):
                    count = np.zeros((N, 1))
                    for n in range(N):
                        count[n] = counter(data[n], i, j)
                    T[k][i,j] = p_h_vn[:, k].dot(count)
                
                count_first = np.zeros((N, 1))
                for n in range(N):
                    count_first[n] = (data[n, 0] == i)
                p_v1_h[i,k] = p_h_vn[:, k].dot(count_first)

        # normalize T and p_v1_h
        for i in range(3):
            T[i] = T[i] / np.sum(T[i], axis = 0)
        p_v1_h = p_v1_h / np.sum(p_v1_h, axis=0)

        # e_step
        for n in range(N):
            for k in range(3):
                v1 = int(data[n, 0])
                product = p_h_new[k] * p_v1_h[v1,k]
                for t in range(data.shape[1]-1):
                    product *= T[k][int(data[n,t+1]), int(data[n,t])]
                p_h_vn[n,k] = product

        # normalize
        p_h_vn = p_h_vn / np.sum(p_h_vn, axis=1).reshape((N,1))

        print(".", end='')
        sys.stdout.flush() 

    print("\np_h:")
    print(p_h_new)
    print("T:")
    print(T)
    print("v1:")
    print(p_v1_h)

    print("log likelihood of the data:")
    # prod(i rows) { sum(all H) p(H) x p(vi,1|H) x prod(jth column) [p(vi,j | vi,j-1, TH)] } 
    print(likelihood(p_h_new, p_v1_h, T))

    print("post: ")
    print(p_h_vn[:10].round(5))



if __name__ == "__main__":
    data = np.loadtxt("meteo1.csv")
    EM(data)