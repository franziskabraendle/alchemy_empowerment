import json

import empowermentexploration.utils.data_handle as data_handle


class Gametrees():
    """Class functions generate Little Alchemy game trees.
    """
    def __init__(self):
        """Initializes game tree class.
        """

    def get_alchemy1_gametree(self):
        """Gets game tree of Little Alchemy 1.
        """
        # print info for user
        print('\nGet alchemy1 game tree.')

        # load raw gametree
        with open('empowermentexploration/resources/littlealchemy/data/raw/elements.json', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # initialize element storage for alchemy 1 elements
        elements = set()

        # get all elements from little alchemy 1
        for key, value in old_gametree.items():
            parents = key.split(',')
            results = value
            elements.update(parents, results)
        elements.difference_update({'water', 'fire', 'earth', 'air'})
        elements = ['water', 'fire', 'earth', 'air'] + list(elements)

        # initialize game tree
        gametree = dict()
        for element_id, element in enumerate(elements):
            gametree[element_id] = {'name': element, 'parents': []}

        # fill game tree
        for key, value in old_gametree.items():
            parents = key.split(',')
            parents = sorted([elements.index(parents[0]), elements.index(parents[1])])
            results = value
            for result in results:
                gametree[elements.index(result)]['parents'].append(parents)

        # write edited library to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/alchemy1Gametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/alchemy1Elements.json', 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)

    def get_alchemy2_gametree(self):
        """Gets game tree of Little Alchemy 2.
        """
        # print info for user
        print('\nGet alchemy2 game tree.')

        # load raw game tree
        with open('empowermentexploration/resources/littlealchemy/data/raw/all.json', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # initialize element storage for alchemy 2 elements and myths and monsters elements
        elements = list()
        myths_and_monsters = list()

        # set for hidden elements that won't be included in game tree
        hidden_elements = {'tardis', 'the doctor', 'blaze', 'conflagration', 'inferno', 'terrain', 'ground', 'supervolcano', 'keyboard cat', 'batman'}

        # store little alchemy 2 elements and myths and monsters elements
        for element in old_gametree['elements']:
            if 'dlc' in old_gametree['elements'][element]:
                myths_and_monsters.append(element)
            elif old_gametree['elements'][element]['name'] not in hidden_elements:
                elements.append(old_gametree['elements'][element]['name'])

        # get assignment of old ID to new ID
        id_assignments = dict()
        new_ID = 0
        for old_ID in old_gametree['elements']:
            if 'dlc' not in old_gametree['elements'][old_ID] and old_gametree['elements'][old_ID]['name'] not in hidden_elements:
                id_assignments[old_ID] = new_ID
                new_ID += 1

        # initialize new game tree
        gametree = dict()

        for element in old_gametree['elements']:
            if "dlc" not in old_gametree['elements'][element] and old_gametree['elements'][element]['name'] not in hidden_elements:
                # store element info with new id
                gametree[id_assignments[element]] = old_gametree['elements'][element]

                # get parents that are not part of the myths and monsters pack or hidden elements
                old_parents = old_gametree['elements'][element]['parents']
                parents = list()
                for parent in old_parents:
                    if parent[0] not in myths_and_monsters and parent[1] not in myths_and_monsters and parent[0] not in hidden_elements and parent[1] not in hidden_elements:
                        parents.append(parent)

                # edit parent IDs
                new_parents = list()
                for parent in parents:
                    new_parents.append([id_assignments[parent[0]], id_assignments[parent[1]]])
                gametree[id_assignments[element]]['parents'] = new_parents

                # edit conditions
                if 'condition'in old_gametree['elements'][element] and 'elements' in old_gametree['elements'][element]['condition']:
                    old_condition = old_gametree['elements'][element]['condition']['elements']
                    new_condition = list()
                    for condition_element in old_condition:
                        if condition_element not in myths_and_monsters and condition_element not in hidden_elements:
                            new_condition.append(id_assignments[condition_element])
                    gametree[id_assignments[element]]['condition']['elements'] = new_condition

        # write edited library to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/alchemy2Gametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/alchemy2Elements.json', 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)

    def get_joined_gametree(self):
        """Gets game tree of joined version Little Alchemy 1 + Little Alchemy 2.
        """
        # print info for user
        print('\nGet joined game tree.')

        # load raw game trees
        alchemy1_gametree = data_handle.get_gametree('alchemy1')
        alchemy2_gametree = data_handle.get_gametree('alchemy2')

        # load elements
        alchemy1_elements = data_handle.get_elements('alchemy1')
        alchemy2_elements = data_handle.get_elements('alchemy2')

        # initialize element storage for joined elements
        elements = set()
        elements.update(alchemy1_elements, alchemy2_elements)
        elements.difference_update({'water', 'fire', 'earth', 'air'})
        elements = ['water', 'fire', 'earth', 'air'] + list(elements)

        # initialize game tree
        gametree = dict()
        for element_id, element in enumerate(elements):
            gametree[element_id] = {'name': element, 'parents': []}

        for element in alchemy1_gametree:
            # get parents
            alchemy1_parents = alchemy1_gametree[element]['parents']
            parents = list()
            for parent in alchemy1_parents:
                parents.append(sorted([elements.index(alchemy1_elements[parent[0]]), elements.index(alchemy1_elements[parent[1]])]))
            if parents:
                gametree[elements.index(alchemy1_elements[element])]['parents'].extend(parents)

        for element in alchemy2_gametree:
            # get parents
            alchemy2_parents = alchemy2_gametree[element]['parents']
            parents = list()
            for parent in alchemy2_parents:
                parents.append(sorted([elements.index(alchemy2_elements[parent[0]]), elements.index(alchemy2_elements[parent[1]])]))
            if parents:
                gametree[elements.index(alchemy2_elements[element])]['parents'].extend(parents)

            # edit conditions
            if 'condition' in alchemy2_gametree[element]:
                if 'elements' in alchemy2_gametree[element]['condition']:
                    old_condition = alchemy2_gametree[element]['condition']['elements']
                    new_condition = list()
                    for condition_element in old_condition:
                        new_condition.append(elements.index(alchemy2_elements[condition_element]))
                    gametree[elements.index(alchemy2_elements[element])]['condition'] = {}
                    gametree[elements.index(alchemy2_elements[element])]['condition']['elements'] = new_condition
                else:
                    gametree[elements.index(alchemy2_elements[element])]['condition'] = alchemy2_gametree[element]['condition']


        # write edited library to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/joinedGametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/joinedElements.json', 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)


    def get_tiny_gametree(self, version='alchemy'):
        """Gets game tree of Little Alchemy 1.

        Args:
            version (str, optional): Defines version more precisely. Can either be 'alchemy' or 'pixels' Defaults to 'alchemy'.
        """
        # print info for user
        print('\nGet tiny{} game tree.'.format(version))

        # load raw gametree
        with open('empowermentexploration/resources/littlealchemy/data/raw/rawTinyGametree.json', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # load elements
        with open('empowermentexploration/resources/littlealchemy/data/raw/tiny{}Elements.json'.format(version), encoding='utf8') as infile:
            elements = json.load(infile)

        # initialize game tree
        gametree = dict()
        for element_id, element in enumerate(elements):
            gametree[element_id] = {'name': element, 'parents': []}

        # initialize memory storing previous combinations
        memory = list()

        # fill game tree
        for element_combinations in old_gametree:
            for combination in element_combinations[1]:
                # when combinations yield more than one element, keep only the first
                if sorted(combination) not in memory:
                    gametree[element_combinations[0]]['parents'].append(sorted(combination))
                    memory.append(sorted(combination))

        # write edited library to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/tiny{}Gametree.json'.format(version), 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/tiny{}Elements.json'.format(version), 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)
