import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import matplotlib as mpl
import matplotlib.colors as c
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy.stats import sem

mpl.use('Agg')

class Visualization():
    """Visualization model.
    """
    def __init__(self, game_version, time, model_type, temperatures, runs, steps, memory_type, empowerment_calculation=None):
        """Initializes visualization.

        Args:
            game_version (str):
            time (str): Time that will be used as folder name for saving pictures.
            model_type (str or list): Model(s) that the plots are for.
            temperatures (list): List of temperatures for which simulations are run.
            runs (int): Number of simulations.
            steps (int): Number of steps for each simulation.
            memory_type (int, optional): States whether it should be memorized what combinations have been used before. There are different options
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 10 steps)
            empowerment_calculation (tuple, optional): Tuple made of three entries. Defaults to None.
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                    or length of set of resulting elements.
        """
        # set attributes
        self.game_version = game_version
        self.time = time
        self.model_type = model_type
        self.temperatures = temperatures
        self.runs = runs
        self.steps = steps
        self.memory_type = memory_type
        self.empowerment_calculation = empowerment_calculation

        # set general settings for plotting
        # TODO: change font to Open Sans
        sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth':0.6, 'grid.color': '#9d9d9d',
                                                                                      'axes.linewidth':0.6, 'axes.edgecolor': '#9d9d9d'})
        # set color
        color = '#828282'
        if self.model_type == 'base':
            color = '#828282'
        elif self.model_type == 'emp' or self.model_type == 'trueemp':
            color = '#0c2e8a'
            #color = '#ffc640' '#0c2e8a'
        elif self.model_type == 'bin' or self.model_type == 'truebin':
            color = '#ffc640'
            #color = '#ff796c' '#ffc640'
        elif self.model_type == 'cbu':
            color = '#ff796c'
            #color = '#0c2e8a' '#ff796c'
        elif self.model_type == 'cbv':
            color = '#6ab8d9'
        elif self.model_type == 'sim':
            color = '#bf3409'
        color = c.to_rgba(color)
        self.colors = [color]
        if temperatures is not None and len(temperatures) > 1:
            j = 1
            for _ in range(len(self.temperatures)-1):
                j += 0.2
                self.colors.append(helpers.adjust_lightness(color,j))
        sns.set_palette(sns.color_palette(self.colors))

    def plot_gameprogress(self, inventory):
        """Plots game progress and saves file as PNG.

        Args:
            inventory (Inventory): Inventory info.
        """
        # print info
        print('\nPlot game progress.')

        # plot data for each temperature
        for t, temperature in enumerate(self.temperatures):
            # get average inventory over time, means and stds
            steps = range(0,self.steps+1)
            inventory_over_time = np.squeeze(inventory.inventory_size_over_time[t,:,:])
            inventory_over_time_mean = np.mean(inventory_over_time, axis=0)
            inventory_over_time_sem = sem(inventory_over_time, axis=0)

            # plot line
            if self.model_type == 'base':
                plt.plot(inventory_over_time_mean)
            else:
                plt.plot(inventory_over_time_mean, label='T={}'.format(temperature))

            # plot std
            plt.fill_between(steps, inventory_over_time_mean - inventory_over_time_sem,
                             inventory_over_time_mean + inventory_over_time_sem, alpha=0.1)

        # set titles, labels, legends
        plt.xlabel('Trial')
        plt.ylabel('Inventory size')
        plt.xlim(left=0, right=self.steps)
        plt.ylim(bottom=0)
        if self.model_type != 'base':
            plt.legend(loc=0, frameon=False)
        model = helpers.translate_model(self.model_type)
        #plt.title('Game progress averaged over {} runs, model={}'.format(self.runs, model), loc='center', wrap=True)
        plt.tight_layout()
        if self.model_type in ['emp', 'trueemp', 'bin', 'truebin']:
            plt.savefig('empowermentexploration/data/models/{}/{}-{}-{}-memory{}-averageGameProgress.svg'.format(self.time, self.game_version, self.model_type, self.empowerment_calculation, self.memory_type))
            plt.savefig('empowermentexploration/data/models/{}/{}-{}-{}-memory{}-averageGameProgress.png'.format(self.time, self.game_version, self.model_type, self.empowerment_calculation, self.memory_type))
        else:
            plt.savefig('empowermentexploration/data/models/{}/{}-{}-memory{}-averageGameProgress.svg'.format(self.time, self.game_version, self.model_type, self.memory_type))
            plt.savefig('empowermentexploration/data/models/{}/{}-{}-memory{}-averageGameProgress.png'.format(self.time, self.game_version, self.model_type, self.memory_type))
        plt.close()

    def plot_inventory_sizes(self, inventory, temperature_idx):
        """Plots density of inventory sizes.

        Args:
            inventory: (Inventory): Inventory info.
            temperature_idx (int): Index of given temperature.
        """
        # print info
        print('\nPlot inventory sizes.')

        # get inventory sizes
        inventory_sizes = np.squeeze(inventory.inventory_size_over_time[temperature_idx,:,-1])

        # plot data as histogram (density)
        ax = sns.histplot(data=inventory_sizes, kde=True)

        # plot mean
        if len(ax.lines) != 0:
            kdeline = ax.lines[0]
            mean = inventory_sizes.mean()
            height = np.interp(mean, kdeline.get_xdata(), kdeline.get_ydata())
            ax.vlines(mean, 0, height, ls='dashed', color='#444444', linewidth=1)

        # set titles, labels
        plt.xlabel('Inventory size')
        plt.ylabel('Count')
        model = helpers.translate_model(self.model_type)
        if self.model_type == 'base':
            #plt.title('Density of inventory sizes at {} runs, model={}'.format(self.runs, model), loc='center', wrap=True)
            plt.tight_layout()
            plt.savefig('empowermentexploration/data/models/{}/{}-memory{}-inventorySizes.svg'.format(self.time, self.model_type, self.memory_type))
            plt.savefig('empowermentexploration/data/models/{}/{}-memory{}-inventorySizes.png'.format(self.time, self.model_type, self.memory_type))
        elif self.model_type in ['emp', 'trueemp', 'bin', 'truebin']:
            #plt.title('Density of inventory sizes at {} runs, model={}, T={}'.format(self.runs, model, self.temperatures[temperature_idx]), loc='center', wrap=True)
            plt.tight_layout()
            plt.savefig('empowermentexploration/data/models/{}/{}-{}-memory{}-temperature{}-inventorySizes.svg'.format(self.time, self.model_type, self.empowerment_calculation, self.memory_type, self.temperatures[temperature_idx]))
            plt.savefig('empowermentexploration/data/models/{}/{}-{}-memory{}-temperature{}-inventorySizes.png'.format(self.time, self.model_type, self.empowerment_calculation, self.memory_type, self.temperatures[temperature_idx]))
        else:
            #plt.title('Density of inventory sizes at {} runs, model={}, T={}'.format(self.runs, model, self.temperatures[temperature_idx]), loc='center', wrap=True)
            plt.tight_layout()
            plt.savefig('empowermentexploration/data/models/{}/{}-memory{}-temperature{}-inventorySizes.svg'.format(self.time, self.model_type, self.memory_type, self.temperatures[temperature_idx]))
            plt.savefig('empowermentexploration/data/models/{}/{}-memory{}-temperature{}-inventorySizes.png'.format(self.time, self.model_type, self.memory_type, self.temperatures[temperature_idx]))

        plt.close()

    def plot_all(self, value_calculation, human=True):
        """Plots gameprogress curves for all run models and humans for comparison.

        Args:
            value_calculation (tuple): Tuple containing first calculation info on model trueemp, then emp, then truebin and bin.
            human (boolean, optional): True if plot for human should be added as well, False if not. Defaults to True.
        """
        # print info
        print('\nPlot game progress.')

        # set figure size
        plt.figure(figsize=(6.2,5))

        # initialize variable storing maximum
        max = -1

        # read in model data
        for model_type in self.model_type:
            # plot human line eralier in case of special model arrangement
            if human is True and np.all(self.model_type == ['base','cbu', 'truebin', 'trueemp']) and model_type == 'truebin':
                # set color
                colors = ['#82cafc', '#d9effe']

                # read in human data
                memory = False
                if self.memory_type == 1:
                    memory = True
                data = data_handle.get_player_data('alchemy2', memory=memory)
                grouped_data = data.groupby('id')

                # get player subset
                trial_sizes = grouped_data['trial'].max()
                trial_sizes = trial_sizes.loc[trial_sizes > self.steps-2]
                idx = trial_sizes.index
                player_subset = data.query('id in @idx & trial < @self.steps')

                # get human average inventory over time
                inventory_over_time_mean = player_subset.groupby('trial')['inventory'].mean()
                inventory_over_time_sem = player_subset.groupby('trial')['inventory'].sem()

                # plot line
                plt.plot(inventory_over_time_mean, label='human', color=colors[0])

                # plot std
                plt.fill_between(range(0,self.steps), inventory_over_time_mean - inventory_over_time_sem,
                                inventory_over_time_mean + inventory_over_time_sem, alpha=0.1, color=colors[1])

            # set color
            if model_type == 'base':
                colors = ['#828282', '#a9a9a9']
            elif model_type == 'emp' or model_type == 'trueemp':
                colors = ['#0c2e8a', '#ae8782']
                #colors = ['#ffc640', '#ffdd83'] ['#0c2e8a', '#ae8782']
            elif model_type == 'bin' or model_type == 'truebin':
                colors = ['#ffc640', '#ffdd83']
                #colors = ['#ff796c', '#ffc1ba'] ['#ffc640', '#ffdd83']
            elif model_type == 'cbu':
                colors = ['#ff796c', '#ffc1ba']
                #colors = ['#0c2e8a', '#ae8782'] ['#ff796c', '#ffc1ba']
            elif model_type == 'cbv':
                colors = ['#6ab8d9', '#a9d6e9']
            elif model_type == 'sim':
                colors = ['#bf3409', '#f55422']

            # set empowerment_calculation
            if model_type == 'trueemp':
                empowerment_calculation = value_calculation[0]
            elif model_type == 'emp':
                empowerment_calculation = value_calculation[1]
            elif model_type in ['truebin']:
                empowerment_calculation = value_calculation[2]
            elif model_type in ['bin']:
                empowerment_calculation = value_calculation[3]
            else:
                empowerment_calculation = ['placeholder']
            for e_c in empowerment_calculation:
                if model_type in ['trueemp', 'emp', 'bin', 'truebin']:
                    data = data_handle.get_gameprogress_data(self.time, self.game_version, '{}-{}'.format(model_type, e_c), self.memory_type)
                else:
                    data = data_handle.get_gameprogress_data(self.time, self.game_version, model_type, self.memory_type)

                # get temperature value resulting in highest average inventory size
                t_max = -1
                t = 0
                if model_type != 'base':
                    for temperature in range(len(self.temperatures)):
                        inventory_over_time = np.squeeze(data['out'][temperature,:,self.steps])
                        if np.mean(inventory_over_time, axis=0) > t_max:
                            t_max = np.mean(inventory_over_time, axis=0)
                            t = temperature

                # plot gameprogress curve
                inventory_over_time = np.squeeze(data['out'][t,:,:self.steps])
                inventory_over_time_mean = np.mean(inventory_over_time, axis=0)
                inventory_over_time_sem = sem(inventory_over_time, axis=0)

                # check if maximum
                if np.max(inventory_over_time_mean) > max:
                    max = np.max(inventory_over_time_mean)

                # plot line
                plt.plot(inventory_over_time_mean, label=helpers.translate_model(model_type), color=colors[0])

                # plot std
                plt.fill_between(range(0,self.steps), inventory_over_time_mean - inventory_over_time_sem,
                                 inventory_over_time_mean + inventory_over_time_sem, alpha=0.1, color=colors[1])

        if human is True and not np.all(self.model_type == ['base','cbu', 'truebin', 'trueemp']):
            # set color
            colors = ['#82cafc', '#cfeafe']

            # read in human data
            memory = False
            if self.memory_type == 1:
                memory = True
            data = data_handle.get_player_data('alchemy2', memory=memory)
            grouped_data = data.groupby('id')

            # get player subset
            trial_sizes = grouped_data['trial'].max()
            trial_sizes = trial_sizes.loc[trial_sizes > self.steps-2]
            idx = trial_sizes.index
            player_subset = data.query('id in @idx & trial < @self.steps')

            # get human average inventory over time
            inventory_over_time_mean = player_subset.groupby('trial')['inventory'].mean()
            inventory_over_time_sem = player_subset.groupby('trial')['inventory'].sem()

            # plot line
            plt.plot(inventory_over_time_mean, label='human', color=colors[0])

            # plot std
            plt.fill_between(range(0,self.steps), inventory_over_time_mean - inventory_over_time_sem,
                             inventory_over_time_mean + inventory_over_time_sem, alpha=0.1, color=colors[1])

        # set titles, labels, legends
        plt.xlabel('Trial')
        plt.ylabel('Inventory size')
        plt.xlim(left=0, right=self.steps)
        plt.ylim(bottom=0, top=max+max/4)
        #plt.yticks(np.arange(0, max+5, 20))
        plt.legend(loc='lower left', bbox_to_anchor=(0, 0.66, 1.02, 0.2), frameon=False, mode='expand', ncol=2)
        # plt.title('Game progress comparison, averaged over {} runs, memory={}'.format(self.runs, self.memory_type), loc='center', wrap=True)
        plt.tight_layout()

        plt.savefig('empowermentexploration/data/models/{}/{}-averageGameProgressAll.pdf'.format(self.time, self.game_version))
        plt.savefig('empowermentexploration/data/models/{}/{}-averageGameProgressAll.png'.format(self.time, self.game_version))
        plt.savefig('empowermentexploration/data/models/{}/{}-averageGameProgressAll.svg'.format(self.time, self.game_version))
        plt.close()
