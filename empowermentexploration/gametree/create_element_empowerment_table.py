import json
import numpy as np
import pandas as pd

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers

# tinyalchemy, tinypixels, alchemy2
#specify game version for which you want to create the game tree
game_version = 'tinypixels'

#no changes from here on
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

p = open("empowermentexploration/resources/littlealchemy/data/{}ParentTable.json".format(game_version))
parenttable = json.load(p)
parenttable = data_handle.get_parent_table(version=game_version)
print(len(parenttable))
emp_list = []
for j in range(elementnumber):
    if(j in parenttable):
        emp_list.append(len(parenttable[j]))
    else:
        emp_list.append(0)
empowerment_table["emp_value_true"] = emp_list
print(empowerment_table)
empowerment_table.to_csv("empowermentexploration/data/gametree/element_empowerment/{}_element_empowerment_dataframe.csv".format(game_version), index = False)
