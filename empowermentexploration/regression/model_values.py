import json
import random

import empowermentexploration.utils.info_logs as log
import pandas as pd
from empowermentexploration.regression.bin_model import BinModel
from empowermentexploration.regression.cbu_model import CBUModel
from empowermentexploration.regression.recency_model import RecencyModel
from empowermentexploration.regression.cbv_model import CBVModel
from empowermentexploration.regression.emp_model import EmpModel
from empowermentexploration.regression.inventory import Inventory
from empowermentexploration.regression.sim_model import SimModel
from empowermentexploration.regression.truebin_model import TrueBinModel
from empowermentexploration.regression.trueemp_model import TrueEmpModel
from empowermentexploration.regression.empdirect_model import EmpdirectModel
import empowermentexploration.utils.data_handle as data_handle
from scipy.stats import zscore


class ModelValues():
    """Little Alchemy player data.
    """
    def __init__(self, player_data, time, game_version, split_version, vector_version, model_type, memory_type, matched, emp_version, z_score=True):
        """Initializes dataframe consisting of model values for each person and trial.

        Args:
            player_data (DataFrame): Dataframe containing game info for each player.
            time (str): Timestamp. This will be used for logs.
            game_version (str): 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                        States what player data set set is going to be used.
            split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.
            model_type (str): Model type, which is either 'human' or any selection from 'base', 'emp', 'bin', 'trueemp',
                        'truebin', 'cbv', 'sim' or 'cbu' if data is generated for simulated data.
            memory_type (int): Memory type that was used for data generation. There are different options
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 10 steps)
            z_score (boolean, optional): True if z score for model differences should be caculated, False otherwise. Defaults to True.
        """
        # convert dataframe to numpy array with (1) id, (2) trial, (3) inventory, (4) first, (5) second, (6) success, (7) results
        player_data = player_data.to_numpy()

        # initialize new list holding information on (1) player id, (2) trial, (3) first, (4) second, (5) decision between two arms, (6)-(11) differences for values of model strategies
        self.data = list()
        self.combination_table = data_handle.get_combination_table(game_version, csv=False)
        # initialize inventory
        inventory = Inventory(game_version)
        inventory.reset()

        # initialize model specific info
        cbv_model = CBVModel(game_version)
        cbv_model.reset()
        cbu_model = CBUModel(game_version) #normal cbu model.
        cbu_model.reset()
        rec_model = RecencyModel(game_version)
        rec_model.reset()
        sim_model = SimModel(game_version)
        bin_model = BinModel(game_version, split_version, vector_version)
        if emp_version == "elements":
            emp_model = EmpModel(game_version, split_version, vector_version) #need to decide if element or direct empowerment model (values) is used. Dependent on the gametreefile (need to be changed if other model should be used).
        elif emp_version == "values":
            emp_model = EmpdirectModel(game_version, split_version, vector_version)
        else:
            raise ValueError('Undefined version: "{}". Use "values" or "elements" instead.'.format(emp_version))


        truebin_model = TrueBinModel(game_version)
        trueemp_model = TrueEmpModel(game_version)

        # get initial player id
        player_id = player_data[0][0]

        # iterate through every combination trial
        for trial in player_data:
            # initialize inventory for each new player
            if trial[0] != player_id:
                player_id = trial[0]
                inventory.reset()
                cbv_model.reset()
                cbu_model.reset()
                rec_model.reset()
                print(player_id)

            # initialize dictionary to store info on combination trial
            trial_data = {'id': player_id, 'trial': trial[1], 'inventory': trial[2]}

            # get chosen and random combination
            # TODO: random combination can be adjusted to expected value
            chosen_combination = sorted([trial[3], trial[4]])
            trial_data.update({'first': chosen_combination[0], 'second': chosen_combination[1]})




            #New version with matching of the combination success:
            if matched == True:
                if chosen_combination[0] in self.combination_table and chosen_combination[1] in self.combination_table[chosen_combination[0]]:
                    #random_combination = sorted([random.choice(list(inventory.inventory_successfull)), random.choice(list(inventory.inventory_successfull))])
                    random_combination = sorted([random.choice(inventory.inventory_successfull)])
                else:
                    random_combination = sorted([random.choice(inventory.inventory_not_successfull)])
                random_combination = sorted(random_combination[0])
            else:
                #Old version without matching of the combination success:
                if game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
                    random_combination = sorted([random.choice(list(inventory.inventory_total)), random.choice(list(inventory.inventory_total))])
                else:
                    random_combination = sorted([random.choice(list(inventory.inventory_used)), random.choice(list(inventory.inventory_used))])


            # set decision which corresponds to assigning combination to options x_i and x_j
            decision = random.randint(0,1)
            trial_data.update({'decision': decision})

            # set models that are to be looked at
            models = [('cbv', cbv_model), ('cbu', cbu_model), ('rec', rec_model), ('sim', sim_model), ('bin', bin_model), ('emp', emp_model), ('truebin', truebin_model), ('trueemp', trueemp_model)]


            # iterate through different models
            for model in models:
                # get model value for chosen and random combination

                value_chosen_combination = model[1].get_value(chosen_combination)
                value_random_combination = model[1].get_value(random_combination)

                # compute difference depending on decision
                if decision == 1:
                    delta = value_chosen_combination - value_random_combination
                else:
                    delta = value_random_combination - value_chosen_combination

                # update dictionary
                trial_data.update({'delta_{}'.format(model[0]): delta})

            self.data.append(trial_data)

            # extract results of chosen combination
            try:
                results_chosen_combination = json.loads(trial[6])
            except:
                results_chosen_combination = list()

            # update inventory and cbv model
            results = inventory.update(chosen_combination, results_chosen_combination)
            if matched == True:
                inventory.update_success_list()
            cbv_model.update_model_specifics(chosen_combination, results)
            cbu_model.update_model_specifics(chosen_combination, results)
            rec_model.update_model_specifics(chosen_combination, results)



        # convert to dataframe
        self.data = pd.DataFrame(self.data)

        # compute z-scores for differences
        if z_score is True:
            for model in models:
                self.data['delta_{}'.format(model[0])] = zscore(self.data['delta_{}'.format(model[0])])

        # store as csv file
        log.store_regression_data(self.data, time, z_score, model_type, memory_type, game_version)
