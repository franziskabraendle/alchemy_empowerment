import time

import empowermentexploration.utils.info_logs as log
from empowermentexploration.models.little_alchemy_model import \
    LittleAlchemyModel
from empowermentexploration.models.visualization import Visualization

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: SET APPROPRIATE VARIABLES
    # set game version: 'alchemy2', 'alchemy1', 'joined', 'tinypixels' or 'tinyalchemy'
    game_version = 'alchemy2'

    # set list of models that are to be run: 'base', 'cbv', 'cbu', 'sim', 'bin' 'emp', 'truebin', 'trueemp'
    models = ['bin']

    # set value calculation
    # tuple contains first list of calculation info on trueemp, then emp, then truebin, then and bin
    # each calculation info tuple in the list is ordered by (dynamic, local, outgoing_combinations)
    # set dynamic true for truebin oracle model, and false for normal bin on recreated gametree version
    value_calculation = ([(False,False,False)], [(None,None,False)], [(True,None,None)], [(False,None,None)])

    # set list of temperatures that are to be run
    temperatures = [0.1]

    # set number of runs and steps
    runs = 1000
    steps = 200

    # set memory type: 0, 1, 2
    memory_type = 1

    # set vector version the custom gameteee or word vectors are based on e.g. 'crawl300', 'ccen100
    # check if desired gametree and/or vectors are available
    vector_version = 'crawl300'
    split_version = 'data'
    # YOUR ACTION IS NOT RECQUIRED ANYMORE

    # create directory to log info from this run
    time = time.strftime('%Y%m%d-%H%M')
    log.create_directory('empowermentexploration/data/models/{}/'.format(time))

    # plot info for user
    print('\nRun models: {}. Save logs to directory empowermentexploration/data/model/{}/'.format(models, time))

    # write info on variables to file
    model = LittleAlchemyModel(time, game_version=game_version, runs=runs, steps=steps, temperatures=temperatures, memory_type=memory_type,
                               models=models, value_calculation=value_calculation, vector_version=vector_version, split_version=split_version)
    log.log_model_info(model, mode=1, mode_type='{}LittleAlchemyModel'.format(game_version), time=time)

    # run models
    for model_type in models:
        print('\nRun model: {}.'.format(model_type))
        # run empowerment-like models
        if model_type in ['trueemp', 'emp', 'truebin', 'bin']:
            # set list of empowerment calculations that are to be run for models 'trueemp', 'emp', 'truebin', 'emp'
            # (1) dynamic (2) local (3) outgoing combinations
            if model_type == 'trueemp':
                empowerment_calculation = value_calculation[0]
            elif model_type == 'emp':
                empowerment_calculation = value_calculation[1]
            elif model_type in ['truebin']:
                empowerment_calculation = value_calculation[2]
            elif model_type in ['bin']:
                empowerment_calculation = value_calculation[3]

            for e_c in empowerment_calculation:
                print('\nCalculation (dynamic, local, outgoing_combinations): {}.'.format(e_c))
                model = LittleAlchemyModel(time, game_version=game_version, runs=runs, steps=steps, temperatures=temperatures, memory_type=memory_type,
                                           vector_version=vector_version, split_version=split_version)
                model.simulate_game(model_type, e_c)
        # run other models
        else:
            model = LittleAlchemyModel(time, game_version=game_version, runs=runs, steps=steps, temperatures=temperatures, memory_type=memory_type,
                                       vector_version=vector_version, split_version=split_version)
            model.simulate_game(model_type)

    # initialize visualization
    visualization = Visualization(game_version, time, models, temperatures, runs, steps, memory_type)

    # plot gameprogress curves for comparison
    visualization.plot_all(value_calculation, human=True)

    print('\nDone.')
