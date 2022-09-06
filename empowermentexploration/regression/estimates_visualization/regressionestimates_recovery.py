import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

mpl.use('Agg')

# set data version (base, cbu, emp, bin)
data_version = 'cbu'
#set if with or without bin (True, False)
with_bin = False

# set general settings for plotting
# TODO: change font to Open Sans
sns.set_theme(context='paper', style='ticks', font='Arial', font_scale=2, rc={'lines.linewidth': 2, 'grid.linewidth': 0.6, 'grid.color': '#9d9d9d',
                                                                              'axes.linewidth': 0.6, 'axes.edgecolor': '#9d9d9d'})
# set color
if with_bin:
    colors = ['#0c2e8a','#178259','#ff796c']
else:
    colors = ['#0c2e8a','#ff796c']
sns.set_palette(colors)

# set figure size
plt.figure(figsize=(6.2,5))

if data_version == 'emp': #values from 01.09.2022
    plt.errorbar(x=['empowerment', 'uncertainty'], y=[3.296459, 0.700077], yerr = [1.96*0.015023,  1.96*0.009145], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'uncertainty'], height=[3.296459, 0.700077], color=['#0c2e8a', '#ff796c'])
elif data_version == 'cbu': #values from 01.09.2022
    plt.errorbar(x=['empowerment', 'uncertainty'], y=[-0.074895, 22.574845], yerr = [1.96*0.008028, 1.96*0.126821], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'uncertainty'], height=[-0.074895, 22.574845], color=['#0c2e8a','#ff796c'])
elif data_version == 'base': #values from 01.09.2022
    plt.errorbar(x=['empowerment', 'uncertainty'], y=[-0.029381, 0.455752], yerr = [1.96*0.004630, 1.96*0.005034], color = '#444444', fmt='none', elinewidth=3)
    g = plt.bar(x=['empowerment', 'uncertainty'], height=[-0.029381, 0.455752], color=['#0c2e8a','#ff796c'])

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

plt.tight_layout()

# save plot
if with_bin:
    plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates.png'.format(data_version))
    plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates.svg'.format(data_version))
else:
   plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates_withoutbin.png'.format(data_version))
   plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates_withoutbin.svg'.format(data_version))

plt.close()
