import random
from itertools import combinations_with_replacement

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class SimModel():
    """Similarity model.
    """
    def __init__(self, game_version, memory_type, vector_version):
        """Initializes a little alchemy similarity model.
        
        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinypixels' or 'tinyalchemy'. 
                        States what element and combination set is going to be used.
            memory_type (int): States whether it should be memorized what combinations have been used before.
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                        States what element vectors the empowerment info should be based on. 
                        Defaults to 'crawl300'.
        """
        # get similarities
        element_vectors = data_handle.get_wordvectors(game_version, vector_version)
        self.similarities = cosine_similarity(element_vectors, element_vectors)
        
        # set memory information
        self.memory_type = memory_type
        
    def choose_combination(self, temperature, renew_calculation):
        """Chooses combination.

        Args:
            temperature (float): Current temperature for softmax function.
            renew_calculation (bool): True = renew calculation of inventory probabilities, False = Use previous inventory probabilities.

        Returns:
            list: List of element indices that are involved in combination.
        """
        if renew_calculation is True:
            # compute probabilities with softmax function
            self.inventory_probabilities = helpers.softmax(self.similarities_combinations.values(), temperature)
        
        # pick combination by probability with respect to memory
        combination_index = np.random.choice(len(self.similarities_combinations), p = self.inventory_probabilities)
        combination = list(self.similarities_combinations.keys())[combination_index]
            
        return combination

    def update_model_specifics(self, combination, results, inventory, step):
        """Updates combination similarity storage.
        
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
            # update combination similarity storage with new keys
            for inventory_element in inventory.inventory_used:
                update_combination = sorted([result, inventory_element])
                self.similarities_combinations[update_combination[0], update_combination[1]] = self.similarities[update_combination[0], update_combination[1]]
            
    def update_memory(self, combination, step):
        """Adds combination to memory and deletes it from combination similarity storage. \
            If memory is fading, every 5 steps a random entry in the memory is deleted.

        Args:
            combination (list): List of element indices that are involved in combination.
            step (int): Current step within run.
        """
        # update fading memory every 10 steps
        if self.memory_type == 2 and step % 5 == 0 and self.memory:
            # find random combination to delete from memory and put it back to combination similarity storage
            forget_combination = random.choice(list(self.memory.keys()))
            self.memory.pop(forget_combination)
            self.similarities_combinations[forget_combination[0],forget_combination[1]] = self.similarities[forget_combination[0],forget_combination[1]]
        
        # update memory with new combination and delete it from combination similarity storage
        self.memory[combination[0],combination[1]] = 1
        self.similarities_combinations.pop((combination[0],combination[1]))

    def reset(self):
        """Resets combination similarity storage to combination between basic elements.
        """
        # initialize memory
        if self.memory_type != 0:
            self.memory = dict()
        
        # initialize combination similarity storage
        self.similarities_combinations = dict()
        for combination in combinations_with_replacement([0,1,2,3],2):
            combination = sorted(combination)
            self.similarities_combinations[combination[0],combination[1]] = self.similarities[combination[0],combination[1]]
