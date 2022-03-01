import empowermentexploration.utils.data_handle as data_handle
from sklearn.metrics.pairwise import cosine_similarity


class SimModel():
    """Similarity model.
    """
    def __init__(self, game_version, vector_version='crawl300'):
        """Initializes a little alchemy similarity model.
        
        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                        States what element vectors the table should be based on. 
                        Defaults to 'crawl300'.
        """
        # get similarities
        element_vectors = data_handle.get_wordvectors(game_version, vector_version)
        self.similarities = cosine_similarity(element_vectors, element_vectors)
      
    def get_value(self, combination):
        """Returns value for given combination.

        Args:
            combination (list): List of element indices that are involved in combination.

        Returns:
            float: Value.
        """
        return self.similarities[combination[0]][combination[1]]
    