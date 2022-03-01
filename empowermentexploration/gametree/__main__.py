import time

import empowermentexploration.utils.info_logs as log
import pandas as pd
from empowermentexploration.gametree.cross_validation import CrossValidation

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: SET APPROPRIATE VARIABLES
    # set game version: 'alchemy2', 'alchemy1', 'joined', 'tinyalchemy', 'tinypixels'
    game_version = 'tinyalchemy'

    # set vector version: split on 'data' or 'element', use vector version 'ccen', 'wiki or 'crawl' and dimension 100 or 300 (check what is available)
    split_version = 'data'
    vector_version = 'crawl'
    dim = 300

    # set number of cross validation splits
    k = 10

    # other variables e.g. epochs etc. have to be set in the class call below
    # YOUR ACTION IS NOT RECQUIRED ANYMORE

    # rewrite split_version:
    if split_version == 'data':
        exclude_elements_test = False
        exclude_elements_val = False
    elif split_version == 'element':
        exclude_elements_test = True
        exclude_elements_val = True
    else:
        raise ValueError('Undefined version: "{}". Use "data" or "element" instead.'.format(split_version))

    # create directory to log info from this run
    time = time.strftime('%Y%m%d-%H%M')
    log.create_directory('empowermentexploration/data/gametree/{}/'.format(time))

    # plot info for user
    print('\nRun models. Save logs to directory empowermentexploration/data/gametree/{}'.format(time))

    # run link prediction model
    print('\nRun link prediction model.')
    link_prediction = CrossValidation(k, time, game_version=game_version, link_prediction=True, epochs=100, steps_per_epoch=30,
                                      exclude_elements_test=exclude_elements_test, exclude_elements_val=exclude_elements_val, manual_validation=0.2,
                                      oversampling=1.0, vector_version=vector_version, dim=dim)
    log.log_model_info(link_prediction, mode=3, mode_type='{}LinkPred'.format(game_version), time=time)
    link_prediction.run_cross_validation()

    # run element prediction model
    print('\nRun element prediction model.')
    element_prediction = CrossValidation(k, time, game_version=game_version, link_prediction=False, epochs=15, batch_size=32,
                                         exclude_elements_test=exclude_elements_test, exclude_elements_val=exclude_elements_val, manual_validation=0.2,
                                         vector_version=vector_version, dim=dim)
    log.log_model_info(element_prediction, mode=3, mode_type='{}ElemPred'.format(game_version), time=time)
    element_prediction.run_cross_validation()

    # join results
    print('\nJoin model results.')
    link_prediction_table = pd.read_csv('empowermentexploration/data/gametree/{}/{}LinkPredTable-{}-{}{}.csv'.format(time, game_version, split_version, vector_version, dim))
    element_prediction_table = pd.read_csv('empowermentexploration/data/gametree/{}/{}ElemPredTable-{}-{}{}.csv'.format(time, game_version, split_version, vector_version, dim))

    # delete columns with true value
    link_prediction_table = link_prediction_table.drop(['trueSuccess', 'trueResult'], axis=1)
    element_prediction_table = element_prediction_table.drop(['trueSuccess', 'trueResult'], axis=1)

    # set index
    link_prediction_table = link_prediction_table.set_index(['first', 'second'])
    element_prediction_table = element_prediction_table.set_index(['first', 'second'])

    # merge for duplications, get mean of the values
    link_prediction_table = link_prediction_table.groupby(link_prediction_table.index).mean()
    element_prediction_table = element_prediction_table.groupby(element_prediction_table.index).mean()
    
    # merge both tables
    gametree_table = link_prediction_table.join(element_prediction_table, how='outer')
    gametree_table.index = pd.MultiIndex.from_tuples(gametree_table.index)
    gametree_table.index.names = ['first', 'second']

    # add column 'predResult'
    if game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
        elements = 540
    elif game_version == 'alchemy2':
        elements = 720
    elif game_version == 'joined':
        n_elements = 738
    gametree_table['predResult'] = gametree_table[gametree_table.columns[-elements:]].idxmax(axis='columns').astype(int)

    # write resulting table to file
    print('\nWrite to HDF5 file.')
    gametree_table.to_hdf('empowermentexploration/data/gametree/{}/{}GametreeTable-{}-{}{}.h5'.format(time, game_version, split_version, vector_version, dim), key='gametreeTable', mode='w')

    print('\nDone.')
