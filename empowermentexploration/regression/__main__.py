import time

from empowermentexploration.regression.model_values import ModelValues
from empowermentexploration.regression.player_data import PlayerData

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: SET APPROPRIATE VARIABLES
    # set source (either 'human' or any selection from 'base', 'emp', 'bin', 'trueemp', 'truebin', 'cbv', 'sim' or 'cbu')
    data_source = 'human'

    # set memory type: 0 = no memory, 1 = full memory, 2 = fading memory
    memory_type = 1

    # set game version: alchemy1, alchemy2, tinypixels, tinyalchemy
    game_version = 'tinyalchemy'

    # set vector version
    split_version = 'data'
    vector_version = 'crawl300'

    #set empowerment version to 'elements' for original calculation and 'values' for model directly trained on empowerment values
    #!!! Have to change empowerment file in resources/costumgametree/data to the one that should be used
    emp_version = 'elements' # 'elements' or 'values'

    #Do you want to match the random combinations to the success of the chosen combinations
    matched = False

    stepsused = None #None for using all
    # YOUR ACTION IS NOT RECQUIRED ANYMORE

    # set time stamp
    time = time.strftime('%Y%m%d-%H%M')

    # plot info for user
    print('\nGet regression data for player data from {}. Save logs to directory empowermentexploration/data/regression/'.format(game_version))

    # load player data
    players = PlayerData(game_version, data_source=data_source, memory_type=memory_type)
    players.get_player_subset(n_players=None, steps=stepsused, seed=None)

    # generate new dataframe with info on values of different model strategies
    values = ModelValues(players.data, time, game_version, split_version, vector_version, data_source, memory_type, matched, emp_version, z_score=False)
