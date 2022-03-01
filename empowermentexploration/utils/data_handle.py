import json

import empowermentexploration.utils.helpers as helpers
import numpy as np
import pandas as pd
import scipy.io


def get_combination_table(version='alchemy2', csv=True):
    """Returns a combination table with four columns:
        (1) first: element index
        (2) second: element index
        (3) success: 0 or 1
        (4) result: element index, if available

    Args:
        version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.
        csv (bool, optional): True if csv version is to be returned, False for json file. Defaults to True.

    Returns:
        DataFrame or dict: Contains information about elements involved in combination.
    """
    if version == 'joined' or version == 'alchemy1' or version == 'alchemy2' or version == 'tinyalchemy' or version == 'tinypixels':
        if csv is True:
            combination_table = pd.read_csv('empowermentexploration/resources/littlealchemy/data/{}CombinationTable.csv'.format(version),
                                dtype={'first': int, 'second': int, 'success': int, 'result': int})
        else:
            with open('empowermentexploration/resources/littlealchemy/data/{}CombinationTable.json'.format(version),
                      encoding='utf8') as infile:
                combination_table = json.load(infile, object_hook=helpers.jsonKeys2int)
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(version))

    return combination_table

def get_elements(version='alchemy2'):
    """Returns elements for given version.

    Args:
        version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.

    Returns:
        list: Elements of the given version.
    """
    if version == 'joined' or version == 'alchemy1' or version == 'alchemy2' or version == 'tinyalchemy' or version == 'tinypixels':
        with open('empowermentexploration/resources/littlealchemy/data/{}Elements.json'.format(version),
                  encoding='utf8') as infile:
            elements = json.load(infile)
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(version))

    return elements

def get_wordvectors(game_version='alchemy2', vector_version='crawl300'):
    """Returns wordvectors for given version.

    Args:
        game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on. Defaults to 'crawl300'.

    Returns:
        ndarray(dtype=float, ndim=2): Word vectors for elements of the given version.
    """
    if game_version == 'joined' or game_version == 'alchemy1' or game_version == 'alchemy2' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
        if vector_version == 'ccen100' or vector_version == 'ccen300' or vector_version == 'crawl100' or vector_version == 'crawl300' or vector_version == 'wiki100' or vector_version == 'wiki300':
            vectors = np.loadtxt('empowermentexploration/resources/littlealchemy/data/{}ElementVectors-{}.txt'.format(game_version, vector_version))
        else:
            raise ValueError('Undefined vector_version: "{}". Use "ccen100", "ccen300", "crawl100", "crawl300", "wiki100" or "wiki300" instead.'.format(vector_version))
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(game_version))

    return vectors

def get_gametree(version='alchemy2'):
    """Returns a (true) game tree depending on the version.

    Args:
        version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.

    Returns:
        dict: Game tree information of the given version.
    """
    if version == 'joined' or version == 'alchemy1' or version == 'alchemy2' or version == 'tinyalchemy' or version == 'tinypixels':
        with open('empowermentexploration/resources/littlealchemy/data/{}Gametree.json'.format(version),
                  encoding='utf8') as infile:
            gametree = json.load(infile)
            gametree = {int(k):v for k,v in gametree.items()}
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(version))

    return gametree

def get_parent_table(version='alchemy2'):
    """Returns a parent table where each parent has its own dict entry consisting of al resulting children.

    Args:
        version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.

    Returns:
        dict: Parent table where each parent has its own dict entry consisting of al resulting children.
    """
    if version == 'joined' or version == 'alchemy1' or version == 'alchemy2' or version == 'tinyalchemy' or version == 'tinypixels':
        with open('empowermentexploration/resources/littlealchemy/data/{}ParentTable.json'.format(version),
                  encoding='utf8') as infile:
            parent_table = json.load(infile)
            parent_table = {int(k):v for k,v in parent_table.items()}
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(version))

    return parent_table

def get_custom_parent_table(game_version='alchemy2', split_version='data', vector_version='crawl300'):
    """Returns a parent table where each parent has its own dict entry consisting of al resulting children.

    Args:
        game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the empowerment info should be based on.
                    Defaults to 'crawl300'.

    Returns:
        dict: Parent table where each parent has its own dict entry consisting of al resulting children.
    """
    if game_version == 'joined' or game_version == 'alchemy1' or game_version == 'alchemy2' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
        with open('empowermentexploration/resources/customgametree/data/{}ChildrenEmpowermentTable-{}-{}.json'.format(game_version, split_version, vector_version),
                  encoding='utf8') as infile:
            parent_table = json.load(infile)
            parent_table = {int(k):v for k,v in parent_table.items()}
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(game_version))

    return parent_table

def get_probability_table(game_version='alchemy2', split_version='data', vector_version='crawl300'):
    """Returns probability table from custom gametree.

    Args:
        game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.

    Returns:
        DataFrame: Probability table from custom gametree. Includes combination elements, true success and result,
                    predicted success and prediction for each element.
    """
    try:
        probability_table = pd.read_hdf('empowermentexploration/resources/customgametree/data/{}GametreeTable-{}-{}.h5'.format(game_version, split_version, vector_version))

        return probability_table
    except:
        raise ValueError('Corresponding custom gametree table not found. Check if input was correct or create the needed table using "empowermentexploration.gametree"')

def get_empowerment_info(game_version='alchemy2', split_version='data', vector_version='crawl300'):
    """Returns empowerment info from custom gametree.

    Args:
        game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what element and combination set is going to be used. Defaults to 'alchemy2'.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the empowerment info should be based on.
                    Defaults to 'crawl300'.

    Returns:
        DataFrame: Empowerment info from custom gametree. Includes combination elements, predicted success
                    and empowerment info for both calculation types (outgoing combination and children).
    """
    try:
        empowerment_info = pd.read_csv('empowermentexploration/resources/customgametree/data/{}EmpowermentTable-{}-{}.csv'.format(game_version, split_version, vector_version),
                                  dtype={'first': int, 'second': int, 'predResult': int, 'empComb': float, 'empChild': float, 'binComb': float, 'binChild': float})

        return empowerment_info
    except:
        raise ValueError('Corresponding empowerment info not found. Check if input was correct or create the needed info using "empowermentexploration.resources.customgametree"')

def get_player_data(version='alchemy2', memory = True):
    """Returns player data for given version. Player data is already cleansed of doubling combinations.

    Args:
        version (str, optional): 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                    States what player data set set is going to be used. Defaults to 'alchemy2'.
        memory (boolean, optional): True if memory version of data is going to be used, False otherwise. Defaults to True.

    Returns:
        DataFrame: Player data.
    """
    if version == 'alchemy1' or version == 'alchemy2' or version == 'tinyalchemy' or version == 'tinypixels':
        if memory is True:
            memory = 'Memory'
        else:
            memory = ''
        player_data = pd.read_csv('empowermentexploration/resources/playerdata/data/{}HumanData{}.csv'.format(version, memory))
    else:
        raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy" or "tinypixels" instead.'.format(version))

    return player_data

def get_gameprogress_data(time, game_version, model, memory_type):
    """Returns model data from game progress.

    Args:
        time (str): Time at which data was generated.
        game_version (str): 'alchemy1', 'alchemy2', 'joined', 'tinyalchemy' or 'tinypixels'.
                    States what player data set set is going to be used.
        model (str): Model that the plots are for.
        memory_type (int): Memory type that was used for data generation. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 10 steps)
    Returns:
        ndarray(dtype=float, ndim=2): Arrays containing data from game progress
    """
    try:
        gameprogress_data = scipy.io.loadmat('empowermentexploration/data/models/{}/{}-{}-memory{}-inventory.mat'.format(time, game_version, model, memory_type))

        return gameprogress_data
    except:
        raise ValueError('Corresponding gameprogress data not found. Check if input was correct.')


def get_regression_data(time, game_version, model, z_score, memory_type ):
    """Returns data for regression including model differences.

    Args:
        time (str): Time at which data was generated.
        game_version (str): 'alchemy1', 'alchemy2', 'joined', 'tinyalchemy' or 'tinypixels'.
                    States what player data set set is going to be used.
        model (str): Model type, which is either 'human' or any selection from 'base', 'emp', 'bin', 'trueemp',
                    'truebin', 'cbv', 'sim' or 'cbu' if data is generated for simulated data.
        z_score (boolean): True if z score for model differences should be caculated, False otherwise.
        memory_type (int): Memory type that was used for data generation. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 10 steps)

    Returns:
        DataFrame: Player data.
    """
    try:
        if z_score is True:
            z_score = '-scaled'
        else:
            z_score = ''
        regression_data = pd.read_csv('empowermentexploration/data/regression/{}-{}-valuedifferences-{}{}-{}.csv'.format(time, game_version, model, z_score, memory_type))

        return regression_data
    except:
        raise ValueError('Corresponding regression data not found. Check if input was correct.')

def get_simulation_data(game_version, model, memory_type):
    """Returns simulation data for given version.

    Args:
        game_version (str): 'alchemy1', 'alchemy2', 'joined', 'tinyalchemy' or 'tinypixels'.
                    States what player data set set is going to be used.
        model (str): Model type, which is either 'base', 'emp', 'bin', 'trueemp',
                    'truebin', 'cbv', 'sim' or 'cbu'.
        memory_type (int): Memory type that was used for data generation. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 10 steps)

    Returns:
        DataFrame: Simulation data.
    """
    try:
        simulation_data = pd.read_csv('empowermentexploration/resources/playerdata/data/reference/{}{}Combinations-memory{}.csv'.format(game_version, model, memory_type))

        return simulation_data
    except:
        raise ValueError('Corresponding simulation data not found. Check if input was correct.')
