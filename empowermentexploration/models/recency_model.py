import math
import random
from itertools import combinations_with_replacement

import empowermentexploration.utils.helpers as helpers
import numpy as np


class RecencyModel():
    """Recency model based on time until element was last used.
    """
    def __init__(self, game_version, memory_type):
        """Initializes a little alchemy recency model.

        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinypixels' or 'tinyalchemy'.
                        States what element and combination set is going to be used.
            memory_type (int): States whether it should be memorized what combinations have been used before.
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)
        """
        # get number of elements
        if game_version == 'joined':
            self.n_elements = 738
        elif game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
            self.n_elements = 540
        elif game_version == 'alchemy2':
            self.n_elements = 720

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
            self.inventory_probabilities = helpers.softmax(self.values_combinations.values(), temperature)

        # pick combination by probability with respect to memory
        combination_index = np.random.choice(len(self.values_combinations), p = self.inventory_probabilities)
        combination = list(self.values_combinations.keys())[combination_index]

        return combination

    def update_model_specifics(self, combination, results, inventory, step):
        """Updates combination value storage.

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
            # update combination value storage with new keys
            for inventory_element in inventory.inventory_used:
                update_combination = sorted([result, inventory_element])
                self.values_combinations[update_combination[0], update_combination[1]] = self.values_elements[inventory_element]

        # update element values for combination elements
        self.total_count += 1
        self.element_lastused += 1
        self.element_lastused[combination[0]] = 0
        self.element_lastused[combination[1]] = 0

        for i in range(self.n_elements):
            self.values_elements[i] = (self.element_lastused[i]) / (self.total_count)

        # update combination value storage
        for key, _ in self.values_combinations.items():
            self.values_combinations[key] = self.values_elements[key[0]] + self.values_elements[key[1]]

    def update_memory(self, combination, step):
        """Adds combination to memory and deletes it from combination value storage. \
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
            self.values_combinations[forget_combination[0],forget_combination[1]] = self.values_elements[forget_combination[0]] + self.values_elements[forget_combination[1]]

        # update memory with new combination and delete it from combination similarity storage
        self.memory[combination[0],combination[1]] = 1
        self.values_combinations.pop((combination[0],combination[1]))

    def reset(self):
        """Resets combination value storage to combination between basic elements.
        """
        # initialize memory
        if self.memory_type != 0:
            self.memory = dict()

        # initialize combination value storage
        self.values_elements = np.zeros(self.n_elements)
        self.total_count = 1
        self.element_lastused = np.zeros(self.n_elements)
        self.values_combinations = dict()
        for combination in combinations_with_replacement([0,1,2,3],2):
            combination = sorted(combination)
            self.values_combinations[combination[0],combination[1]] = 0
