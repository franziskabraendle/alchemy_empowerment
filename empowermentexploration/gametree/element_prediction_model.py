import empowermentexploration.utils.data_handle as data_handle
import empowermentexploration.utils.helpers as helpers
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_docs as tfdocs
import tensorflow_docs.modeling
from empowermentexploration.gametree.visualization import Visualization
from sklearn.metrics.pairwise import cosine_similarity
from tensorflow import keras
from tensorflow.keras import backend, layers


class ElementPredictionModel():
    """Model that predicts probabilities of resulting elements for a combination.
    """
    def __init__(self, time, step, epochs=1, batch_size=32, steps_per_epoch=None, game_version='alchemy2', vector_version='crawl300'):
        """Initializes an element prediction model.

        Args:
            time (str): Time that will be used as folder name for saving pictures.
            step (int): Iteration round.
            epochs (int, optional): Number of epochs to train the model. Defaults to 1.
            batch_size (int, optional): Number of samples per gradient update. Defaults to 32.
            steps_per_epoch (int, optional): Total number of steps (batches of samples) before declaring one epoch finished 
                        and starting the next epoch. Defaults to None.
            game_version (str, optional): 'joined', 'alchemy1', 'alchemy2', 'tinyalchemy' or 'tinypixels'. 
                        States what element and combination set is going to be used. 
                        Defaults to 'alchemy2'.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'. 
                        States what element vectors the empowerment info should be based on. 
                        Defaults to 'crawl300'.
        """
        # print info for user
        print('\nInitialize element prediction model.')
        
        # set attributes
        self.game_version = game_version
        self.time = time
        self.step = step
        self.epochs = epochs
        self.batch_size = batch_size
        self.steps_per_epoch = steps_per_epoch
        
        # get list of element vectors and convert to Tensor objects
        self.element_vectors = data_handle.get_wordvectors(game_version, vector_version)
        self.element_vectors_tensor = tf.convert_to_tensor(self.element_vectors, dtype=tf.float32)
    
    def evaluate_model(self, X, y, idx, validation_split=None):
        """Get, train and evaluate model for predicting probabilities of resulting elements for a combination.

        Args:
            X (tuple): Tuple containing inputs for training (1), testing (2) and validation (3, optional). 
                        Each is an ndarray(dtype=float, ndim=2)).
            y (tuple): Tuple containing outputs for training (1), testing (2) and validation (3, optional). 
                        Each is an ndarray(dtype=float, ndim=2)).
            idx (tuple): Tuple containing combination indices for training (1) and testing (2). 
                        Each is an ndarray(dtype=int, ndim=1)).
            validation_split (float, optional): Fraction of the training data to be used as validation data. 
                        Defaults to None which means validation set is given manually with X and y.
           
        Returns:
            tuple: 
                - pred_probabilities (ndarray(dtype=float, ndim=2)): Predicted probabilities for each element on test data set.
                - test_metrics (dictionary): Metric info on test data (model + ranks).
        """
        # extract train, test and prediction data
        X_train, y_train, idx_train = X[0], y[0], idx[0]
        X_test, y_test, idx_test = X[1], y[1], idx[1]
        
        # get input and output size
        n_inputs, n_outputs = X_train.shape[1], y_train.shape[1]

        # build model
        model = self.build_model(n_inputs, n_outputs)
        model.summary()

        # apply early stopping
        # early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', 
        #                                           verbose=1, mode='min', 
        #                                           patience=15, restore_best_weights=True)

        # print info for user
        print('\nFit element prediction model.')
        
        if validation_split is not None:
            # train model
            history = model.fit(X_train, y_train, 
                                steps_per_epoch=self.steps_per_epoch, 
                                epochs=self.epochs, 
                                batch_size=self.batch_size,
                                validation_split=validation_split,
                                verbose=0, 
                                callbacks=[tfdocs.modeling.EpochDots()]) 
                                #          tf.keras.callbacks.TensorBoard(log_dir='./logs')])
        else:
            X_val, y_val = X[2], y[2]
            
            # train model
            history = model.fit(X_train, y_train, 
                                steps_per_epoch=self.steps_per_epoch, 
                                epochs=self.epochs, 
                                batch_size=self.batch_size,
                                validation_data = (X_val, y_val), 
                                verbose=0, 
                                callbacks=[tfdocs.modeling.EpochDots()]) 
                                #          tf.keras.callbacks.TensorBoard(log_dir='./logs')])
                
        # visualization of training progress
        visualization = Visualization(self.time, '{}ElemPred'.format(self.game_version), self.step)
        visualization.plot_progress(history, ['loss', 'mse', 'mae', 'cosine similarity'])
        
        # make predictions 
        train_predictions = model.predict(X_train)
        test_predictions = model.predict(X_test)
        
        # get probabilities for elements and rank results
        _, train_ranks = self.get_element_probabilities(train_predictions, idx_train)
        probabilities, test_ranks = self.get_element_probabilities(test_predictions, idx_test)

        # visualization of ranks
        test_metrics_ranks = visualization.plot_ranks(train_ranks, test_ranks)
        
        # check generalization on test data
        test_metrics_model = model.evaluate(X_test, y_test, verbose=0, return_dict=True)
        
        # print info for user
        print('\nReturn results from element prediction model.')
        
        # update metrics
        test_metrics_ranks.update(test_metrics_model)    
        
        # return predictions and test metrics
        return probabilities, test_metrics_ranks


    def build_model(self, n_inputs, n_outputs):
        """Creates and returns model for predicting probabilities of resulting elements for a combination.

        Args:
            n_inputs (int): Input size.
            n_outputs (int): Output size.
            
        Returns:
            Sequential: Model.
        """
        # print info for user
        print('\nBuild element prediction model.')
        
        # define architecture
        model = keras.Sequential([
            layers.Dense(1024, activation='relu', input_shape=[n_inputs]),
            layers.Dense(1024, activation='relu'),
            layers.Dense(n_outputs, activation='linear')
        ])

        # define learning rate
        lr = 1e-3

        # define optimizer
        optimizer = tf.keras.optimizers.Adam(lr)

        # define metrics
        metrics = [
            keras.metrics.MeanSquaredError(name='mse'),
            keras.metrics.MeanAbsoluteError(name='mae'),
            keras.metrics.CosineSimilarity(name='cosine similarity'),
        ]

        # compile model
        model.compile(#loss=self.custom_loss_function,
                      loss=tf.keras.losses.cosine_similarity,
                      optimizer=optimizer,
                      metrics=metrics)
        
        return model
    
    def custom_loss_function(self, y_true, y_predicted):
        """Custom loss function based on ranks.\
           Computes similarities between true element and word vectors and predicted element an word vectors.\
           Returns MSE between those similarities. 

        Args:
            y_true (Tensor): True word vector.
            y_predicted (Tensor): Predicted word vector.

        Returns:
            float: MSE.
        """        
        # get similarities
        similarities_true = tf.matmul(self.element_vectors_tensor, y_true, transpose_b=True)
        similarities_pred = tf.matmul(self.element_vectors_tensor, y_predicted, transpose_b=True)
    
        # get mse
        return backend.mean(backend.sum(backend.square(similarities_true - similarities_pred)))
        
    def get_element_probabilities(self, prediction_vectors, true_idx):
        """Computes ranks of the true elements for each prediction. \
           Returns these ranks and probabilities for each prediction and each element.

        Args:
            prediction_vectors (ndarray(dtype=float, ndim=2)): Predicted word vectors.
            true_idx (ndarray(dtype=int, ndim=1), optional): True element index of the predicted vectors.
            
        Returns:
            tuple: 
                - test_probabilities (ndarray(dtype=float, ndim=2)): Predicted probabilities for each element on prediction data set.
                - test_ranks (ndarray(dtype=int, ndim=1)): Rank of true elements for each prediction. Is only returned if true_idx ist not None.
        """
        # print info for user
        print('\nGet element probabilities and predicted ranks of true results.')

        # get similarities
        similarities = cosine_similarity(self.element_vectors, prediction_vectors)
        
        # apply softmax
        probabilities = helpers.softmax(np.transpose(similarities))

        # get ranks
        ranks = pd.DataFrame(similarities)
        ranks = ranks.rank(method='dense', ascending=False).astype(int)
        ranks = ranks.values

        # get predicted rank of true result 
        result_ranks = list()
        for idx in range(len(prediction_vectors)):
            # only append rank results if combination was truly successful
            if true_idx[idx,2] == 1:
                result_ranks.append(ranks[int(true_idx[idx,3])][idx])
    
        return probabilities, result_ranks
