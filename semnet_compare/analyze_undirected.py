from semnet import SemNet
import multiprocessing as mp

import pandas as pd


def analyze(edgefile, name):
    print('Working on:', name)

    network = SemNet(source=edgefile, directed=False)
    network.do_analyses()

    return pd.Series(network.stats, name=name)


path_edgefiles = [
        '../data/fan/fan_weighted_edges.pkl',
        '../data/word2vec/w2v_fan_0.38_cos_edgeset.pkl',
        '../data/word2vec/w2v_fan_4.20_dot_edgeset.pkl',
        '../data/glove/glove_fan_0.53_cos_edgeset.pkl',
        '../data/glove/glove_fan_22.70_dot_edgeset.pkl'
        ]

save_names = ['USF undirected', 'word2vec-cos', 'word2vec-dot',
              'glove-cos', 'glove-dot']
path_results = './results/undirected_results'

if __name__ == "__main__":

    with mp.Pool(processes=mp.cpu_count()) as pool:
        res = pool.starmap(analyze, zip(path_edgefiles, save_names))

    df = pd.concat(res, axis=1)

    df.to_pickle(path_results + '.pkl')
    df.to_csv(path_results + '.csv')

    print('Done', path_results)
