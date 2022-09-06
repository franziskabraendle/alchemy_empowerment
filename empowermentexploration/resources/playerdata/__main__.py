from empowermentexploration.resources.playerdata.playerdata_la2 import PlayerDataLA2
from empowermentexploration.resources.playerdata.playerdata_tiny import PlayerDataTiny
from empowermentexploration.resources.playerdata.behavior import Behavior

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: CHOOSE APPROPRIATE METHOD AND METHOD ARGUMENTS
    #playerdata = PlayerDataLA2()
    #playerdata = PlayerDataTiny('alchemy')
    #playerdata = PlayerDataTiny('pixels')

    Behavior(version='alchemy2', memory=True, trials=100, model_type='base')
    Behavior(version='tinyalchemy', memory=True, trials=100, model_type='base')
    Behavior(version='tinypixels', memory=True, trials=100, model_type='base')

    # YOUR ACTION IS NOT RECQUIRED ANYMORE
