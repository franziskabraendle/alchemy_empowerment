import empowermentexploration.utils.data_handle as data_handle
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

mpl.use('Agg')

class Similarity():
    """Class function plots similarity values.
    """
    def __init__(self, game_version, vector_version='crawl300'):
        """Initializes similarity class.
        
        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used.
            vector_versions (tuple, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                        States what element vectors the empowerment info should be based on. 
                        Defaults to 'crawl300'.
        """
        # print info for user
        print('\nPlot similarity values for version {} with {} vectors.'.format(game_version, vector_version))

        # set attributes
        self.game_version = game_version
        self.vector_version = vector_version
        
        # set general settings for plotting 
        # TODO: change font to Open Sans
        sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth':0.6, 'grid.color': '#9d9d9d', 
                                                                                      'axes.linewidth':0.6, 'axes.edgecolor': '#9d9d9d'})      
        self.colors = ['#bf3409']
        sns.set_palette(sns.color_palette(self.colors))
        
        # plot values
        self.plot_similarity_histogram()
        
    def plot_similarity_histogram(self):
        """Plots similarity value distribution.
        """
        # set figure size
        plt.figure(figsize=(12,5))
        
        # import parent table 
        word_vectors = data_handle.get_wordvectors(self.game_version, self.vector_version)

        # get similarities
        similarities = cosine_similarity(word_vectors, word_vectors)
        
        # get combinations
        combination_table = data_handle.get_combination_table(self.game_version)
        successful_combinations = combination_table[combination_table['success'] == 1]
        unsuccessful_combinations = combination_table[combination_table['success'] == 0]
        
        # get similarities for unsuccessful and successful combinations
        similarity_list = list()
        successful_element_similarities = list()
        for combination in successful_combinations.to_numpy():
            successful_element_similarities.append(similarities[combination[0]][combination[1]])
        similarity_list.append(successful_element_similarities)

        unsuccessful_element_similarities = list()
        for combination in unsuccessful_combinations.to_numpy():
            unsuccessful_element_similarities.append(similarities[combination[0]][combination[1]])
        similarity_list.append(unsuccessful_element_similarities)
        
        for j in range(2):
            # plot data as histogram (density)
            plt.subplot(1,2,j+1)
            
            ax = sns.histplot(data=np.array(similarity_list[j]), kde=True, bins=20)

            # plot mean
            if len(ax.lines) != 0:
                kdeline = ax.lines[0]
                mean = np.array(similarity_list[j]).mean()
                print(mean)
                height = np.interp(mean, kdeline.get_xdata(), kdeline.get_ydata())
                ax.vlines(mean, 0, height, ls='dashed', color='#444444', linewidth=1)

            # set titles, labels
            plt.xlim(left=0)
            plt.xlabel('Similarity')
            plt.ylabel('Count')
            if j == 0:
                plt.title('Successful combinations')
            else:
                plt.title('Unsuccessful combinations')
            plt.tight_layout()
        
        # save figure
        filename = 'empowermentexploration/resources/littlealchemy/figures/{}SimilarityHistogram-{}'.format(self.game_version, self.vector_version)
        plt.savefig('{}.svg'.format(filename))
        plt.savefig('{}.png'.format(filename))
        plt.savefig('{}.pdf'.format(filename))
        plt.close()
