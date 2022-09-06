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

    #set version to element (using the main empowerment calculation afterwards) or empowerment (directly training on the empowerment values)
    model_version = 'element'

    # set number of cross validation splits
    #k = 10
    k=10

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

    #prediction_model: 0-link prediction, 1-element prediction, 2-empowerment prediction
    # plot info for user
    print('\nRun models. Save logs to directory empowermentexploration/data/gametree/{}'.format(time))

    #run link prediction model
    print('\nRun link prediction model.')
    link_prediction = CrossValidation(k, time, game_version=game_version, prediction_model=0, epochs=100, steps_per_epoch=30,
                                      exclude_elements_test=exclude_elements_test, exclude_elements_val=exclude_elements_val, manual_validation=0.2,
                                      oversampling=1.0, vector_version=vector_version, dim=dim)
    log.log_model_info(link_prediction, mode=3, mode_type='{}LinkPred'.format(game_version), time=time)
    link_prediction.run_cross_validation()

    if model_version == 'element':
    #run element prediction model
        print('\nRun element prediction model.')
        element_prediction = CrossValidation(k, time, game_version=game_version, prediction_model=1, epochs=15, batch_size=32,
                                            exclude_elements_test=exclude_elements_test, exclude_elements_val=exclude_elements_val, manual_validation=0.2,
                                            vector_version=vector_version, dim=dim)
        log.log_model_info(element_prediction, mode=3, mode_type='{}ElemPred'.format(game_version), time=time)
        element_prediction.run_cross_validation()

    elif model_version == 'empowerment':
    # #run empowerment prediction model
        print('\nRun empowerment prediction model.')
        empowerment_prediction = CrossValidation(k, time, game_version=game_version, prediction_model=2, epochs=100, steps_per_epoch=30, #epochs=100 & steps_per_epoch=30 for LA2
                                         exclude_elements_test=exclude_elements_test, exclude_elements_val=exclude_elements_val, manual_validation=0.2,
                                         vector_version=vector_version, dim=dim) #not sure if I need batch size or steps per epoch here, check it
        log.log_model_info(empowerment_prediction, mode=3, mode_type='{}EmpPred'.format(game_version), time=time)
        empowerment_prediction.run_cross_validation()
    else:
        raise ValueError('Undefined model version: "{}". Use "element" or "empowerment" instead.'.format(model_version))

    # join results
    print('\nJoin model results.')
    link_prediction_table = pd.read_csv('empowermentexploration/data/gametree/{}/{}LinkPredTable-{}-{}{}.csv'.format(time, game_version, split_version, vector_version, dim))
    link_prediction_table = link_prediction_table.drop(['trueSuccess', 'trueResult'], axis=1)
    link_prediction_table = link_prediction_table.set_index(['first', 'second'])
    link_prediction_table = link_prediction_table.groupby(link_prediction_table.index).mean()

    if model_version == 'element':
        element_prediction_table = pd.read_csv('empowermentexploration/data/gametree/{}/{}ElemPredTable-{}-{}{}.csv'.format(time, game_version, split_version, vector_version, dim))
        element_prediction_table = element_prediction_table.drop(['trueSuccess', 'trueResult'], axis=1)
        element_prediction_table = element_prediction_table.set_index(['first', 'second'])
        element_prediction_table = element_prediction_table.groupby(element_prediction_table.index).mean()
        gametree_table = link_prediction_table.join(element_prediction_table, how='outer')

    else:
        empowerment_prediction_table = pd.read_csv('empowermentexploration/data/gametree/{}/{}EmpPredTable-{}-{}{}.csv'.format(time, game_version, split_version, vector_version, dim))
        empowerment_prediction_table = empowerment_prediction_table.drop(['trueSuccess', 'trueResult'], axis=1)
        empowerment_prediction_table = empowerment_prediction_table.set_index(['first', 'second'])
        empowerment_prediction_table = empowerment_prediction_table.groupby(empowerment_prediction_table.index).mean()
        gametree_table = link_prediction_table.join(empowerment_prediction_table, how='outer')

    gametree_table.index = pd.MultiIndex.from_tuples(gametree_table.index)
    gametree_table.index.names = ['first', 'second']
    print(gametree_table)

    #add column 'predResult'
    if game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
        elements = 540
    elif game_version == 'alchemy2':
        elements = 720
    elif game_version == 'joined':
        elements = 738

    if model_version == 'element':
        gametree_table['predResult'] = gametree_table[gametree_table.columns[-elements:]].idxmax(axis='columns').astype(int)

    # write resulting table to file
    print('\nWrite to HDF5 file.')
    gametree_table.to_hdf('empowermentexploration/data/gametree/{}/{}GametreeTable-{}-{}{}.h5'.format(time, game_version, split_version, vector_version, dim), key='gametreeTable', mode='w')

    print('\nDone.')
