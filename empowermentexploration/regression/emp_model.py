import empowermentexploration.utils.data_handle as data_handle


class EmpModel():
    """Empowerment model based on self-constructed game tree.
    """
    def __init__(self, game_version='alchemy2', split_version='data', vector_version='crawl300'):
        """Initializes a little alchemy empowerment model based on self-constructed game tree.
        
            Args:
                game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels. 
                        States what element and combination set is going to be used. Defaults to 'alchemy2'.
                split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on. 
                            Defaults to 'data'.
                vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                            States what element vectors the table should be based on. 
                            Defaults to 'crawl300'.
        """
        # TODO: offer diffferen empowerment calculation options
        # get empowerment info 
        self.empowerment_info = data_handle.get_empowerment_info(game_version, split_version, vector_version)
        self.empowerment_info = self.empowerment_info.set_index(['first', 'second'])
        self.empowerment_info = self.empowerment_info.sort_index()
                
    def get_value(self, combination):
        """Returns empowerment value for given combination.

        Args:
            combination (list): List of element indices that are involved in combination.

        Returns:
            float: Value.
        """            
        # get all probabilities for this combination
        predicted_empowerment = self.empowerment_info.loc[tuple(combination), :]
                        
        # set empowerment value for combination
        empowerment = predicted_empowerment['empChild']

        return empowerment
