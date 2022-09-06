import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.info_logs as log
from empowermentexploration.models.base_model import BaseModel
from empowermentexploration.models.bin_model import BinModel
from empowermentexploration.models.cbu_model import CBUModel
from empowermentexploration.models.cbv_model import CBVModel
from empowermentexploration.models.emp_model import EmpModel
from empowermentexploration.models.inventory import Inventory
from empowermentexploration.models.sim_model import SimModel
from empowermentexploration.models.truebin_model import TrueBinModel
from empowermentexploration.models.trueemp_model import TrueEmpModel
from empowermentexploration.models.visualization import Visualization

class LittleAlchemyModel():
    """Model that plays the game Little Alchemy 2.
    """
    def __init__(self, time, game_version='alchemy2', runs=100, steps=1000, temperatures=[1.0], memory_type=0,
                 models=None, value_calculation=None,
                 vector_version='crawl300', split_version='data'):
        """Initializes a little alchemy 2 model.

        Args:
            time (str): Timestamp. This will be used for logs.
            game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinypixels' or 'tinyalchemy'. States what element and combination set is going to be used.
                        Defaults to 'alchemy2'.
            runs (int, optional): Number of simulations. Defaults to 100.
            steps (int, optional): Number of steps for each simulation. Defaults to 1000.
            temperatures (list): List of temperatures (float) that are used to compute probabilities.
                        There will be one complete run for each temperature. Defaults to [1.0].
            memory_type (int, optional): States whether it should be memorized what combinations have been used before.
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)
                        Defaults to 0.
            models (list, optional): List of models that are to be run. Defaults to None.
            value_calculation (tuple, optional): Tuple of value calculation Tuple contains first calculation info on trueemp, then emp, then truebin and bin.
                        Defaults to None.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                        States what element vectors the empowerment info should be based on.
                        Defaults to 'crawl300'.
            split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on.
                        Defaults to 'data'.
        """
        # print info for user
        print('\nInitialize little alchemy model based on gametree {}.'.format(game_version))

        # set general info
        self.time = time
        self.game_version = game_version
        self.runs = runs
        self.steps = steps
        self.temperatures = temperatures
        self.memory_type = memory_type
        self.models = models
        self.value_calculation = value_calculation
        self.vector_version = vector_version
        self.split_version = split_version

        # load info table
        self.combination_table = data_handle.get_combination_table(game_version, csv=False)

    def simulate_game(self, model_type, empowerment_calculation=(True,True,False)):
        """Simulates game.

        Args:
            model_type (str): model_version (str, optional): States what kind of model is going to be used.
                        (1) 'base' = baseline model
                        (2) 'cbv' = count-based value model
                        (3) 'cbu' = count-based uncertainty model
                        (4) 'sim' = similarity model
                        (5) 'bin' = binary model based on the self-constructed game tree
                        (6) 'emp' = empowerment model based on the self-constructed game tree
                        (7) 'truebin' = binary model based on the true game tree
                        (8) 'trueemp' = empowerment model based on the true game tree
            empowerment_calculation (tuple, optional): Tuple made of three entries. Defaults to (True,True,False).
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                    or length of set of resulting elements.
        """
        # print info for user
        print('\nStart game for using model {} on gametree {}, memory={}.'.format(model_type, self.game_version, self.memory_type))

        # initialize model specific info
        model = self.initialize_model(model_type, empowerment_calculation)

        if model_type == 'base':
            print('\nRun simulations.')

            # initialize visualization
            visualization = Visualization(self.game_version, self.time, model_type, [1.0], self.runs, self.steps, self.memory_type)

            # initialize inventory
            inventory = Inventory(self.game_version, 1, self.runs, self.steps)

            for run in range(self.runs):
                # reset inventories: one only holds usable elements and no final elements, the other one tracks all elements
                inventory.reset()

                # reset model specific info
                model.reset()

                for step in range(self.steps):
                    combination = model.choose_combination(inventory, step)
                    inventory.update(combination, 0, run, step)

            # visualization of inventory sizes
            visualization.plot_inventory_sizes(inventory, 0)
        else:
            # initialize visualization
            visualization = Visualization(self.game_version, self.time, model_type, self.temperatures, self.runs, self.steps, self.memory_type, empowerment_calculation)

            # initialize inventory
            inventory = Inventory(self.game_version, len(self.temperatures), self.runs, self.steps)

            for temperature_idx, temperature_value in enumerate(self.temperatures):
                print('\nRun {} simulations for temperature value {}.'.format(self.runs, temperature_value))

                for run in range(self.runs):

                    # reset inventories: one only holds usable elements and no final elements, the other one tracks all elements
                    inventory.reset()

                    # reset model specific info
                    model.reset()

                    for step in range(self.steps):
                        combination = model.choose_combination(temperature_value, (step==0 or self.memory_type == 1 or self.memory_type == 2 or len(results[0]) != 0))
                        results = inventory.update(combination, temperature_idx, run, step)
                        model.update_model_specifics(combination, results, inventory, step)

                # visualization of inventory sizes
                visualization.plot_inventory_sizes(inventory, temperature_idx)

        # visualization of training progress
        visualization.plot_gameprogress(inventory)

        # store inventory data
        log.store_inventory(self.game_version, inventory, self.time, model_type, self.memory_type, empowerment_calculation)

    def initialize_model(self, model_type, empowerment_calculation):
        """Return model instance depending on what version is requested.

        Args:
            model_version (str, optional): States what kind of model is going to be used.
                        (1) 'base' = baseline model
                        (2) 'cbv' = count-based value model
                        (3) 'cbu' = count-based uncertainty model
                        (4) 'sim' = similarity model
                        (5) 'bin' = binary model based on the self-constructed game tree
                        (6) 'emp' = empowerment model based on the self-constructed game tree
                        (7) 'truebin' = binary model based on the true game tree
                        (8) 'trueemp' = empowerment model based on the true game tree
            empowerment_calculation (tuple): Tuple made of three entries.
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                    or length of set of resulting elements.

        Returns:
            Model: Model instance depending on what version is requested.
        """
        if model_type == 'base':
            return BaseModel(self.memory_type)
        elif model_type == 'bin':
            return BinModel(self.game_version, self.memory_type, empowerment_calculation, self.vector_version, self.split_version)
        elif model_type == 'emp':
            return EmpModel(self.game_version, self.memory_type, empowerment_calculation, self.vector_version, self.split_version,)
        elif model_type == 'truebin':
            return TrueBinModel(self.game_version, self.memory_type, empowerment_calculation)
        elif model_type == 'trueemp':
            return TrueEmpModel(self.game_version, self.memory_type, empowerment_calculation)
        elif model_type == 'sim':
            return SimModel(self.game_version, self.memory_type, self.vector_version)
        elif model_type == 'cbv':
            return CBVModel(self.game_version, self.memory_type)
        elif model_type == 'cbu':
            return CBUModel(self.game_version, self.memory_type)

        else:
            raise ValueError('Undefined model version: "{}". Use "base", "cbv",\
                "cbu", "sim", "bin", "emp", "truebin" or "trueemp" instead.'.format(model_type))
