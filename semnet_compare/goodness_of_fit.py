"""
This script runs a Jupyter notebook to fetch graph data. 
It has to be run in the following way from the console:
    $ ipython goodnes_of_fit.py
"""
import numpy as np
import multiprocessing as mp
import powerlaw
import os
import sys
import pandas as pd

from IPython import get_ipython
ipython = get_ipython()


def strip(edges):
    if len(edges[0]) == 2:
        return edges
    else:
        return [(x, y) for x, y, _ in edges]


def goodness_of_fit(degrees, name):
    epsilon = 0.01  # determines the accuracy of the p-value
    nr_sets = int(0.25*epsilon**(-2))

    ks_statistics = np.zeros(nr_sets)

    # original power-law estimate
    original = powerlaw.Fit(degrees, discrete=True)

    keep_stderr = sys.stderr  # powerlaw package prints to stderr
    with open(os.devnull, 'w') as f:
        sys.stderr = f

        for i in range(nr_sets):
            theoretical_distributon = powerlaw.Power_Law(
                xmin=original.xmin,  # xmax=original.xmax,
                parameters=[original.alpha], discrete=True)

            simulated_data = theoretical_distributon.generate_random(
                    5018, estimate_discrete=True)

            new_fit = powerlaw.Fit(simulated_data, discrete=True)
            ks_statistics[i] = new_fit.power_law.KS()

    sys.stderr = keep_stderr   # reverse re-direct
    p = np.sum(ks_statistics > original.power_law.KS())/nr_sets
    print(name, p)
    return (name, p)


if __name__ == "__main__":

    # Load graphs from the Jupyter Notebook, for this to work
    # run this script with IPython
    ipython.magic("run '../notebooks/create-final-graphs.ipynb'")

    with mp.Pool(processes=mp.cpu_count()) as pool:
        res = pool.starmap(
                goodness_of_fit,
                zip(degrees.values(), degrees))

    df = pd.Series(dict(res))
    df.to_csv('results/gof_test.csv')
