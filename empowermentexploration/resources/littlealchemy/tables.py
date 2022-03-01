import json
from itertools import combinations_with_replacement

import empowermentexploration.utils.data_handle as data_handle
import pandas as pd


class Tables():
    """Class functions generate Little Alchemy tables.
    """
    def __init__(self):
        """Initializes table class.
        """
        
    def get_tables(self, table_type='combination', version='alchemy2', expand=False):
        """Returns table depending on the type. Can either be combination, parent or child table.

        Args:
            table_type (str, optional): 'combination', 'parent' or 'child'. States what kind of table is going to be created. 
                        Defaults to 'combination'.
            version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used. Defaults to 'alchemy2'.
            expand (bool, optional): True if table also includes unsuccessful combinations. False if table only includes
                        successful combinations. Defaults to False.
        """
        if table_type != 'combination' and table_type != 'parent' and table_type != 'child':
            raise ValueError('Undefined Version: "{}". Use "combination", "parent" or "child" instead.'.format(table_type))
        
        if version != 'alchemy1' and version != 'alchemy2' and version != 'joined' and version != 'tinyalchemy' and version != 'tinypixels':
            raise ValueError('Undefined Version: "{}". Use "alchemy1", "alchemy2", "tinyalchemy", "tinypixels" or "joined" instead.'.format(version))
        
        # print info for user
        print('\nGet table of type {} for version {}.'.format(table_type, version))
        
        # get game tree
        gametree = data_handle.get_gametree(version)

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

    def expand_combination_table(self, table_results, version='alchemy2'):
        """Expands table to include all element combinations, whether successful or not.

        Args:
            table_results (DataFrame): DataFrame consisting of 3 columns: 
                        (1) first (element index)
                        (2) second (element index) 
                        (3) result (element index or NaN)
            version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used. Defaults to 'alchemy2'.

        Returns:
            DataFrame: DataFrame consisting of 4 columns: 
                        (1) first (element index)
                        (2) second (element index) 
                        (3) success (0 or 1)
                        (4) result (element index or NaN)
        """
        # get umber of elements
        if version == 'joined':
            n_elements = 747
        elif version == 'alchemy1' or version == 'tinyalchemy' or version == 'tinypixels':
            n_elements = 540
        elif version == 'alchemy2':
            n_elements = 720
            
        # transform first two entries in table to list
        parents_results = table_results[['first', 'second']].values.tolist()

        # get result for each inventory combination
        table_success = list()
        combinations = combinations_with_replacement(range(n_elements),2)
        for c in combinations:
            combination = sorted(c)
            if combination in parents_results:
                table_success.append({'first': combination[0], 'second': combination[1], 'success': 1})
            else:
                table_success.append({'first': combination[0], 'second': combination[1], 'success': 0})
        table_success = pd.DataFrame(table_success)        
        table_expanded = pd.merge(table_results, table_success, how='outer', on=['first', 'second'])
        table_expanded = table_expanded[['first', 'second', 'success', 'result']]
                
        # return expanded table
        return table_expanded 
