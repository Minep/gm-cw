import numpy as np

def get_sample(n):
    """
    
    Generates n random samples of values -1 and 1 in a 2d array.

    @param n: number of samples to generate

    @return: 2d array of shape (n, n) containing samples
    """
    return np.random.choice([-1, 1], size=(n, n))

def get_neighbours(i, j, shape = (10, 10)):
    """
    
    Returns the indices of the neighbours of the element at position (i, j) in a 2d array of shape (n, m).

    @param i: row index
    @param j: column index
    @param shape: shape of the 2d array

    @return: list of indices of neighbours
    """
    neighbours = [[i + 1, j], [i - 1, j], [i, j + 1], [i, j - 1]] # list of possible neighbours

    # remove neighbours that are out of bounds
    neighbours = [neighbour for neighbour in neighbours if neighbour[0] >= 0 and neighbour[0] < shape[0] and neighbour[1] >= 0 and neighbour[1] < shape[1]]

    return neighbours

def conditional(beta, sample, i, j):

    """
    
    Defines the conditional probability of the element at position (i, j) given the rest of the array.

    @param beta: inverse temperature

    @param sample: 2d array of shape (n, n) containing samples

    @param i: row index

    @param j: column index

    @return: conditional probability of the element at position (i, j)
    """
    
    neighbours = get_neighbours(i, j, sample.shape) # get indices of neighbours

    energy = sum([sample[i, j] == sample[k, l] for (k, l) in neighbours]) # calculate energy

    return np.exp(-beta * energy) # return conditional probability

def gibbs_sampling(n, beta, runs = 1000, burn_in = 100, nth = 10):

    """
    
    Performs Gibbs sampling on a 2d array of shape (n, n) with beta as the inverse temperature.

    @param n: number of samples to generate

    @param beta: inverse temperature

    @param runs: number of runs to perform

    @param burn_in: number of runs to discard

    @param nth: only keep every nth sample
    
    """

    sample = get_sample(n) # generate samples

    samples = [np.copy(sample)] # store samples

    for _ in range(runs): # perform runs

        for _ in range(sample.size): # iterate over rows

            (i, j) = np.unravel_index(np.random.randint(sample.size), sample.shape) # pick a random element

            p = conditional(beta, sample, i, j) # calculate conditional probability

            # print("P: {}".format(p))

            if np.random.rand() < p: # flip element with probability p

                sample[i, j] *= -1
    
        samples.append(np.copy(sample)) # store samples

    return samples[burn_in::nth] # return samples
    

betas = [0.01, 1, 4]

for beta in betas:

    samples = gibbs_sampling(10, beta) # perform Gibbs sampling

    # print(type(samples))

    num_samples = len(samples) # number of samples

    if num_samples != 0:

        index00, index01, index10, index11 = 0, 0, 0, 0 # counters for each configuration

        for sample in samples:

            if sample[0, 9] == -1 and sample[9, 9] == -1:
                index00 += 1
            elif sample[0, 9] == -1 and sample[9, 9] == 1:
                index01 += 1
            elif sample[0, 9] == 1 and sample[9, 9] == -1:
                index10 += 1
            elif sample[0, 9] == 1 and sample[9, 9] == 1:
                index11 += 1

        print("Beta: {}".format(beta))
        print("P(00): {}".format(index00 / num_samples))
        print("P(01): {}".format(index01 / num_samples))
        print("P(10): {}".format(index10 / num_samples))
        print("P(11): {}".format(index11 / num_samples))