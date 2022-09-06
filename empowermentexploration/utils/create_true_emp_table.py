import empowermentexploration.utils.data_handle as data_handle
import numpy as np
import pandas as pd
from itertools import combinations_with_replacement

#creates table with the true empowerment values for each possible combination.

#choose game version "alchemy2", "tinyalchemy", "tinypixels"
game_version = "tinyalchemy"

parent_table = data_handle.get_parent_table(game_version)
combination_table = data_handle.get_combination_table(game_version, csv=False)

if game_version == "alchemy2":
    number_of_elements = 720
else:
    number_of_elements = 540

if game_version == "alchemy2":
    number_of_combinations = 259560
else:
    number_of_combinations = 146070

items = list(range(0,number_of_elements))
emp_array = np.zeros((number_of_combinations,3))
emp_array[:,2] = -1
counter = 0
for(combination) in combinations_with_replacement(items, 2):
    emp_array[counter][0]=combination[0]
    emp_array[counter][1]=combination[1]

    # check results of combination
    if combination[0] in combination_table and combination[1] in combination_table[combination[0]]:
        results = combination_table[combination[0]][combination[1]]
    else:
        results = list()

    # initialize empowerment depending on how it is calculated
    empowerment = set()

    # calculate empowerment value iteratively for each result
    for r in results:
        if r in parent_table:
            empowerment.update(parent_table[r])
    if len(results) != 0:
        emp_array[counter][2] = len(empowerment)
    counter+=1

print(emp_array[:10])
print(emp_array[-10:])
df = pd.DataFrame(emp_array, columns=['Element1','Element2','Trueemp'])
filename = 'empowermentexploration/resources/littlealchemy/trueemp_table.csv'
df.to_csv(filename, index=False)
