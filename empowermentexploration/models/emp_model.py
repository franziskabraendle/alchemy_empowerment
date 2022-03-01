import random
from itertools import combinations_with_replacement

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import numpy as np


class EmpModel():
    """Empowerment model based on self-constructed game tree.
    """
    def __init__(self, game_version, memory_type, empowerment_calculation, vector_version='crawl300', split_version='data'):
        """Initializes a little alchemy empowerment model based on self-constructed gametree.

        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinypixels' or 'tinyalchemy'. 
                        States what element and combination set is going to be used.
            memory_type (int): States whether it should be memorized what combinations have been used before.
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)  
            empowerment_calculation (tuple): Tuple made of three entries.
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations 
                                    or length of set of resulting elements.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                        States what element vectors the empowerment info should be based on. 
                        Defaults to 'crawl300'.
            split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on. 
                        Defaults to 'data'.
        """
        # set infos on empowerment calculation
        self.outgoing_combinations = empowerment_calculation[2]
               
        # get number of elements 
        self.game_version = game_version
        if self.game_version == 'joined':
            self.n_elements = 738
        elif self.game_version == 'alchemy1':
            self.n_elements = 540
        elif self.game_version == 'alchemy2':
            self.n_elements = 720
        
        # set memory information
        self.memory_type = memory_type
        
        # get empowerment info 
        self.empowerment_info = data_handle.get_empowerment_info(game_version, split_version, vector_version)
        self.empowerment_info = self.empowerment_info.set_index(['first', 'second'])
        self.empowerment_info = self.empowerment_info.sort_index()
        
    def choose_combination(self, temperature, renew_calculation):
        """Chooses combination.

        Args:
            temperature (float): Current temperature for softmax function.
            renew_calculation (bool): True = renew calculation of inventory probabilities, False = Use previous inventory probabilities
            
        Returns:
            list: List of element indices that are involved in combination.
        """
        if renew_calculation is True:
            # compute probabilities with softmax function
            self.inventory_probabilities = helpers.softmax(self.empowerment_combinations.values(), temperature)
        
        # pick combination by probability with respect to memory
        combination_index = np.random.choice(len(self.empowerment_combinations), p = self.inventory_probabilities)
        combination = list(self.empowerment_combinations.keys())[combination_index]
        
        return combination

    def update_model_specifics(self, combination, results, inventory, step):
        """Updates combination empowerment storage.
        
        Args:
            combination (list): List of element indices that are involved in combination.
            result (tuple): Consists of
                        (1) new_results_non_final (list): List of non final element indices that resulted from combination.
                        (2) new_results_total (list): List of all new element indices that resulted from combination.
            inventory (Inventory): Info on current inventory.
            step (int): Current step within run. 
        """
        # update memory if necessary
        if self.memory_type != 0:
            self.update_memory(combination, step)
            
        for result in results[0]:
            # update combination empowerment storage with new keys
            for inventory_element in inventory.inventory_used:
                self.update_empowerment_combinations(sorted([result, inventory_element]))
     
    def update_memory(self, combination, step):
        """Adds combination to memory and deletes it from combination empowerment storage. \
            If memory is fading, every 5 steps a random entry in the memory is deleted.

        Args:
            combination (list): List of element indices that are involved in combination.
            step (int): Current step within run. 
        """
        # update fading memory every 5 steps
        if self.memory_type == 2 and step % 5 == 0 and self.memory:
            # find random combination to delete from memory and put it back to combination empowerment storage
            forget_combination = random.choice(list(self.memory.keys()))
            self.memory.pop(forget_combination)
            self.update_empowerment_combinations(forget_combination)
        
        # update memory with new combination and delete it from combination empowerment storage
        self.memory[combination[0],combination[1]] = 1
        self.empowerment_combinations.pop((combination[0],combination[1]))
        
    def update_empowerment_combinations(self, combination):
        """Updates combination empowerment storage depending on the calculation type.

        Args:
            combination (list): List of element indices that are involved in combination.
        """
        # get all probabilities for this combination
        predicted_empowerment = self.empowerment_info.loc[tuple(combination), :]
                        
        # set empowerment value for combination
        if self.outgoing_combinations is True:
            self.empowerment_combinations[combination[0],combination[1]] = predicted_empowerment['empComb']
        else:
            self.empowerment_combinations[combination[0],combination[1]] = predicted_empowerment['empChild']
    
    def reset(self):
        """Resets combination empowerment storage to combination between basic elements.
        """
        # initialize memory
        if self.memory_type != 0:
            self.memory = dict()
             
        # initialize combination empowerment storage
        self.empowerment_combinations = dict()
        for combination in combinations_with_replacement([0,1,2,3],2):
            self.update_empowerment_combinations(sorted(combination))
