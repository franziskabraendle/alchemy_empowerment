import json
from itertools import combinations_with_replacement

import empowermentexploration.utils.data_handle as data_handle
import pandas as pd


table_type='child'
version='tinyalchemy'
expand = False


# print info for user
print('\nGet table of type {} for version {}.'.format(table_type, version))

with open('empowermentexploration/resources/littlealchemy/data/{}Gametree.json'.format(version),
          encoding='utf8') as infile:
    gametree = json.load(infile)
    gametree = {int(k):v for k,v in gametree.items()}
# get game tree

# initialize search table and parent respectively child table
table = dict()
table_csv = list()

# traverse through game tree
for element in gametree:
    for parent in gametree[element]["parents"]:
        # sort parents
        parent = sorted(parent)

        if table_type == 'combination':
            # assign resulting elements to combination elements
            if parent[0] not in table:
                table[parent[0]] = {}
            if parent[1] not in table:
                table[parent[1]] = {}
            if parent[1] not in table[parent[0]]:
                table[parent[0]][parent[1]] = [element]
            elif element not in table[parent[0]][parent[1]]:
                table[parent[0]][parent[1]].append(element)
            if parent[0] not in table[parent[1]]:
                table[parent[1]][parent[0]] = [element]
            elif element not in table[parent[1]][parent[0]]:
                table[parent[1]][parent[0]].append(element)

            table_csv.append({'first': parent[0], 'second': parent[1], 'result': element})

        elif table_type == 'parent':
            # add resulting element to parent list for each combination element
            if parent[0] not in table:
                table[parent[0]] = {element}
            else:
                table[parent[0]].update([element])
            if parent[1] not in table:
                table[parent[1]] = {element}
            else:
                table[parent[1]].update([element])

        elif table_type == 'child':
            # add parents to child list for resulting element
            if element not in table:
                table[element] = set(parent)
            else:
                table[element].update(parent)

if table_type == 'parent' or table_type == 'child':
    # adjust to list to successfully write to JSON file
    for element in table:
        table[element] = list(table[element])

    # transform into DataFrame
    table_csv = pd.DataFrame({key:pd.Series(value) for key, value in table.items()})
else:
    table_csv = pd.DataFrame(table_csv)
    if expand is True:
        table_csv = self.expand_combination_table(table_csv, version)

# write to JSON file
with open('empowermentexploration/resources/littlealchemy/data/{}{}Table.json'.format(version, table_type.capitalize()), 'w') as filehandle:
    json.dump(table, filehandle, indent=4, sort_keys=True)

# replace nan values with -1
table_csv = table_csv.fillna(-1)

# write to csv file
table_csv.to_csv('empowermentexploration/resources/littlealchemy/data/{}{}Table.csv'.format(version, table_type.capitalize()), index=False, float_format='%.f')
