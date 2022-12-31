import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

iterations = 100
shape = (10, 10)

for beta in [0.01, 1, 4]:

    q = np.zeros(shape) # initialise array of probabilities

    for i in range(iterations):

        for j in range(shape[0]):
            for k in range(shape[1]):

                neighbours = get_neighbours(j, k, shape) # get indices of neighbours

                odds = beta * np.sum(2 *q[neighbours] - 1) # calculate odds

                q[j, k] = np.exp(odds) / (1 + np.exp(odds)) # calculate probability

        plt.figure() # create new figure

        sns.heatmap(q, vmin = 0, vmax = 1) # plot heatmap

        plt.title(r'$\beta = {}$'.format(beta)) # set title

        plt.savefig('beta_{}.png'.format(beta)) # save figure