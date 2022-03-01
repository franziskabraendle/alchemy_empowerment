import random
from itertools import combinations_with_replacement

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import numpy as np
from empowermentexploration.models.inventory import Inventory


class TrueEmpModel():
    """Empowerment model based on true game tree.
    """
    def __init__(self, game_version, memory_type, empowerment_calculation):
        """Initializes a little alchemy empowerment model based on true game tree.

        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                        States what element and combination set is going to be used.
            memory_type (int, optional): States whether it should be memorized what combinations have been used before.
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)
            empowerment_calculation (tuple): Tuple made of three entries.
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                    or length of set of resulting elements.
        """
        # set infos on empowerment calculation
        self.dynamic = empowerment_calculation[0]
        self.local = empowerment_calculation[1]
        self.outgoing_combinations = empowerment_calculation[2]

        # get parent table to check for resulting elements
        self.game_version = game_version
        self.parent_table = data_handle.get_parent_table(game_version)

        # get combination table
        self.combination_table = data_handle.get_combination_table(game_version, csv=False)

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
            self.update_memory(combination, inventory, step)

        if self.local is False and self.dynamic is False:
            for result in results[0]:
                # update combination empowerment storage with new keys
                for inventory_element in inventory.inventory_used:
                    self.update_empowerment_combinations(sorted([result, inventory_element]), inventory)
        else:
            for combination in combinations_with_replacement(inventory.inventory_used,2):
                if tuple(sorted(combination)) not in self.memory:
                    self.update_empowerment_combinations(sorted([combination[0], combination[1]]), inventory)

        for result in results[1]:
            if self.dynamic is True and self.outgoing_combinations is True:
                # delete all combinations whith same result out of combination table
                self.combination_table_csv.query('first!=@result & second!=@result & result!=@result', inplace=True)

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
            # find random combination to delete from memory and put it back to combination empowerment storage
            forget_combination = random.choice(list(self.memory.keys()))
            self.memory.pop(forget_combination)
            self.update_empowerment_combinations(forget_combination, inventory)

        # update memory with new combination and delete it from combination empowerment storage
        self.memory[combination[0],combination[1]] = 1
        self.empowerment_combinations.pop((combination[0],combination[1]))

        # delete combination out of combination table
        if self.outgoing_combinations is True:
            self.combination_table_csv.query('first!=@combination[0] & second!=@combination[1]', inplace=True)

    def update_empowerment_combinations(self, combination, inventory):
        """Updates combination empowerment storage depending on the calculation type.

        Args:
            combination (list): List of element indices that are involved in combination.
            inventory (Inventory): Info on current inventory.
        """
        # set empowerment value for combination
        self.empowerment_combinations[combination[0],combination[1]] = self.get_empowerment_value(combination, inventory)

    def get_empowerment_value(self, combination, inventory):
        """Returns combination empowerment value depending on the calculation type.

        Args:
            combination (list): List of element indices that are involved in combination.
            inventory (Inventory): Info on current inventory.
        """
        # check results of combination
        if combination[0] in self.combination_table and combination[1] in self.combination_table[combination[0]]:
            results = self.combination_table[combination[0]][combination[1]]
        else:
            results = list()

        # initialize empowerment depending on how it is calculated
        if self.outgoing_combinations is True:
            empowerment = 0
        else:
            empowerment = set()

        # calculate empowerment value iteratively for each result
        for r in results:
            if r in self.parent_table:
                # extend inventory with result
                inventory_used_temp = inventory.inventory_used.copy()
                inventory_used_temp.add(r)

                if self.outgoing_combinations is True:
                    first_r = self.combination_table_csv.eval('first==@r')
                    second_r = self.combination_table_csv.eval('second==@r')
                    if self.local is False:
                        # check how many outgoing combinations with result are possible
                        combinations = self.combination_table_csv.loc[first_r | second_r].drop_duplicates(subset=['first', 'second'])
                    else:
                        # check how many outgoing combinations between result and elements from inventory are possible
                        first_inventory = self.combination_table_csv.eval('first in @inventory_used_temp')
                        second_inventory = self.combination_table_csv.eval('second in @inventory_used_temp')
                        combinations = self.combination_table_csv.loc[(first_r & second_inventory) | (first_inventory & second_r)].drop_duplicates(subset=['first', 'second'])
                    empowerment += len(combinations.index)
                else:
                    # check children for every resulting element
                    if self.local is False:
                        # add results to set, no matter with what elements those resuls were achieved
                        # in case of dynamic calculation only if this result is not already in the inventory
                        if (self.dynamic is False) or (self.dynamic is True and r not in inventory.inventory_total):
                            empowerment.update(self.parent_table[r])
                    else:
                        # add results to set, but only those that resulted from combinations within inventory
                        # in case of dynamic calculation only if this result is not already in the inventory
                        if (self.dynamic is False) or (self.dynamic is True and r not in inventory.inventory_total):
                            for item in inventory_used_temp:
                                a = sorted([r, item])
                                if a[0] in self.combination_table and a[1] in self.combination_table[a[0]]:
                                    empowerment.update(self.combination_table[a[0]][a[1]])
        if self.outgoing_combinations is False:
            if self.dynamic is True:
                # only those elements add to empowerment value that are new
                empowerment = len(empowerment.difference(inventory.inventory_total))
            else:
                empowerment = len(empowerment)

        return empowerment

    def reset(self):
        """Resets combination empowerment storage to combination between basic elements.
        """
        # initialize memory
        if self.memory_type != 0:
            self.memory = dict()

        # reset combination table csv
        if self.outgoing_combinations is True:
            self.combination_table_csv = data_handle.get_combination_table(self.game_version, csv=True)
            self.combination_table_csv.query('success == 1', inplace=True)

        # initialize combination empowerment storage
        self.empowerment_combinations = dict()
        inventory_basic = Inventory(self.game_version,0,0,0)
        inventory_basic.reset()
        for combination in combinations_with_replacement([0,1,2,3],2):
            self.update_empowerment_combinations(sorted(combination), inventory_basic)
