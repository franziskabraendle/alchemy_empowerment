import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

mpl.use('Agg')

# set game version
game_version = 'tinypixels'

# set general settings for plotting
# TODO: change font to Open Sans
sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth': 0.6, 'grid.color': '#9d9d9d',
                                                                              'axes.linewidth': 0.6, 'axes.edgecolor': '#9d9d9d'})
# set color
colors = ['#ffc640', '#0c2e8a']
sns.set_palette(colors)

# set figure size
if game_version == 'alchemy2':
    plt.figure(figsize=(6.2,5))
else:
    plt.figure(figsize=(6,3))

# plot barplot
if game_version == 'alchemy2':
    #plt.errorbar(x=['empowerment', 'uncertainty'], y=[0.248022, 0.888754], yerr = [1.96*0.004628, 1.96*0.005257], color = '#444444', fmt='none', elinewidth=3)
    #g = plt.bar(x=['empowerment', 'uncertainty'], height=[0.248022, 0.888754], color=['#ffc640', '#0c2e8a'])
    plt.errorbar(x=['empowerment', 'uncertainty'], y=[0.3776, 0.2233], yerr = [1.96*0.001024, 1.96*0.001091], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'uncertainty'], height=[0.3776, 0.2233], color=['#0c2e8a','#ff796c'])
elif game_version == 'tinyalchemy': #values from 11.10.2021
    plt.errorbar(x=['empowerment', 'uncertainty'], y=[0.322388, 0.100159], yerr = [1.96*0.010213, 1.96*0.010232], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'uncertainty'], height=[0.322388, 0.100159], color=['#0c2e8a','#ff796c'])
elif game_version == 'tinypixels': #values from 11.10.2021
    plt.errorbar(x=['empowerment', 'uncertainty'], y=[-0.109565, 0.080353], yerr = [1.96*0.016336, 1.96*0.016749], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'uncertainty'], height=[-0.109565, 0.080353], color=['#0c2e8a','#ff796c'])

#function for changing width of bars
def change_width(ax, new_value) :
    for patch in ax.patches :
        current_width = patch.get_width()
        diff = current_width - new_value

        # we change the bar width
        patch.set_width(new_value)

        # we recenter the bar
        patch.set_x(patch.get_x() + diff * 0.5)


# set titles, labels,
plt.ylabel('Regression')
plt.xlabel('Models')
axes = plt.gca()
change_width(axes, .58)
if game_version == 'tinyalchemy' or game_version == 'tinypixels':
    axes.set_ylim([-0.15,0.4])
plt.tight_layout()

# save plot
plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates.png'.format(game_version))
plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates.svg'.format(game_version))
plt.close()
