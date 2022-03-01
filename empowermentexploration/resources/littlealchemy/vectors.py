import empowermentexploration.utils.data_handle as data_handle
import fasttext.util
import numpy as np


class Vectors():
    """Class function generates Little Alchemy word vectors.
    """
    def __init__(self):
        """Initializes vector class.
        """
    
    def get_wordvectors(self, game_version, vector_version, dim):
        """Loads and stores fastText wordvectors of elements.

        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used. 
            vector_version (str): 'ccen', 'crawl' or 'wiki'. 
                        States what element vectors the empowerment info should be based on. 
            dim (int): Vector dimension e.g. 100 or 300.
        """
        # print info for user
        print('\nGet {} word vectors from fastText model {} with dimension {}.'.format(game_version, vector_version, dim))
        
        # load pretrained fastText model
        if vector_version == 'crawl':
            model = fasttext.load_model('empowermentexploration/resources/fasttext/crawl-300d-2M-subword.bin')
        elif vector_version == 'ccen':
            model = fasttext.load_model('empowermentexploration/resources/fasttext/cc.en.300.bin')
        elif vector_version == 'wiki':
            model = fasttext.load_model('empowermentexploration/resources/fasttext/wiki.en.bin')
        else:
            raise ValueError('Undefined version: "{}". Use "wiki", "crawl" or "ccen" instead.'.format(vector_version))

        # reduce dimensionality
        fasttext.util.reduce_model(model, dim)

        # load elements
        elements = data_handle.get_elements(game_version)

        # get element word vectors
        element_vectors = np.empty((0,model.get_dimension()), int)
        for i in range(len(elements)):
            element_vector = model[elements[i]]
            element_vectors = np.r_[element_vectors, np.reshape(element_vector, (1,-1))]

        # write element word vectors to text file for later usage
        np.savetxt('empowermentexploration/resources/littlealchemy/data/{}ElementVectors-{}{}.txt'.format(game_version, vector_version, dim), element_vectors)

        