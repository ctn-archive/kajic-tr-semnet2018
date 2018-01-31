import os
import os.path

import pandas as pd


def load_free_association_data(min_resp=2, column='FSG',
                               return_strength=True):
    """Loads the free association data stored in ../data/fan.
    The data should be downloaded manually into that directory from:
    http://w3.usf.edu/FreeAssociation/AppendixA/

    Parameters
    ----------
    min_resp : int
        Load association pairs which were produced by at leat `min_resp`
        participant
    column : str, optional
        Column in the data files that gives the association strength. Use 'FSG'
        for forward strength and 'BSG' for backward strength.

    Returns
    -------
    A tuple (words, association_database) where words is a set of all occuring
    words (either as cue or target) and association_database is a list of
    associations. Each association is a tuple (cue, target, strength).
    """
    normed_responses = 0
    words = set()
    association_database = []

    path = os.path.join(os.pardir, 'data', 'fan')

    # check all files have been downloaded
    filenames = [
            'Cue_Target_Pairs.A-B',
            'Cue_Target_Pairs.C',
            'Cue_Target_Pairs.D-F',
            'Cue_Target_Pairs.G-K',
            'Cue_Target_Pairs.L-O',
            'Cue_Target_Pairs.P-R',
            'Cue_Target_Pairs.S',
            'Cue_Target_Pairs.T-Z']

    for filename in filenames:
        assert os.path.isfile(os.path.join(path, filename)), \
                filename + " not found in " + path

    for filename in filenames:
        df = pd.read_csv(
            os.path.join(path, filename), skipinitialspace=True,
            comment='<',  # comment='<' is a hackish way to skip HTML tags
            encoding='windows-1252')
        df[column] = pd.to_numeric(df[column])

        df_normed = df[df['NORMED?'] == 'YES']
        df_normed = df_normed[df_normed['#P'] >= min_resp]
        normed_responses += len(df_normed)

        # extract norms
        for _, row in df_normed.iterrows():
            cue, target = row['CUE'].upper(), row['TARGET'].upper()
            words.add(cue)
            words.add(target)

            if return_strength:
                strength = row[column]
                association_database.append((cue, target, strength))
            else:
                association_database.append((cue, target))

    assert len(words) == 5018, "Number words should be 5018."
    assert normed_responses == 63619, \
        "Number of normed responses should be 63619"

    return words, association_database
