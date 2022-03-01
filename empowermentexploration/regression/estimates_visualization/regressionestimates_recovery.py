import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

mpl.use('Agg')

# set data version (base, cbu, emp, bin)
data_version = 'bin'
#set if with or without bin (True, False)
with_bin = True

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

if with_bin:
    if data_version == 'emp': #values from 25.11.2021
        plt.errorbar(x=['empowerment', 'success-only', 'uncertainty'], y=[3.1005, 0.5432, 0.8300], yerr = [1.96*0.0157, 1.96*0.0128, 1.96*0.0098], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'success-only', 'uncertainty'], height=[3.1005, 0.5432, 0.8300], color=['#0c2e8a','#178259','#ff796c'])
    elif data_version == 'cbu': #values from 25.11.2021
        plt.errorbar(x=['empowerment', 'success-only', 'uncertainty'], y=[-0.09991, 0.02388, 22.60695], yerr = [1.96*0.01224, 1.96*0.01194, 1.96*0.12726], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'success-only', 'uncertainty'], height=[-0.09991, 0.02388, 22.60695], color=['#0c2e8a','#178259','#ff796c'])
    elif data_version == 'base': #values from 25.11.2021
        plt.errorbar(x=['empowerment', 'success-only', 'uncertainty'], y=[-0.026290, -0.018520, 0.456168], yerr = [1.96*0.007219, 1.96*0.007215, 1.96*0.005042], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'success-only', 'uncertainty'], height=[-0.026290, -0.018520, 0.456168], color=['#0c2e8a','#178259','#ff796c'])
    elif data_version == 'bin': #values from 26.11.2021
        plt.errorbar(x=['empowerment', 'success-only', 'uncertainty'], y=[-0.144980, 10.0388, 1.32426], yerr = [1.96*0.01455, 1.96*0.067496, 1.96*0.013516], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'success-only', 'uncertainty'], height=[-0.144980, 10.0388, 1.32426], color=['#0c2e8a','#178259','#ff796c'])

else:
    if data_version == 'emp': #values from 25.11.2021
        plt.errorbar(x=['empowerment', 'uncertainty'], y=[3.3156, 0.7061], yerr = [1.96*0.0152,  1.96*0.0092], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'uncertainty'], height=[3.3156, 0.7061], color=['#0c2e8a', '#ff796c'])
    elif data_version == 'cbu': #values from 25.11.2021
        plt.errorbar(x=['empowerment', 'uncertainty'], y=[-0.036, 75.531], yerr = [1.96*0.0105, 1.96*0.8042], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'uncertainty'], height=[-0.036, 75.531], color=['#0c2e8a','#ff796c'])
    elif data_version == 'base': #values from 25.11.2021
        plt.errorbar(x=['empowerment', 'uncertainty'], y=[-0.0409, 0.455], yerr = [1.96*0.0046, 1.96*0.0051], color = '#444444', fmt='none', elinewidth=3)
        g = plt.bar(x=['empowerment', 'uncertainty'], height=[-0.0409, 0.455], color=['#0c2e8a','#ff796c'])

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
#if data_version == 'tinyalchemy' or data_version == 'tinypixels':
#    axes.set_ylim([-0.1,0.4])
plt.tight_layout()

# save plot
if with_bin:
    plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates.png'.format(data_version))
    plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates.svg'.format(data_version))
else:
   plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates_withoutbin.png'.format(data_version))
   plt.savefig('empowermentexploration/data/regression/figures/{}RegressionEstimates_withoutbin.svg'.format(data_version))

plt.close()
