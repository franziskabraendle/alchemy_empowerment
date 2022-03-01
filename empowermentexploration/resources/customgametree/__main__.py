import json

import empowermentexploration.resources.customgametree.custom_empowerment as custom_empowerment
import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.info_logs as log
import numpy as np

if __name__ == '__main__':   
    # IMPORTANT INFORMATION: YOU MAY NEED TO RELOCATE DESIRED PROBABILITY TABLE FROM empowermentexploration.data.gametree BEFOREHAND
    # YOUR ACTION IS REQUIRED HERE
    # set game version: 'alchemy2', 'alchemy1', 'joined', 'tinypixels' or 'tinyalchemy'
    game_version = 'tinyalchemy'
    
    # set vector version: split on 'data' or 'element', use vector version 'ccen', 'wiki or 'crawl' and dimension 100 or 300 (check what is available)
    split_version = 'data'
    
    # set vector version the probability table is based on e.g. 'crawl300', 'ccen100
    # check if desired table is available 
    vector_version = 'crawl300'
    # YOUR ACTION IS NOT RECQUIRED ANYMORE

    # print info for user
    print('\nGet custom global empowerment info for game version {}.'.format(game_version))
    
    # get combinations
    if game_version == 'joined':
        n_elements = 738
    elif game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
        n_elements = 540
    elif game_version == 'alchemy2':
        n_elements = 720
        
    # get probability table
    probability_table = data_handle.get_probability_table(game_version, split_version, vector_version) 
    
    # print info for user
    print('\nGet single element empowerment info.')
    
    # initialize storage for empowerment info
    empowerment_outgoing_combinations = dict()
    empowerment_children = dict()
    
    # get empowerment info for each element
    for element in range(n_elements):       
        empowerment_outgoing_combinations[element] = custom_empowerment.get_empowerment(probability_table, float(element), True, n_elements)
        empowerment_children[element] = custom_empowerment.get_empowerment(probability_table, float(element), False, n_elements)
            
     # write to JSON file
    with open('empowermentexploration/resources/customgametree/data/{}OutgoingCombinationsEmpowermentTable-{}-{}.json'.format(game_version, split_version, vector_version), 'w') as filehandle:
        json.dump(empowerment_outgoing_combinations, filehandle, indent=4, sort_keys=True)
    
    with open('empowermentexploration/resources/customgametree/data/{}ChildrenEmpowermentTable-{}-{}.json'.format(game_version, split_version, vector_version), 'w') as filehandle:
        json.dump(empowerment_children, filehandle, indent=4, sort_keys=True)
    
    # print info for user
    print('\nGet combination empowerment info.')
    
    # initialize logging to csv file
    log.create_empowermenttable_file(game_version=game_version, split_version=split_version, vector_version=vector_version)
    
    # get empowerment info for each combination
    for element in range(n_elements):
        # get combination probabilities
        combination_probabilities = probability_table.query('first == @element')
        
        # get combination elements
        combination_elements = combination_probabilities.index.values
        combination_elements = [list(x) for x in combination_elements]
        combination_elements = np.array(combination_elements)
        
        # get predicted result
        result = combination_probabilities['predResult'].values
        
        # get probability
        empowerment_probability = custom_empowerment.get_combination_empowerment(empowerment_outgoing_combinations, empowerment_children, combination_probabilities, n_elements)
        
        # join arrays
        element_empowerment_info = np.zeros((combination_probabilities.shape[0],7))
        element_empowerment_info[:,:2] = combination_elements
        element_empowerment_info[:,2] = result
        element_empowerment_info[:,3:] = empowerment_probability
        
        # write to file
        log.append_empowermenttable_file(element_empowerment_info, first_line=False, game_version=game_version, split_version=split_version, vector_version=vector_version)
            
    print('\nDone.')
