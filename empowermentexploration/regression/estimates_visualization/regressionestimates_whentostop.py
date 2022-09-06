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
#colors = ['#ffc640', '#0c2e8a']
#sns.set_palette(colors)

# set figure size
if game_version == 'alchemy2':
    plt.figure(figsize=(6.2,5))
else:
    plt.figure(figsize=(6,3))

# plot barplot
if game_version == 'alchemy2':
    plt.errorbar(x=['empowerment', 'success'], y=[0.41545,-0.31173], yerr = [1.96*0.009721, 1.96*0.009506], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'success'], height=[0.41545,-0.31173], color=['#0c2e8a','#ffc640'])
elif game_version == 'tinyalchemy':
    plt.errorbar(x=['empowerment', 'success'], y=[0.6431, -0.1213], yerr = [1.96*0.2394, 1.96*0.1415], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'success'], height=[0.6431, -0.1213], color=['#0c2e8a','#ffc640'])
elif game_version == 'tinypixels': 
    plt.errorbar(x=['empowerment', 'success'], y=[0.2686, 0.5173], yerr = [1.96*0.3432, 1.96*0.2868], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'success'], height=[0.2686, 0.5173], color=['#0c2e8a','#ffc640'])

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
    axes.set_ylim([-0.5,1.2])
plt.tight_layout()

# save plot
plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates_whentostop.png'.format(game_version))
plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates_whentostop.svg'.format(game_version))
plt.close()
