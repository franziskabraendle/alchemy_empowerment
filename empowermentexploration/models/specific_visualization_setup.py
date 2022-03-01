import time

import empowermentexploration.utils.info_logs as log
from empowermentexploration.models.little_alchemy_model import \
    LittleAlchemyModel
from empowermentexploration.models.visualization import Visualization

print("start")
# YOUR ACTION IS REQUIRED HERE: SET APPROPRIATE VARIABLES
# set game version: 'alchemy2', 'alchemy1', 'joined', 'tinypixels' or 'tinyalchemy'
game_version = 'alchemy2'

# set list of models that are to be run: 'base', 'cbv', 'cbu', 'sim', 'bin' 'emp', 'truebin', 'trueemp'
models = ['base','cbu', 'truebin', 'trueemp', 'bin', 'emp']

# set value calculation
# tuple contains first list of calculation info on trueemp, then emp, then truebin and bin
# each calculation info tuple in the list is ordered by (dynamic, local, outgoing_combinations)
value_calculation = ([(False,False,False)], [(None,None,False)], [(True,None,None)], [(False,None,None)])

# set list of temperatures that are to be run
temperatures = [0.1]

# set number of runs and steps
runs = 1000
steps = 200

# set memory type: 0, 1, 2
memory_type = 1

# YOUR ACTION IS NOT RECQUIRED ANYMORE

#time = time.strftime('%Y%m%d-%H%M')
time= "20211130-1518"

# initialize visualization
visualization = Visualization(game_version, time, models, temperatures, runs, steps, memory_type)

# plot gameprogress curves for comparison
visualization.plot_all(value_calculation, human=True)

print('\nDone.')
