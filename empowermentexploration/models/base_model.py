import random


class BaseModel():
    """Baseline model.
    """
    def __init__(self, memory_type):
        """Initializes a little alchemy baseline model.
        
        Args:
            memory_type (int): States whether it should be memorized what combinations have been used before. 
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)
        """
        # set memory information
        self.memory_type = memory_type
        
    def choose_combination(self, inventory, step):
        """Chooses random combination.

        Args:
            inventory (Inventory): Info on current inventory.
            step (int): Current step within run. 

        Returns:
            list: List of element indices that are involved in combination.
        """
        if self.memory_type == 0:
            # generate random combination from current used inventory
            combination = sorted([random.choice(list(inventory.inventory_used)), random.choice(list(inventory.inventory_used))])
        else:
            # generate new random combination that was not already used
            is_new = False
            while is_new is False:
                combination = sorted([random.choice(list(inventory.inventory_used)), random.choice(list(inventory.inventory_used))])
                if (combination[0],combination[1]) not in self.memory:
                    is_new = True
            self.update_memory(combination, step)
            
        return combination
        
    def update_memory(self, combination, step):
        """Adds combination to memory. If memory is fading, every 5 steps a random entry in the memory is deleted.

        Args:
            combination (list): List of element indices that are involved in combination.
            step (int): Current step within run.
        """
        if self.memory_type == 2 and step % 5 == 0 and self.memory:
            self.memory.pop(random.choice(list(self.memory.keys())))
        self.memory[combination[0],combination[1]] = 1
        
    def reset(self):
        """Resets memory.
        """     
        # initialize memory       
        if self.memory_type != 0:
            self.memory = dict()
