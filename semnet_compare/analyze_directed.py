from semnet import SemNet
import multiprocessing as mp

import pandas as pd


def analyze(edgefile, name):
    print('Working on:', name)

    network = SemNet(source=edgefile, directed=True)
    network.do_analyses()

    return pd.Series(network.stats, name=name)


path_edgefiles = [
        '../data/fan/fan_weighted_edges.pkl',
        '../data/word2vec/w2v_fan_directed-cs-cos_edgeset.pkl',
        '../data/word2vec/w2v_fan_directed-cs-dot_edgeset.pkl',
        '../data/word2vec/w2v_fan_directed-knn-cos_edgeset.pkl',
        '../data/word2vec/w2v_fan_directed-knn-dot_edgeset.pkl',
        '../data/glove/glove_fan_directed-cs-cos_edgeset.pkl',
        '../data/glove/glove_fan_directed-cs-dot_edgeset.pkl',
        '../data/glove/glove_fan_directed-knn-cos_edgeset.pkl',
        '../data/glove/glove_fan_directed-knn-dot_edgeset.pkl'
        ]

save_names = ['USF directed', 'word2vec-cs-cos', 'word2vec-cs-dot',
              'word2vec-knn-cos', 'word2vec-knn-dot',
              'glove-cs-cos', 'glove-cs-dot', 'glove-knn-cos',
              'glove-knn-dot']

path_results = './results/directed_results'

if __name__ == "__main__":

    with mp.Pool(processes=mp.cpu_count()) as pool:
        res = pool.starmap(analyze, zip(path_edgefiles, save_names))

    df = pd.concat(res, axis=1)

    df.to_pickle(path_results + '.pkl')
    df.to_csv(path_results + '.csv')

    print('Done', path_results)
