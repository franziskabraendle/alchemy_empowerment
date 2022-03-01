import empowermentexploration.utils.data_handle as data_handle
import numpy as np


class PlayerData():
    """Little Alchemy player data.
    """
    def __init__(self, game_version='alchemy2', data_source='base', memory_type=1):
        """Initializes little alchemy player data.

        Args:
            game_version (str, optional): 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what player data set set is going to be used. Defaults to 'alchemy2'.
            data_source (str, optional): States what kind of model is going to be used as data source: 
                        'human', 'base', 'bin', 'emp', 'truebin', 'trueemp', 'sim', 'cbu', 'cbv'.
                        Defaults to 'human'.
            memory_type (int, optional): Memory type that was used for data generation. There are different options
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 10 steps)
                        Defaults to 1.
        """               
        # load player or simulation data
        if data_source == 'human':
            if memory_type == 1 or memory_type == 2:
                memory = True
            else:
                memory = False
            self.data = data_handle.get_player_data(game_version, memory=memory)      
        else:
            self.data = data_handle.get_simulation_data(game_version, data_source, memory_type)         
    
    def get_player_subset(self, n_players=None, steps=None, seed=None):
        """Returns player subset indices.
        
        Args:
            n_players (int, optional): Number of players. 
            steps (int, optional): Minimum number of steps a player must have.  
            seed (int, optional): Seed used for random selection.
        """
        if steps is not None:
            # group by player id
            grouped_data = self.data.groupby('id')
            
            # filter by number of steps
            trial_size = grouped_data['trial'].max()
            trial_size = trial_size.loc[trial_size > steps-2]
            
            if n_players is not None:
                # get player subset of a given size
                if seed is not None:
                    np.random.seed(seed)
                player_subset = np.random.choice(trial_size.index, n_players, replace=False)
            else:
                player_subset = trial_size.index
            
            # get data subset
            self.data = self.data.query('id in @player_subset & trial < @steps')
        else:
            if n_players is not None:
                # get player subset of a given size
                if seed is not None:
                    np.random.seed(seed)
                player_subset = np.random.choice(self.data['id'].unique(), n_players, replace=False)
                
                # get data subset
                self.data = self.data.query('id in @player_subset')
