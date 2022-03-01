import empowermentexploration.utils.data_handle as data_handle


class TrueBinModel():
    """Binary model based on true game tree.
    """
    def __init__(self, game_version='alchemy2'):
        """Initializes a little alchemy binary model based on true game tree.
        
        Args:
            game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used. Defaults to 'alchemy2'.
        """ 
        # TODO: offer dynamic calculation        
        # get combination table 
        self.combination_table = data_handle.get_combination_table(game_version, csv=False)
        
    def get_value(self, combination):
        """Returns value for given combination.

        Args:
            combination (list): List of element indices that are involved in combination.

        Returns:
            float: Value.
        """  
        utility = 0
        if combination[0] in self.combination_table and combination[1] in self.combination_table[combination[0]]:
            utility = 1
            
        return utility
