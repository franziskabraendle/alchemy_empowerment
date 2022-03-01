import empowermentexploration.utils.data_handle as data_handle
import numpy as np


class Inventory():
    """Little Alchemy Inventory
    """
    def __init__(self, game_version, temperatures, runs, steps):
        """Initializes a little alchemy inventory.

        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. States what element and combination set is going to be used.
            temperatures (int): Number of temperatures for which simulations are run. 
            runs (int): Number of simulations.
            steps (int): Number of steps for each simulation. 
        """        
        # initialize storage
        self.inventory_size_over_time = np.zeros((temperatures, runs, steps + 1))
        self.inventory_size_over_time[:,:,0] = 4
        self.combination_storage = list()
        
        # load info tables
        self.game_version = game_version
        self.parents = data_handle.get_parent_table(game_version)
        self.combination_table = data_handle.get_combination_table(game_version, csv=False)
    
    def reset(self):
        """Resets inventory to basic elements.
        """
        self.inventory_used = {0,1,2,3}
        self.inventory_total = {0,1,2,3}
        if self.game_version == 'alchemy2':
            self.combination_table_depletion = data_handle.get_combination_table(self.game_version, csv=False)
    
    def update(self, combination, temperature_idx, run, step):
        """Updates inventory for given combination and results. Stores inventory length for given run and step.

        Args:
            combination (list): List of two element indices involved in last combination.
            temperature_idx (int): Current temperature index. 
            run (int): Current run.
            step (int): Current step within run.
        """
        # store current inventory
        inventory_used_temp = self.inventory_used.copy()
        inventory_total_temp = self.inventory_total.copy()
        
        # get combination results
        combination_results = self.get_combination_results(combination)
        
        # set success to 1 if combination is successful
        if len(combination_results)> 0:
            success = 1
        else:
            success = 0
        
        # update total inventory
        self.inventory_total.update(combination_results)
        if self.game_version == 'alchemy2':
            condition_elements = self.check_conditions()
            self.inventory_total.update(condition_elements) 

            # update used inventory
            for element in combination_results + condition_elements:
                if self.is_final(element) is False:
                    if self.is_depleted(element) is False:
                        self.inventory_used.add(element)
            
            # delete depleted elements
            self.update_combination_table(combination)
            self.delete_if_depleted(combination[0])
            self.delete_if_depleted(combination[1])
        else:
            self.inventory_used = self.inventory_total.copy()
        
        # store inventory length
        self.inventory_size_over_time[temperature_idx,run,step+1] = len(self.inventory_total)
        
        new_results_non_final = list(self.inventory_used.difference(inventory_used_temp))
        new_results_total = list(self.inventory_total.difference(inventory_total_temp))
        
        # store info on trials
        if len(new_results_total) != 0:            
            self.combination_storage.append({'id': run, 'trial': step, 'inventory': len(self.inventory_total), 
                                            'first': combination[0], 'second': combination[1], 
                                            'success': success, 'results': new_results_total, 't': temperature_idx})
        else:
            self.combination_storage.append({'id': run, 'trial': step, 'inventory': len(self.inventory_total), 
                                            'first': combination[0], 'second': combination[1], 
                                            'success': success, 'results': -1, 't': temperature_idx})
        
        return (new_results_non_final, new_results_total)
    
    def get_combination_results(self, combination):
        """Returns combination results.

        Args:
            combination (list): List of element indices involved in combination.

        Returns:
            list: List of element indices that resulted from combination.
        """
        if combination[0] in self.combination_table and combination[1] in self.combination_table[combination[0]]:
            return self.combination_table[combination[0]][combination[1]]
        else:
            return list()
    
    def check_conditions(self):
        """Returns elements for which conditions are fulfilled.

        Returns:
            list: List of elements indices for which conditions are fulfilled.
        """       
        condition_elements = list()
        inventory_size = len(self.inventory_total)
    
        # check for size conditions
        if (inventory_size >= 50) and (35 not in self.inventory_total):
            condition_elements.append(35)
        if (inventory_size >= 100) and (40 not in self.inventory_total):
            condition_elements.append(40)
        if (inventory_size >= 150) and (605 not in self.inventory_total):
            condition_elements.append(605)
        if (inventory_size >= 150) and (606 not in self.inventory_total):
            condition_elements.append(606)
        if (inventory_size >= 150) and (566 not in self.inventory_total):
            condition_elements.append(566)
        if (inventory_size >= 300) and (627 not in self.inventory_total):
            condition_elements.append(627)
        
        # check for set conditions
        light_set = {367, 114, 239, 280, 593, 136, 125, 21, 107, 176, 434, 25, 46, 109, 133, 284}
    
        if (121 not in self.inventory_total) and (len(self.inventory_total.intersection(light_set)) >= 5):
            condition_elements.append(121)

        small_set = {165, 325, 332, 484, 574, 570, 485, 422, 429, 419, 339, 222}
        if (572 not in self.inventory_total) and (len(self.inventory_total.intersection(small_set)) >= 5):
            condition_elements.append(572)

        motion_set = {569, 265, 19, 150, 375, 15, 12, 16, 20, 22, 25, 32, 40, 45, 248}
        if (571 not in self.inventory_total) and (len(self.inventory_total.intersection(motion_set)) >= 5):
            condition_elements.append(571)

        return condition_elements
    
    def is_final(self, element):
        """Checks if element is final.

        Args:
            element (int): Element index.

        Returns:
            bool: True if element is final, False if it is not.
        """
        if (element in self.parents) and (len(self.parents[element]) > 0):
            return False
        else:
            return True
        
    def is_depleted(self, element):
        """Checks if element is depleted.

        Args:
            element (int): Element index.

        Returns:
            bool: True if element is depleted, False if it is not.
        """
        if len(self.combination_table_depletion[element]) == 0 and element in self.inventory_used:
            return True
        return False
                   
    def delete_if_depleted(self, element):
        """Deletes element from used inventory if it is depleted.

        Args:
            element (int): Element index.
        """
        if self.is_final is False:
            if self.is_depleted(element) is True:
                self.inventory_used.remove(element)
            
    def update_combination_table(self, combination):
        """Deletes combination from combination table.

        Args:
            combination (list): List of element indices involved in combination.
        """
        if combination[0] in self.combination_table_depletion and combination[1] in self.combination_table_depletion[combination[0]]:
            del self.combination_table_depletion[combination[0]][combination[1]]
        if combination[1] in self.combination_table_depletion and combination[0] in self.combination_table_depletion[combination[1]]:
            del self.combination_table_depletion[combination[1]][combination[0]]
