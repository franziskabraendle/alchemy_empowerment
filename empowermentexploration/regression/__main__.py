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
    # YOUR ACTION IS NOT RECQUIRED ANYMORE

    # set time stamp
    time = time.strftime('%Y%m%d-%H%M')

    # plot info for user
    print('\nGet regression data for player data from {}. Save logs to directory empowermentexploration/data/regression/'.format(game_version))

    # load player data
    players = PlayerData(game_version, data_source=data_source, memory_type=memory_type)
    players.get_player_subset(n_players=None, steps=None, seed=None)

    # generate new dataframe with info on values of different model strategies
    values = ModelValues(players.data, time, game_version, split_version, vector_version, data_source, memory_type, z_score=False)
