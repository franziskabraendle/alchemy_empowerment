import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.weightstats as ssw
from numpy import std, mean, sqrt

def cohen_d(x,y):
    nx = len(x)
    ny = len(y)
    dof = nx + ny - 2
    return (mean(x) - mean(y)) / sqrt(((nx-1)*std(x, ddof=1) ** 2 + (ny-1)*std(y, ddof=1) ** 2) / dof)


tinyalchemy_data = data_handle.get_player_data("tinyalchemy", "Memory")
tinypixels_data = data_handle.get_player_data("tinypixels", "Memory")


ta_grouped = tinyalchemy_data.groupby('id')
tp_grouped = tinypixels_data.groupby('id')
ta_inventory_sizes = ta_grouped['inventory'].max()
tp_inventory_sizes = tp_grouped['inventory'].max()



print(ssw.ttest_ind(ta_inventory_sizes, tp_inventory_sizes))
print(cohen_d(ta_inventory_sizes, tp_inventory_sizes))
ta_trials = ta_grouped['trial'].max().to_numpy()
tp_trials = tp_grouped['trial'].max().to_numpy()

print(ssw.ttest_ind(ta_trials, tp_trials))
print(cohen_d(ta_trials, tp_trials))
#correct if the population S.D. is expected to be equal for the two groups.
