import json

import pandas as pd
from empowermentexploration.resources.playerdata.inventory import Inventory


class PlayerDataLA2():
    """Class functions generate Little Alchemy 2 playerdata.
    """
    def __init__(self):
        """Initializes playerdata class for Little Alchemy 2 data.
        """
        # print info for user
        print('\nGet Little Alchemy 2 player data.')
        
        # load raw data
        with open('empowermentexploration/resources/playerdata/data/raw/little-alchemy-2-attempts_data-formatted.json', encoding='utf8') as infile:
            raw_data = json.load(infile)
            
        # load raw gametree
        with open('empowermentexploration/resources/littlealchemy/data/raw/all.json', encoding='utf8') as infile:
            raw_gametree = json.load(infile)
            
        # set for hidden elements that won't be included in game tree
        hidden_elements = {'tardis', 'the doctor', 'blaze', 'conflagration', 'inferno', 'terrain', 'ground', 'supervolcano', 'keyboard cat', 'batman'}

        # get assignment of old ID to new ID
        id_assignments = dict()
        new_ID = 0
        for old_ID in raw_gametree['elements']: 
            if 'dlc' not in raw_gametree['elements'][old_ID] and raw_gametree['elements'][old_ID]['name'] not in hidden_elements:
                id_assignments[old_ID] = new_ID
                new_ID += 1

        # initialize storage for cleaned data
        clean_data = list()
        
        # initialize inventory
        inventory = Inventory()

        # parse through every player
        for person_id, person in enumerate(raw_data['attempts']): 
            # initialize player storage
            player_data = list()
            
            # initialize error flag
            error_flag = False

            # reset inventory
            inventory.reset()

            # parse through every trial
            for trial_id, trial in enumerate(raw_data['attempts'][person]):
                # check if player played at all, get result and then update data
                if 'synced_with_other_progress' not in raw_data['attempts'][person][trial]['v']:
                    # get combination
                    combination = raw_data['attempts'][person][trial]['v'].split('|')
                    combination = sorted([id_assignments[combination[0]], id_assignments[combination[1]]])

                    # check if combination elements are in current usable inventory
                    if combination[0] in inventory.inventory_used and combination[1] in inventory.inventory_used:
                        # get results and update inventory
                        results = inventory.update(combination)

                        # append data
                        if len(results[1]) != 0:
                            player_data.append([person_id, trial_id, len(inventory.inventory_total), combination[0], combination[1], results[2], results[1]])
                        else:
                            player_data.append([person_id, trial_id, len(inventory.inventory_total), combination[0], combination[1], results[2], -1])
                    else:
                        # set error flag if data not consistent to rules
                        print('Error for id {} in trial {}: Combination elements {} and/or {} not in usable inventory.'.format(person_id, trial_id, combination[0], combination[1]))
                        error_flag = True
                        break
                        
            # append clean data only if there was no error
            # TODO: write to file continuously to save time
            if error_flag is False:
                clean_data = clean_data + player_data 

        # create a pandas DataFrame 
        clean_data = pd.DataFrame(clean_data, columns = ['id', 'trial', 'inventory', 'first', 'second', 'success', 'results']) 

        # write to csv file
        clean_data.to_csv('empowermentexploration/resources/playerdata/data/alchemy2HumanData.csv', index=False)
        
        # print info for user
        print('\nGet Little Alchemy 2 player data with full memory.')
        
        # preprocess data to have full memory
        clean_data = pd.read_csv('empowermentexploration/resources/playerdata/data/alchemy2HumanData.csv') 
        memory_data = clean_data.drop_duplicates(subset=['id', 'first', 'second'])
        group_size = memory_data.groupby('id')['trial'].count().to_numpy()
        
        trial_memory = list()
        for group in group_size:
            trial_memory = trial_memory + list(range(group))
            
        memory_data['trial'] = trial_memory
        
        # write to csv file
        memory_data.to_csv('empowermentexploration/resources/playerdata/data/alchemy2HumanDataMemory.csv', index=False)
