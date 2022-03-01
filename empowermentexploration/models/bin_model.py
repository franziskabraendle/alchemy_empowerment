import random
from itertools import combinations_with_replacement

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import numpy as np
from empowermentexploration.models.inventory import Inventory


class BinModel():
    """Binary model based on self-constructed game tree.
    """
    def __init__(self, game_version, memory_type, empowerment_calculation, vector_version='crawl300', split_version='data'):
        """Initializes a little alchemy binary model based on self-constructed game tree.

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
        self.game_version = game_version
        # set infos on empowerment calculation
        self.dynamic = empowerment_calculation[0]

        # set memory information
        self.memory_type = memory_type

        # get empowerment info
        self.binary_info = data_handle.get_probability_table(game_version, split_version, vector_version)
        self.binary_info = self.binary_info[['predSuccess', 'predResult']]

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
            self.inventory_probabilities = helpers.softmax(self.binary_combinations.values(), temperature)

        # pick combination by probability with respect to memory
        combination_index = np.random.choice(len(self.binary_combinations), p = self.inventory_probabilities)
        combination = list(self.binary_combinations.keys())[combination_index]

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
            self.update_memory(combination, inventory, step)

        if self.dynamic is False:
            for result in results[0]:
                # update combination empowerment storage with new keys
                for inventory_element in inventory.inventory_used:
                    self.update_binary_combinations(sorted([result, inventory_element]), inventory)
        else:
            for combination in combinations_with_replacement(inventory.inventory_used,2):
                if tuple(sorted(combination)) not in self.memory:
                    self.update_binary_combinations(sorted([combination[0], combination[1]]), inventory)

    def update_memory(self, combination, inventory, step):
        """Adds combination to memory and deletes it from combination empowerment storage. \
            If memory is fading, every 5 steps a random entry in the memory is deleted.

        Args:
            combination (list): List of element indices that are involved in combination.
            inventory (Inventory): Info on current inventory.
            step (int): Current step within run.
        """
        # update fading memory every 5 steps
        if self.memory_type == 2 and step % 5 == 0 and self.memory:
            # find random combination to delete from memory and put it back to combination binary storage
            forget_combination = random.choice(list(self.memory.keys()))
            self.memory.pop(forget_combination)
            self.update_binary_combinations(forget_combination, inventory)

        # update memory with new combination and delete it from combination binary storage
        self.memory[combination[0],combination[1]] = 1
        self.binary_combinations.pop((combination[0],combination[1]))

    def update_binary_combinations(self, combination, inventory):
        """Updates combination binary storage depending on the calculation type.

        Args:
            combination (list): List of element indices that are involved in combination.
            inventory (Inventory): Info on current inventory.
        """
        # get all probabilities for this combination
        predicted_success = self.binary_info.loc[tuple(combination), :]

        # get empowerment value for combination
        self.binary_combinations[combination[0],combination[1]] = 0
        if self.dynamic is False:
            self.binary_combinations[combination[0],combination[1]] = predicted_success['predSuccess']
        else:
            if int(predicted_success['predResult']) not in inventory.inventory_total:
                self.binary_combinations[combination[0],combination[1]] = predicted_success['predSuccess']

    def reset(self):
        """Resets combination binary storage to combination between basic elements.
        """
        # initialize memory
        if self.memory_type != 0:
            self.memory = dict()

        # initialize combination empowerment storage
        self.binary_combinations = dict()
        inventory_basic = Inventory(self.game_version,0,0,0)
        inventory_basic.reset()
        for combination in combinations_with_replacement([0,1,2,3],2):
            self.update_binary_combinations(sorted(combination), inventory_basic)
