import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import time as ti
import statsmodels.api as sm
import scipy.stats as st
import time

import random

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers

time = time.strftime('%Y%m%d-%H%M')

# tinyalchemy, tinypixels, littlealchemy
game_version = 'alchemy2'
split_version = 'data'
vector_version = 'crawl300'
if game_version == "tinypixels" or game_version == "tinyalchemy":
    elementnumber = 540
else:
    elementnumber = 720


t = open("empowermentexploration/resources/littlealchemy/data/{}Elements.json".format(game_version))
translation = json.load(t)

d = open("empowermentexploration/resources/customgametree/data/{}ChildrenEmpowermentTable-{}-{}.json".format(game_version, split_version, vector_version))
data = json.load(d)
empvalues = []
index = []
for i in range(elementnumber):
    empvalues.append(len(data[str(i)]))
    index.append(i)
empowerment_table = pd.DataFrame(index, columns= ['index'])
empowerment_table["emp_value_predicted"] = empvalues
empowerment_table["element_string"] = translation

parenttable = data_handle.get_parent_table(version=game_version)
print(len(parenttable))
emp_list = []
for j in range(elementnumber):
    if(j in parenttable):
        emp_list.append(len(parenttable[j]))
    else:
        emp_list.append(0)
empowerment_table["emp_value_true"] = emp_list


# definitions for the axes
left, width = 0.1, 0.65
bottom, height = 0.1, 0.65
spacing = 0.01

x = empowerment_table["emp_value_predicted"]
y = empowerment_table["emp_value_true"]

empowerment_table['const'] = 1
model = sm.OLS(endog=empowerment_table["emp_value_true"], exog=empowerment_table[['const',"emp_value_predicted"]]).fit()
yhat = model.predict()
print(helpers.pearsonr_ci(x,y,alpha=0.05))
print(st.kendalltau(x,y))

rect_scatter = [left, bottom, width, height]
rect_histx = [left, bottom + height + spacing, width, 0.2]
rect_histy = [left + width + spacing, bottom, 0.2, height]

# start with a rectangular Figure
plt.figure(figsize=(4.5, 4.5))

ax_scatter = plt.axes(rect_scatter)
ax_scatter.tick_params(direction='in', top=True, right=True)

ax_histx = plt.axes(rect_histx)
ax_histx.tick_params(direction='in', labelbottom=False)
ax_histy = plt.axes(rect_histy)
ax_histy.tick_params(direction='in', labelleft=False)

# the scatter plot:
ax_scatter.scatter(x, y, 0.5, color = '#0c2e8a')
ax_scatter.plot(x, yhat, linewidth=1, linestyle='-', color = '#1140c2')
ax_scatter.set(xlabel = 'predicted empowerment value', ylabel = 'true empowerment value')

# now determine nice limits by hand:
binwidth = 1
limx = np.ceil(np.abs([x]).max() / binwidth) * binwidth
limy = np.ceil(np.abs([y]).max() / binwidth) * binwidth
ax_scatter.set_xlim((-1, limx+3))
ax_scatter.set_ylim((-1, limy+1))

binsx = np.arange(-1, limx+3 + binwidth, binwidth)
binsy = np.arange(-1, limy+1 + binwidth, binwidth)
ax_histx.hist(x, bins=binsx, color = '#0c2e8a')
ax_histx.set(ylabel='count', title="empowerment values" )
ax_histy.hist(y, bins=binsy, color = '#0c2e8a', orientation='horizontal')
ax_histy.set(xlabel='count')
ax_histx.set_xlim(ax_scatter.get_xlim())
ax_histy.set_ylim(ax_scatter.get_ylim())
#plt.show()
plt.savefig('empowermentexploration/data/gametree/figures/{}-EmpowermentValuesCorrelation{}.pdf'.format(time, game_version))
plt.savefig('empowermentexploration/data/gametree/figures/{}-EmpowermentValuesCorrelation{}.png'.format(time, game_version))
plt.savefig('empowermentexploration/data/gametree/figures/{}-EmpowermentValuesCorrelation{}.svg'.format(time, game_version))
