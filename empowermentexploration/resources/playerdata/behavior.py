import json
import time as ti

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

mpl.use('Agg')

class Behavior():
    """Class functions generate behavioral plots for playerdata.
    """
    def __init__(self, version='alchemy2', memory=True, trials=100, model_type='base'):
        """Initializes playerdata tiny class.

        Args:
            version (str, optional): 'alchemy2', 'tinyalchemy' or 'tinypixels'. States what game version is going to be used.
                        Defaults to 'alchemy2'.
            memory (boolean, optional): True if memory version of data is going to be used, False otherwise.
                        Defaults to True.
            trials (int, optional): Number of trials that will be plotted. Defaults to 100.
            model_type (str, optional): Model type, which is either 'base', 'emp', 'bin', 'trueemp',
                        'truebin', 'cbv', 'sim' or 'cbu' and is going to be used as a second data set. Defaults to 'base'.
        """
        # print info for user
        print('\nPlot player data statistics for version {}.'.format(version))

        # set attributes
        self.version = version
        self.memory = ''
        if memory is True:
            self.memory = 'Memory'
        self.trials = trials
        self.model_type = model_type

        # get number of elements
        if version == 'joined':
            self.n_elements = 738
        elif version == 'alchemy1' or version == 'tinyalchemy' or version == 'tinypixels':
            self.n_elements = 540
        elif version == 'alchemy2':
            self.n_elements = 720

        # read in data
        self.data = data_handle.get_player_data(version, memory)
        self.grouped_data = self.data.groupby('id')
        self.n_players = self.grouped_data.ngroups

        # set general settings for plotting
        # TODO: change font to Open Sans
        sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth':0.6, 'grid.color': '#9d9d9d',
                                                                                      'axes.linewidth': 0.6, 'axes.edgecolor': '#9d9d9d'})

        # plot behavior
        self.plot_final_inventory_sizes()
        self.plot_inventory_over_time()
        self.plot_trials()
        self.plot_immediate_usage()

    def plot_final_inventory_sizes(self):
        """ Plots distribution of final inventory sizes.
        """
        # print info
        print('\nPlot inventory sizes.')

        # set figure size
        if self.version == 'alchemy2':
            plt.figure(figsize=(4,6)) #if final inventory and number of trials in same plot
            #plt.figure(figsize=(7,6)) #if final inventory and number of trials in separate plots
        else:
            plt.figure(figsize=(5,4))

        # get inventory sizes
        inventory_sizes = self.grouped_data['inventory'].max()

        # plot data as histogram (density)
        ax = sns.histplot(data=inventory_sizes, kde=False, log_scale=True, bins=10, color='#82cafc')
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        ax.xaxis.get_major_formatter().set_scientific(False)
        plt.minorticks_off()

        # plot mean
        ax.axvline(inventory_sizes.mean(), ls='dashed', color='#444444', linewidth=1)
        print('Maximum inventory size: {}'.format(inventory_sizes.max()))
        print('Minimum inventory size: {}'.format(inventory_sizes.min()))
        print('Mean inventory size: {}'.format(inventory_sizes.mean()))
        print('Confidence Intervals:{}'.format(sm.stats.DescrStatsW(inventory_sizes).tconfint_mean(alpha = 0.05)))


        # set titles, labels
        if self.version == 'alchemy2':
            plt.ylim(bottom=0, top=9000)
            plt.xlim(left=inventory_sizes.min(), right=inventory_sizes.max())
        else:
            plt.ylim(bottom=0, top=25)
            plt.xlim(left=8, right=330)
        plt.xlabel('Final inventory')
        plt.ylabel('Count')

        # add label for mean
        # _, max_ylim = plt.ylim()
        # plt.text(inventory_sizes.mean()*1.3, max_ylim*0.85, 'Mean:\n{:.1f}'.format(inventory_sizes.mean()))
        plt.tight_layout()

        # save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanFinalInventorySizes{}.pdf'.format(self.version,self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanFinalInventorySizes{}.png'.format(self.version,self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanFinalInventorySizes{}.svg'.format(self.version,self.memory))
        plt.close()

    def plot_trials(self):
        """ Plots distribution of trials.
        """
        # print info
        print('\nPlot trial numbers.')

        # set figure size
        if self.version == 'alchemy2':
            plt.figure(figsize=(4,6))  #if final inventory and number of trials in same plot
            #plt.figure(figsize=(7,6))  #if final inventory and number of trials in separate plots
        else:
            plt.figure(figsize=(5,4))

        # get trial sizes
        trial_sizes = self.grouped_data['trial'].max().to_numpy()

        # plot data as histogram (density)
        ax = sns.histplot(data=trial_sizes + 1 , kde=False, log_scale=True, bins=10, color='#82cafc')
        ax.xaxis.set_major_formatter(mpl.ticker.ScalarFormatter())
        ax.xaxis.get_major_formatter().set_scientific(False)
        plt.minorticks_off()

        # plot mean
        ax.axvline(trial_sizes.mean(), ls='dashed', color='#444444', linewidth=1)
        print('Maximum trial size: {}'.format(trial_sizes.max()))
        print('Minimum trial size: {}'.format(trial_sizes.min()))
        print('Mean trial size: {}'.format(trial_sizes.mean()))
        print('Confidence Intervals:{}'.format(sm.stats.DescrStatsW(trial_sizes).tconfint_mean(alpha = 0.05)))


        # set titles, labels
        if self.version == 'alchemy2':
            plt.ylim(bottom=0, top=9000)
            plt.xlim(left=trial_sizes.min()+1, right=trial_sizes.max())
        else:
            plt.ylim(bottom=0, top=25)
            plt.xlim(left=6, right=2277)
        plt.xlabel('Total trials')
        plt.ylabel('Count')

        # add label for mean
        # _, max_ylim = plt.ylim()
        # plt.text(trial_sizes.mean()*1.3, max_ylim*0.85, 'Mean:\n{:.1f}'.format(trial_sizes.mean()))
        plt.tight_layout()

        # save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanFinalTrialSizes{}.pdf'.format(self.version,self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanFinalTrialSizes{}.png'.format(self.version,self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanFinalTrialSizes{}.svg'.format(self.version,self.memory))
        plt.close()

    def plot_inventory_over_time(self):
        """ Plots average inventory over time.
        """
        # print info
        print('\nPlot game progress.')

        # set figure size
        plt.figure(figsize=(12,5))

        # get average inventory over time, means and stds or sems
        trial_sizes = self.grouped_data['trial'].max()
        steps = range(0,trial_sizes.to_numpy().max()+1)

        # get human average inventory over time
        inventory_over_time_mean = self.data.groupby('trial')['inventory'].mean()
        inventory_over_time_sem = self.data.groupby('trial')['inventory'].sem()

        # plot line
        plt.plot(inventory_over_time_mean, color='#82cafc')

        # plot std
        plt.fill_between(steps, inventory_over_time_mean - inventory_over_time_sem,
                         inventory_over_time_mean + inventory_over_time_sem, alpha=0.1, color='#cfeafe')

        # set titles, labels, legends
        plt.xlabel('Trial')
        plt.ylabel('Inventory size')
        plt.xlim(left=0, right=trial_sizes.max())
        plt.ylim(bottom=0)
        plt.title('Game progress averaged over {} players'.format(self.n_players), loc='center', wrap=True)
        plt.tight_layout()

        # save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanAverageGameProgress{}.pdf'.format(self.version,self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanAverageGameProgress{}.png'.format(self.version,self.memory))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanAverageGameProgress{}.svg'.format(self.version,self.memory))
        plt.close()

        # set figure size
        plt.figure(figsize=(6,5))

        # get average inventory over time, means and stds or sems
        steps = range(0, self.trials)

        # get player subset
        trial_sizes = trial_sizes.loc[trial_sizes > self.trials-2]
        idx = trial_sizes.index
        player_subset = self.data.query('id in @idx & trial < @self.trials')

        # get human average inventory over time
        inventory_over_time_mean = player_subset.groupby('trial')['inventory'].mean()
        inventory_over_time_sem = player_subset.groupby('trial')['inventory'].sem()

        # plot line
        plt.plot(inventory_over_time_mean, color='#82cafc')

        # plot std
        plt.fill_between(steps, inventory_over_time_mean - inventory_over_time_sem,
                         inventory_over_time_mean + inventory_over_time_sem, alpha=0.1, color='#cfeafe')

        # set titles, labels, legends
        plt.xlabel('Trial')
        plt.ylabel('Inventory size')
        plt.xlim(left=0, right=self.trials+1)
        # TODO: adjust top accordingly to datasets
        plt.ylim(bottom=0, top=55)
        plt.title('Game progress averaged over {} players'.format(len(trial_sizes.index)), loc='center', wrap=True)
        plt.tight_layout()

        # save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanAverageGameProgress{}{}.pdf'.format(self.version, self.memory, self.trials))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanAverageGameProgress{}{}.png'.format(self.version, self.memory, self.trials))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}HumanAverageGameProgress{}{}.svg'.format(self.version, self.memory, self.trials))
        plt.close()

    def plot_immediate_usage(self):
        """ Plots percentage of immediate usage for human data vs random data.
        """
        # set figure size
        if self.version == 'alchemy2':
            plt.figure(figsize=(6.2,5))
        else:
            plt.figure(figsize=(6,3))

        # set color
        colors = ['#82cafc', '#cfeafe']
        if self.model_type == 'base':
            colors.extend(['#828282', '#a9a9a9'])
        elif self.model_type == 'emp' or self.model_type == 'trueemp':
            colors.extend(['#ffc640', '#ffdd83'])
        elif self.model_type == 'bin' or self.model_type == 'truebin':
            colors.extend(['#ff796c', '#ffc1ba'])
        elif self.model_type == 'cbu':
            colors.extend(['#0c2e8a', '#ae8782'])
        elif self.model_type == 'cbv':
            colors.extend(['#6ab8d9', '#a9d6e9'])
        elif self.model_type == 'sim':
            colors.extend(['#bf3409', '#f55422'])
        sns.set_palette(sns.color_palette(colors))

        # get memory information as integer
        memory = 0
        if self.memory == 'Memory':
            memory = 1

        # import player data
        data_storage = [(self.data,'human'), (data_handle.get_simulation_data(self.version, self.model_type, memory), helpers.translate_model(self.model_type))]

        for d in data_storage:
            # write data as numpy array
            data = d[0].values

            # get array length
            data_length = np.size(data, axis=0)

            # import empowerment values
            table = data_handle.get_parent_table(self.version)
            empowerment = np.zeros(self.n_elements)
            for element in table:
                empowerment[element] = len(table[element])

            element_index = np.arange(self.n_elements)

            # initialize storage
            element_used = np.zeros(self.n_elements)

            # initialize element count
            element_found = np.zeros(self.n_elements)

            #initialize mean trials
            element_trial_average = np.zeros(self.n_elements)

            #initialize mean number elements
            element_inventory_average = np.zeros(self.n_elements)

            # iterate over all rows
            player_id = 0
            for row in range(data_length):
                # ignore first row
                if row == 0:
                    continue

                # only look within same player and ignore first trial for each player
                if data[row][0] == data[row-1][0]:

                    # check if last trial led to new elements
                    elements = json.loads(data[row-1][6])
                    if elements != -1:
                        for element in elements:
                            element_found[element] += 1
                            element_trial_average[element] = element_trial_average[element] + ((1/element_found[element])*(data[row-1][1]-element_trial_average[element]))
                            element_inventory_average[element] = element_inventory_average[element] + ((1/element_found[element])*(data[row-1][2]-element_inventory_average[element]))

                            # check if element was used directly afterwards
                            if data[row][3] == element or data[row][4] == element:
                                element_used[element] += 1
                else:
                    player_id += 1

            #delete never used elements
            element_length = np.size(element_found, axis=0)

            index_without_unused = np.array([])
            element_found_without_unused = np.array([])
            element_used_without_unused = np.array([])
            empowerment_without_unused = np.array([])
            trials_without_unused = np.array([])
            inventory_without_unused = np.array([])

            for element in range(element_length):
                if element_found[element] != 0:
                    element_found_without_unused = np.append(element_found_without_unused, element_found[element])
                    element_used_without_unused = np.append(element_used_without_unused, element_used[element])
                    empowerment_without_unused = np.append(empowerment_without_unused, empowerment[element])
                    trials_without_unused = np.append(trials_without_unused, element_trial_average[element])
                    inventory_without_unused = np.append(inventory_without_unused, element_inventory_average[element])
                    index_without_unused = np.append(index_without_unused, element_index[element])
            element_found = element_found_without_unused
            element_used = element_used_without_unused
            empowerment = empowerment_without_unused
            element_trial_average = trials_without_unused
            element_inventory_average = inventory_without_unused
            element_index = index_without_unused

            # get percentage of immediate usage
            element_used_prob = np.nan_to_num(np.divide(element_used,element_found))

            #clean empowerment from final elements directly visible in LA2

            empowerment_clean = np.array([])
            element_used_clean = np.array([])
            element_found_clean = np.array([])
            element_used_prob_clean = np.array([])
            trials_clean = np.array([])
            inventory_clean = np.array([])
            element_index_clean = np.array([])

            if self.version == 'alchemy2':

                for i in range(len(empowerment)):
                    if empowerment[i] != 0:
                        element_index_clean = np.append(element_index_clean, element_index[i])
                        element_found_clean = np.append(element_found_clean, element_found[i])
                        element_used_clean = np.append(element_used_clean, element_used[i])
                        empowerment_clean = np.append(empowerment_clean, empowerment[i])
                        element_used_prob_clean = np.append(element_used_prob_clean, element_used_prob[i])
                        trials_clean = np.append(trials_clean, element_trial_average[i])
                        inventory_clean = np.append(inventory_clean, element_inventory_average[i])
                element_index = element_index_clean
                empowerment = empowerment_clean
                element_used_prob = element_used_prob_clean
                element_trial_average = trials_clean
                element_inventory_average = inventory_clean
                element_used = element_used_clean
                element_found = element_found_clean

            #create dataframe
            elem_index = element_index
            emp_log = np.log(empowerment+1)
            emp_raw = empowerment
            elem_found = element_found
            elem_used = element_used
            usage_prob = element_used_prob*100
            tri_ave = element_trial_average
            inv_ave = element_inventory_average

            df = pd.DataFrame()
            df['elem_index'] = pd.Series(elem_index)
            df['elem_found'] = pd.Series(elem_found)
            df['elem_used'] = pd.Series(elem_used)
            df['emp_log'] = pd.Series(emp_log)
            df['emp_raw'] = pd.Series(emp_raw)
            df['usage_prob'] = pd.Series(usage_prob)
            df['tri_ave'] = pd.Series(tri_ave)
            df['inv_ave'] = pd.Series(inv_ave)

            #write dataframe for R analysis
            time = ti.strftime('%Y%m%d-%H%M')
            filename_df_for_R = 'empowermentexploration/resources/playerdata/data/dataImUs/{}-{}-immediateusageWithoutLog-{}-{}.csv'.format(time, self.version, self.memory, d[1])
            df.to_csv(filename_df_for_R, index=False)

            #calculate correlation
            print(helpers.pearsonr_ci(df["emp_raw"],df["usage_prob"],alpha=0.05))

            # run glm and get predicted values
            df['const'] = 1
            model = sm.OLS(endog=df['usage_prob'], exog=df[['const','emp_log']]).fit()

            usage_prob_pred = model.predict()
            # sort data
            indx = np.argsort(emp_raw)
            emp_raw = emp_raw[indx]
            usage_prob = usage_prob[indx]
            usage_prob_pred = usage_prob_pred[indx]

            # plot data
            plt.plot(emp_raw, usage_prob_pred, linewidth=2, linestyle='-', label='{}'.format(d[1]))
            plt.plot(emp_raw, usage_prob, linewidth=0, marker='.')

        # set titles, labels, legends
        #plt.xlabel('log(number of offsprings)')
        plt.xlabel('log(number of offsprings)')
        plt.ylabel('Immediate usage in %')
        plt.xscale('log',subsx = [])
        plt.xticks([1,10,100],[1,10,100])

        plt.ylim(bottom=0, top=119)
        if self.version == 'alchemy2':
            plt.legend(loc='lower left', bbox_to_anchor=(0, 0.85, 1, 0.2), frameon=False, mode='expand', ncol=2)
        else:
            plt.legend(loc='lower left', bbox_to_anchor=(0, 0.7, 1, 0.2), frameon=False, mode='expand', ncol=2)
        plt.tight_layout()

        # save plot
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}-{}-ImmediateUsage{}{}.pdf'.format(time, self.version, self.memory, self.model_type))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}-{}-ImmediateUsage{}{}.png'.format(time, self.version, self.memory, self.model_type))
        plt.savefig('empowermentexploration/resources/playerdata/figures/{}-{}-ImmediateUsage{}{}.svg'.format(time, self.version, self.memory, self.model_type))
        plt.close()
