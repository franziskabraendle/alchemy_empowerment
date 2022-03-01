import empowermentexploration.utils.data_handle as data_handle
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

mpl.use('Agg')

class Empowerment():
    """Class function plots empowerment values.
    """
    def __init__(self, game_version, split_version='data', vector_version='crawl300'):
        """Initializes empowerment class.
        
        Args:
            game_version (str): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used.
            split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on. 
                        Defaults to 'data'.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                        States what element vectors the empowerment info should be based on. 
                        Defaults to 'crawl300'.
        """
        # print info for user
        print('\nPlot empowerment values for version {} with the custom gametree based on {} split and {} vectors.'.format(game_version, split_version, vector_version))
        
        # set attributes
        self.game_version = game_version
        self.split_version = split_version
        self.vector_version = vector_version
        self.empowerment = list()
        
        # set general settings for plotting 
        # TODO: change font to Open Sans
        sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth':0.6, 'grid.color': '#9d9d9d', 
                                                                                      'axes.linewidth':0.6, 'axes.edgecolor': '#9d9d9d'})      
        self.colors = ['#ffc640']
        sns.set_palette(sns.color_palette(self.colors))
        
        # plot values
        self.plot_empowerment_histogram()
        self.plot_empowerment_scatter_plot()
            
    def plot_empowerment_histogram(self):
        """Plots empowerment value distribution.
        """
        # get number of elements
        if self.game_version == 'joined':
            n_elements = 738
        elif self.game_version == 'alchemy1' or self.game_version == 'tinyalchemy' or self.game_version == 'tinypixels':
            n_elements = 540
        elif self.game_version == 'alchemy2':
            n_elements = 720
        else:
            raise ValueError('Undefined version: "{}". Use "alchemy1", "alchemy2" or "joined" instead.'.format(self.game_version))

        # set figure size
        plt.figure(figsize=(12,5))
        
        for i in range(2):
            # import parent table 
            if i == 0:
                parents = data_handle.get_parent_table(self.game_version)
            else:
                parents = data_handle.get_custom_parent_table(self.game_version, self.split_version, self.vector_version)

            # get array of empowerment values
            empowerment = np.zeros(n_elements)
            for element_id in range(n_elements):
                if element_id in parents:
                    empowerment[element_id] = len(parents[element_id])
                else:
                    empowerment[element_id] = 0
            self.empowerment.append(empowerment)

            # plot data as histogram (density)
            plt.subplot(1,2,i+1)
            ax = sns.histplot(data=empowerment, kde=True, bins=20)
            #x.set_xscale('log')
            #ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
            #ax.xaxis.get_major_formatter().set_scientific(False)
            #plt.minorticks_off()

            # plot mean
            if len(ax.lines) != 0:
                kdeline = ax.lines[0]
                mean = empowerment.mean()
                print(mean)
                height = np.interp(mean, kdeline.get_xdata(), kdeline.get_ydata())
                ax.vlines(mean, 0, height, ls='dashed', color='#444444', linewidth=1)
                
            # set titles, labels
            #plt.xlim(left=0)
            plt.xlabel('Empowerment')
            plt.ylabel('Count')
            plt.tight_layout()
            
        # save figure
        filename = 'empowermentexploration/resources/littlealchemy/figures/{}EmpowermentHistogram-{}-{}'.format(self.game_version, self.split_version, self.vector_version)
        plt.savefig('{}.svg'.format(filename))
        plt.savefig('{}.png'.format(filename))
        plt.savefig('{}.pdf'.format(filename))
        plt.close()

    def plot_empowerment_scatter_plot(self):
        """Plots empowerment value distribution.
        """
        # make scatter/regression plot 
        g = sns.jointplot(x=self.empowerment[0], y=self.empowerment[1], kind="reg")
        g.ax_joint.set_xscale('log')
        g.ax_joint.set_yscale('log')
        g.ax_joint.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        g.ax_joint.xaxis.get_major_formatter().set_scientific(False)
        g.ax_joint.yaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        g.ax_joint.yaxis.get_major_formatter().set_scientific(False)
        
        # set titles, labels
        plt.xlabel('True empowerment')
        plt.ylabel('Predicted empowerment')
        plt.tight_layout()
        
        # save figure
        filename = 'empowermentexploration/resources/littlealchemy/figures/{}EmpowermentRegression-{}-{}'.format(self.game_version, self.split_version, self.vector_version)
        plt.savefig('{}.svg'.format(filename))
        plt.savefig('{}.png'.format(filename))
        plt.savefig('{}.pdf'.format(filename))
        plt.close()
