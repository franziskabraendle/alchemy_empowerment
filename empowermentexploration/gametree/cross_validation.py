import random

import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import empowermentexploration.utils.info_logs as log
import pandas as pd
from empowermentexploration.gametree.element_prediction_model import \
    ElementPredictionModel
from empowermentexploration.gametree.link_prediction_model import \
    LinkPredictionModel
from empowermentexploration.gametree.empowerment_prediction_model import \
    EmpowermentPredictionModel
from empowermentexploration.gametree.prepared_dataset import PreparedDataset
from sklearn.model_selection import KFold


class CrossValidation():
    def __init__(self, k, time, game_version='alchemy2',
                 prediction_model=0, epochs=1, batch_size=32, steps_per_epoch=None,
                 exclude_elements_test=True, exclude_elements_val=True, manual_validation=None,
                 oversampling=None, custom_class_weight=None,
                 vector_version='crawl', dim=300):
        """Initialize k-fold cross validation.

        Args:
            k (int): Number of splits (= k).
            time (str): Timestamp. This will be used for logs.
            game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'.
                        States what element and combination set is going to be used.
                        Defaults to 'alchemy2'.
            prediction_model (float, optional): States for what model the data is generate,
                        0 = link prediction model, 1 = element prediction model, 2 = empowerment prediction model.
                        Defaults to 0.
            epochs (int, optional): Number of epochs to train the model. An epoch is an iteration over the entire data provided.
                        Defaults to 1.
            batch_size (int, optional): Number of samples per gradient update. Defaults to 32.
            steps_per_epoch (int, optional): Total number of steps (batches of samples) before declaring one epoch finished
                        and starting the next epoch. Defaults to None.
            exclude_elements_test (bool, optional): States whether elements for the test set should be excluded from the training set
                        or if set splits are created randomly. Defaults to True.
            exclude_elements_val (bool, optional): States whether elements for the validation set should be excluded from the training set
                        or if set splits are created randomly. Overwrites manual_validation if True. Defaults to True.
            manual_validation (float, optional): Fraction of validation split.
                        Defaults to None which means the validation split is done automatically by the model with a 0.2:0.8 ratio (val: train).
                        Is overwritten by exclude_elements_val.
            oversampling (float, optional): Desired fraction to what an underrepresented class is to by oversampled.
                        Is only applied, if prediction_model is 0 (link prediction).
                        Defaults to None which means initial bias and class weights is applied instead of oversampling.
            custom_class_weight (dict, optional): Custom class weights where weights are mapped to each class in a dictionary.
                        If custom class weights are given, they will overwrite any automatically computed class weights.
                        Can be used together with oversampling. Defaults to None.
            vector_version (str, optional): 'ccen', 'crawl' or 'wiki'.
                        States what element vectors the empowerment info should be based on. Defaults to 'crawl'.
            dim (int, optional): Vector dimension e.g. 100 or 300. Defaults to 300.
        """
        # set info on cross validation
        self.k = k

        # set vector info
        self.vector_version = '{}{}'.format(vector_version, dim)

        # set general info
        self.time = time
        self.round = 1

        # set info on game version
        self.game_version = game_version
        if game_version == 'joined':
            self.n_elements = 738
        elif game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
            self.n_elements = 540
        elif game_version == 'alchemy2':
            self.n_elements = 720

        # set info on model
        self.prediction_model = prediction_model
        self.epochs = epochs
        self.batch_size = batch_size
        self.steps_per_epoch = steps_per_epoch

        # set info for data generation
        self.exclude_elements_test = exclude_elements_test
        self.exclude_elements_val = exclude_elements_val
        if self.exclude_elements_test is True or exclude_elements_val is True:
            self.split_version = 'element'
        else:
            self.split_version = 'data'
        self.manual_validation = manual_validation
        self.oversampling = oversampling
        self.custom_class_weight = custom_class_weight

    def run_cross_validation(self):
        """Run cross validation.
        """
        # print info for user
        print('\nRun cross validation.')

        # create file for predicted probabilities
        log.create_gametreetable_file(time=self.time, prediction_model=self.prediction_model, n_elements=self.n_elements,
                                      game_version=self.game_version, split_version=self.split_version, vector_version=self.vector_version)

        # load and shuffle dataset
        data_table = data_handle.get_combination_table(self.game_version)
        data_table = data_table.sample(frac=1)

        #if self.prediction_model == 0:
        if self.prediction_model != 1:
            data_table = data_table.drop_duplicates(subset=['first', 'second'])

        # initialize storage for results
        result_metrics = list()

        if self.exclude_elements_test is True:
            # make a k-fold cross-validation that has distinct element groups for each set
            element_groups = helpers.split_numbers(self.n_elements, self.k)

            for idx, test_group in enumerate(element_groups):
                # print info for user
                print('\nRound {} of {}.'.format(self.round, self.k))

                # get data
                if self.exclude_elements_val is True:
                    # choose a random group of elements to make up the validation set
                    val_group = element_groups[random.choice([group for group in range(len(element_groups)) if group != idx])]

                    data = PreparedDataset(data_table, game_version=self.game_version, prediction_model=self.prediction_model,
                                           exclusion_elements=(test_group,val_group),
                                           oversampling=self.oversampling, custom_class_weight=self.custom_class_weight,
                                           vector_version=self.vector_version)
                else:
                    data = PreparedDataset(data_table, game_version=self.game_version, prediction_model=self.prediction_model,
                                           exclusion_elements=(test_group,), manual_validation=self.manual_validation,
                                           oversampling=self.oversampling, custom_class_weight=self.custom_class_weight,
                                           vector_version=self.vector_version)

                # run models and update result storage
                test_metrics = self.run_cross_validation_round(data)
                result_metrics.append(test_metrics)
        else:
            # make a random k-fold cross-validation
            kf = KFold(n_splits=self.k)

            for train_index, test_index in kf.split(data_table):
                # get data
                data = PreparedDataset((data_table.iloc[train_index], data_table.iloc[test_index]), game_version=self.game_version, prediction_model=self.prediction_model,
                                       manual_validation=self.manual_validation,
                                       oversampling=self.oversampling, custom_class_weight=self.custom_class_weight,
                                       vector_version=self.vector_version)

                # run models and update result storage
                test_metrics = self.run_cross_validation_round(data)
                result_metrics.append(test_metrics)

        # save performance
        results = pd.DataFrame(result_metrics)
        if self.prediction_model == 0:
            results.to_csv('empowermentexploration/data/gametree/{}/{}LinkPred-metrics.csv'.format(self.time, self.game_version), index=False)
        elif self.prediction_model == 1:
            results.to_csv('empowermentexploration/data/gametree/{}/{}ElemPred-metrics.csv'.format(self.time, self.game_version), index=False)
        else:
            results.to_csv('empowermentexploration/data/gametree/{}/{}EmpPred-metrics.csv'.format(self.time, self.game_version), index=False)

    def run_cross_validation_round(self, data):
        """Runs one cross validation round with given data.

        Args:
            data (PreparedDataset): Prepared dataset which is fed in into the model.

        Returns:
            dict: Test metrics.
        """
        # evaluate model
        if self.prediction_model == 0:
            model = LinkPredictionModel(self.time, self.round, self.epochs, self.batch_size, self.steps_per_epoch, data.class_weight, data.output_bias, self.game_version)
            if self.manual_validation is not None or self.exclude_elements_val is True:
                predictions, test_metrics = model.evaluate_model((data.X_train, data.X_test, data.X_val), (data.y_train, data.y_test, data.y_val))
            else:
                predictions, test_metrics = model.evaluate_model((data.X_train, data.X_test), (data.y_train, data.y_test), validation_split=0.2)
        elif self.prediction_model == 1:
            model = ElementPredictionModel(self.time, self.round, self.epochs, self.batch_size, self.steps_per_epoch, self.game_version, self.vector_version)
            if self.manual_validation is not None or self.exclude_elements_val is True:
                predictions, test_metrics = model.evaluate_model((data.X_train, data.X_test, data.X_val),
                                                                 (data.y_train, data.y_test, data.y_val), (data.idx_train, data.idx_test))
            else:
                predictions, test_metrics = model.evaluate_model((data.X_train, data.X_test),
                                                                 (data.y_train, data.y_test), (data.idx_train, data.idx_test), validation_split=0.2)
        else:
            model = EmpowermentPredictionModel(self.time, self.round, self.epochs, self.batch_size, self.steps_per_epoch, self.game_version) # data.output_bias
            if self.manual_validation is not None or self.exclude_elements_val is True:
                predictions, test_metrics = model.evaluate_model((data.X_train, data.X_test, data.X_val), (data.y_train, data.y_test, data.y_val))
            else:
                predictions, test_metrics = model.evaluate_model((data.X_train, data.X_test), (data.y_train, data.y_test), validation_split=0.2)

        # write to file
        log.append_gametreetable_file(data.idx_test, predictions, time=self.time, prediction_model=self.prediction_model,
                                      game_version=self.game_version, split_version=self.split_version, vector_version=self.vector_version)

        # increment round
        self.round += 1

        return test_metrics
