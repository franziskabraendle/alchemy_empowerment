import empowermentexploration.utils.data_handle as data_handle
import numpy as np
import pandas as pd
from empowermentexploration.resources.playerdata.inventory import Inventory


class PlayerDataTiny():
    """Class functions generate Tiny Alchemy or Tiny Pixels playerdata.
    """
    def __init__(self, version='alchemy'):
        """Initializes playerdata tiny class.
        
        Args:
            version (str, optional): 'alchemy' or 'pixels'. States what game version is going to be used. 
                    Defaults to 'alchemy'.
        """
        # print info for user
        print('\nGet Tiny {} player data.'.format(version.capitalize()))
        
        # load raw data
        raw_data = pd.read_csv('empowermentexploration/resources/playerdata/data/raw/tiny{}.csv'.format(version))
        raw_data = raw_data.to_numpy()
        
        # load element list
        elements = data_handle.get_elements(version='tiny{}'.format(version))

        # initialize storage for cleaned data
        clean_data = list()
        
        # initialize inventory
        inventory = Inventory(game_version='tiny{}'.format(version))

        # initialize player data
        player_data = list()
        error_flag = False
        player_id = -1
        trial_id = -1
        
        # parse through dataset
        for row in raw_data: 
            player_id_row = row[1]-1

            if player_id_row == player_id and error_flag is True:
                continue
            
            if player_id_row != player_id:  
                # append clean data only with correct data
                clean_data = clean_data + player_data         
                
                # update player_id
                player_id = player_id_row
                
                # initialize trialid
                trial_id = -1 
                
                # initialize player storage
                player_data = list()
            
                # initialize error flag
                error_flag = False

                # reset inventory
                inventory.reset()
                
            if version == 'alchemy':
                trial_id = row[2]-1
                try:
                    combination = sorted([elements.index(row[3]), elements.index(row[4])])
                except:
                    print('Error for id {} in trial {}.'.format(player_id_row, trial_id))
                    error_flag = True      
            elif version == 'pixels':
                trial_id += 1
                try:
                    combination = sorted([elements.index(row[2]), elements.index(row[3])])
                except:
                    print('Error for id {} in trial {}.'.format(player_id_row, trial_id))
                    error_flag = True      
     
            # check if combination elements are in current usable inventory
            if combination[0] in inventory.inventory_total and combination[1] in inventory.inventory_total:
                # get results and update inventory
                results = inventory.update(combination)
                
                # append data
                if len(results[1]) != 0:
                    player_data.append([player_id, trial_id, len(inventory.inventory_total), combination[0], combination[1], results[2], results[1]])
                else:
                    player_data.append([player_id, trial_id, len(inventory.inventory_total), combination[0], combination[1], results[2], -1])
            else:
                # set error flag if data not consistent to rules
                print('Error for id {} in trial {}: Combination elements {} and/or {} not in inventory.'.format(player_id_row, trial_id, combination[0], combination[1]))
                error_flag = True
            
            if np.all(row == raw_data[-1]):  
                # append clean data only with correct data
                clean_data = clean_data + player_data         
                
        # create a pandas DataFrame 
        clean_data = pd.DataFrame(clean_data, columns = ['id', 'trial', 'inventory', 'first', 'second', 'success', 'results']) 

        # write to csv file
        clean_data.to_csv('empowermentexploration/resources/playerdata/data/tiny{}HumanData.csv'.format(version), index=False)
        
        # print info for user
        print('\nGet Tiny {} player data with full memory.'.format(version.capitalize()))
        
        # preprocess data to have full memory
        clean_data = pd.read_csv('empowermentexploration/resources/playerdata/data/tiny{}HumanData.csv'.format(version)) 
        memory_data = clean_data.drop_duplicates(subset=['id', 'first', 'second'])
        group_size = memory_data.groupby('id')['trial'].count().to_numpy()
        
        trial_memory = list()
        for group in group_size:
            trial_memory = trial_memory + list(range(group))
            
        memory_data['trial'] = trial_memory
        
        # write to csv file
        memory_data.to_csv('empowermentexploration/resources/playerdata/data/tiny{}HumanDataMemory.csv'.format(version), index=False)
