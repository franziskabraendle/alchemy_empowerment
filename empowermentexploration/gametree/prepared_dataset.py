import empowermentexploration.utils.data_handle as data_handle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


class PreparedDataset():
    """Dataset containing train, test and (if wanted) validation and prediction set.
    """
    def __init__(self, data, game_version='alchemy2', prediction_model=0, exclusion_elements=None, manual_validation=None,
                 oversampling=None, custom_class_weight=None, vector_version='crawl300'):
        """Initializes prepared datasets that will be input to an element or link prediction model.

        Args:
            data (tuple): Can either be a single DataFrame (total data) or a tuple consisting of two DataFrames (separate train and test data).
                        DataFrames contain information about elements involved in combination (columns 'first' and 'second', element indices)
                        and its success and resulting element (column 'success', is either 1 or 0 and column 'result', element index or NaN).
            game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinypixels' or 'tinyalchemy'.
                        States what element and combination set is going to be used.
                        Defaults to 'alchemy2'.
            prediction_model (float, optional): States for what model the data is generated,
                        0 = link prediction model, 1 = element prediction model, 2 empowerment prediction model.
                        Defaults to 0.
            exclusion_elements (tuple, optional): Contains one or two arrays of elements that are each to be excluded from the training set.
                        They will make up combinations from the test set respectively validation set.
                        Defaults to None.
            manual_validation (float, optional): Fraction of training set that will make up the validation set.
                        Defaults to None, in which case the split is done automatically within the model.
                        exclusion_elements overwrites manual_validation if the tuple contains two entries.
            oversampling (float, optional): Desired fraction to what an underrepresented class is to by oversampled.
                        E.g. 1.0 = ratio will be 1:1, 0.5 = ratio will be 1:2
                        Is only applied, if prediction_model = 0 (link prediction).
                        Defaults to None which means initial bias and class weights is applied instead of oversampling.
            custom_class_weight (dictionary, optional): Custom class weights where weights are mapped to each class in a dictionary.
                        If custom class weights are given, they will overwrite any automatically computed class weights.
                        Can be used together with oversampling. Defaults to None.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                        States what element vectors the empowerment info should be based on.
                        Defaults to 'crawl300'.
        """
        # print info for user
        print('\nGet data set.')

        # set general attributes
        self.game_version = game_version
        if game_version == 'joined':
            self.n_elements = 738
        elif game_version == 'alchemy1' or game_version == 'tinyalchemy' or game_version == 'tinypixels':
            self.n_elements = 540
        elif game_version == 'alchemy2':
            self.n_elements = 720
        self.vector_version = vector_version
        self.prediction_model = prediction_model
        self.exclusion_elements = exclusion_elements
        self.manual_validation = manual_validation

        # split into train, test and validation set
        train_data, test_data, val_data = self.split_train_val_test_sets(data)

        if self.prediction_model == 0:
            # analyze imbalance
            self.output_bias, self.class_weight  = self.analyze_imbalance(train_data, test_data, val_data)
            if custom_class_weight is not None:
                self.class_weight = custom_class_weight

            # apply oversampling
            self.oversampling = oversampling
            if self.oversampling is not None:
                self.output_bias, self.class_weight = None, None
                if custom_class_weight is not None:
                    self.class_weight = custom_class_weight
                train_data = self.apply_oversampling(train_data)

        # transform data into vectors
        self.X_train, self.y_train, self.idx_train = self.get_feature_and_label_vector(train_data, type=0)
        self.X_test, self.y_test, self.idx_test = self.get_feature_and_label_vector(test_data, type=1)
        if val_data is not None:
            self.X_val, self.y_val, self.idx_val = self.get_feature_and_label_vector(val_data, type=2)

        # normalize
        self.normalize()

    def split_train_val_test_sets(self, data): #TODOOOOOO
        """Returns train, test and validation sets.

        Args:
            data (tuple): Can either be a single DataFrame (total data) or a tuple consisting of two DataFrames (separate train and test data).
                        DataFrames contain information about elements involved in combination (columns 'first' and 'second', element indices)
                        and its success and resulting element (column 'success', is either 1 or 0 and column 'result', element index or NaN).

        Returns:
            tuple:
                - train_table (DataFrame): Contains train data.
                - test_table (DataFrame): Contains test data.
                - val_table (DataFrame): Contains validation data. Defaults to None if self.manual_validation is None
        """
        # initialize val_table
        val_table = None

        if self.exclusion_elements is None:
            # extract info from argument
            train_table = data[0]
            test_table = data[1]

            # get total size of data entries
            n_data = len(train_table.index) + len(test_table.index)

            # split train set further into test and validation set depending on manual_validation
            if self.manual_validation is not None:
                split = np.split(train_table.sample(frac=1), [int(self.manual_validation*len(train_table.index))])
                val_table = split[0]
                train_table = split[1]
        else:
            # print info
            print('\nExclude from test set: {}'.format(self.exclusion_elements[0]))

            # extract info from argument
            table = data

            # get total size of data entries
            n_data = len(table.index)

            # split into train and test sets
            first_exclusion_test = table.eval('first in @self.exclusion_elements[0]')
            second_exclusion_test = table.eval('second in @self.exclusion_elements[0]')
            if self.prediction_model != 1:
                test_condition = (first_exclusion_test | second_exclusion_test)
            else:
                result_exclusion_test = table.eval('result in @self.exclusion_elements[0]')
                test_condition = (first_exclusion_test | second_exclusion_test | result_exclusion_test)
            train_table = table.loc[~test_condition]
            test_table = table.loc[test_condition]

            # split train set further into test and validation set
            if len(self.exclusion_elements) == 2:
                # print info
                print('\nExclude from validation set: {}'.format(self.exclusion_elements[1]))

                first_exclusion_val = table.eval('first in @self.exclusion_elements[1]')
                second_exclusion_val = table.eval('second in @self.exclusion_elements[1]')
                if self.prediction_model != 1:
                    val_condition = (first_exclusion_val | second_exclusion_val)
                else:
                    result_exclusion_val = table.eval('result in @self.exclusion_elements[1]')
                    val_condition = (first_exclusion_val | second_exclusion_val | result_exclusion_val)
                val_table = train_table.loc[val_condition]
                train_table = train_table.loc[~val_condition]
            elif self.manual_validation is not None:
                split = np.split(train_table.sample(frac=1), [int(self.manual_validation*len(train_table.index))])
                val_table = split[0]
                train_table = split[1]

        # print info
        print('\nTrain set: {:.2f}%'.format(100 * len(train_table.index)/ n_data))
        print('\nTest set: {:.2f}%'.format(100 * len(test_table.index)/ n_data))
        if val_table is not None:
            print('\nValidation set: {:.2f}%'.format(100 * len(val_table.index)/ n_data))

        # return data sets
        return train_table, test_table, val_table

    def analyze_imbalance(self, *tables):
        """Analyzes class values and returns initial bias and class weights.

        Args;
            tables (Dataframe): Contains information about elements involved in combination (columns 'first' and 'second', element indices)
                        and its success and resulting element (column 'success', is either 1 or 0 and column 'result', element index or NaN).
                        Classes might be imbalanced.
        Returns:
            tuple:
                - initial_bias (float): Initial bias to get better initial convergence.
                - class_weights (dictionary): Maps class indices (integers) to a weight (float) value,
                        used for weighting the loss function (during training only).
                        This can be useful to tell the model to "pay more attention" to samples from an under-represented class.
        """
        # print info
        print('\nAnalyze imbalance:')

        class_values = list()
        for table in tables:
            if table is not None:
                class_values += table['success'].values.tolist()

        # get counts for each class and total
        class_zero, class_one = np.bincount(class_values)
        total = class_zero + class_one
        print('\t- Class 0: {:.2f}%\n\t- Class 1: {:.2f}%'.format(100 * class_zero / total, 100 * class_one / total))

        # get initial bias
        initial_bias = np.log([class_one/class_zero])

        # get class weights
        weight_for_zero = (1 / class_zero)*(total)/2.0
        weight_for_one = (1 / class_one)*(total)/2.0
        class_weight = {0: weight_for_zero, 1: weight_for_one}

        return initial_bias, class_weight

    def apply_oversampling(self, table):
        """Applies oversampling on data.

        Args:
            table (DataFrame): Contains information about elements involved in combination (columns 'first' and 'second', element indices)
                        and its success and resulting element (column 'success', is either 1 or 0 and column 'result', element index or NaN).
                        Classes might be imbalanced.

        Returns:
            (DataFrame): Contains information about elements involved in combination (columns 'first' and 'second', element indices)
                        and its success and resulting element (column 'success', is either 1 or 0 and column 'result', element index or NaN).
                        Classes are balanced according to ratio set in self.oversampling.
        """
        # print info
        print('\nApply oversampling.')

        # extract tables for success or no success
        success_condition = table.eval('success == 1')
        class_one_table = table.loc[success_condition].values
        class_zero_table= table.loc[~success_condition].values

        # oversample: balance out both classes by randomly resampling success group
        ids = np.arange(class_one_table.shape[0])
        choices = np.random.choice(ids, int(class_zero_table.shape[0]*self.oversampling))
        class_one_table_oversampled = class_one_table[choices]

        # join both tables
        table = np.concatenate([class_one_table_oversampled, class_zero_table], axis=0)
        table = pd.DataFrame({'first': table[:, 0], 'second': table[:, 1], 'success': table[:,2], 'result': table[:,3]})

        # return shuffled joined table with balanced classes
        return table.sample(frac=1)

    def normalize(self):
        """Normalizes input vectors.
        """
        # print info for user
        print('\nNormalize data.')

        # normalize
        scaler = StandardScaler()
        self.X_train = scaler.fit_transform(self.X_train)
        self.X_test = scaler.transform(self.X_test)
        if hasattr(self, 'X_val'):
            self.X_val = scaler.transform(self.X_val)

    def get_feature_and_label_vector(self, data, type=0):
        """Returns feature and corresponding label vectors. Feature vectors are made up of concatenated word vectors, labels are either 0 or 1.

        Args:
            data (DataFrame): Contains information about elements involved in combination (columns 'first' and 'second', element indices)
                        and its success and resulting element (column 'success', is either 1 or 0 and column 'result', element index or NaN).
            type (int, optional): Type of set that is made. 0 for train, 1 for test, 2 for val. Only of interest for element prediction model.
                        Defaults to 0.
        Returns:
            tuple:
                - feature_vectors (ndarray(dtype=float, ndim=2)): Inputs.
                - label_vector (ndarray(dtype=int, ndim=1)): Outputs.
                - feature_indices (ndarray(dtype=int, ndim=2)): Combination element indices.
        """
        # print info for user
        print('\nGet feature and label vectors.')

        self.parent_table = data_handle.get_parent_table(self.game_version)
        self.combination_table = data_handle.get_combination_table(self.game_version, csv=False)

        # get list of element vectors
        element_vectors = data_handle.get_wordvectors(self.game_version, self.vector_version)

        # for element prediction model, empowerment prediction model and train and val data: reduce data to only successful data
        if self.prediction_model != 0 and (type == 0 or type == 2):
            data.query('success == 1', inplace=True)
        data = data.values

        # initialize feature vector storage
        combination_count = data.shape[0]
        vector_dim = element_vectors.shape[1]
        feature_vectors = np.empty((2*combination_count,2*vector_dim))

        # initialize label vector storage
        if self.prediction_model != 1:
            label_vector = np.empty(2*combination_count)
        else:
            label_vector = np.empty((2*combination_count, vector_dim))

        # initialize element index storage
        indices = np.empty((2*combination_count,4))

        # create combination features and get corresponding result vectors
        for idx, combination in enumerate(data):
            combination_success = [int(x) for x in combination[:3]]
            result = combination[3]
            feature_vectors[idx,:] = np.concatenate([element_vectors[combination_success[0]], element_vectors[combination_success[1]]], axis = 0)
            feature_vectors[idx+combination_count,:] = np.concatenate([element_vectors[combination_success[1]], element_vectors[combination_success[0]]], axis = 0)

            if self.prediction_model == 0:
                label_vector[idx] = combination_success[2]
                label_vector[idx+combination_count] = combination_success[2]
            elif self.prediction_model ==2:
                #empvalue of result

                if combination[0] in self.combination_table and combination[1] in self.combination_table[combination[0]]:
                    result_elements = self.combination_table[combination[0]][combination[1]]
                else:
                    result_elements = list()

                # initialize empowerment depending on how it is calculated
                empowerment = set()

                # calculate empowerment value iteratively for each result
                for r in result_elements:
                    if r in self.parent_table:
                        empowerment.update(self.parent_table[r])

                label_vector[idx] = len(empowerment)
                label_vector[idx+combination_count] = len(empowerment)
            else:
                if not np.isnan(result):
                    label_vector[idx,:] = element_vectors[int(result)]
                    label_vector[idx+combination_count,:] = element_vectors[int(result)]

            indices[idx,:] = combination
            indices[idx+combination_count,:] = combination

        print('\t\t... shape input vectors:', feature_vectors.shape)
        print('\t\t... shape label vector:', label_vector.shape)

        # return feature vectors and corresponding label and index vectors
        return feature_vectors, label_vector, indices
