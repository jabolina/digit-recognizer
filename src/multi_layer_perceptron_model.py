import os

import dotenv
import pandas as pd
from keras.utils import np_utils
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

dotenv.load()


class MultiLayerPerceptronModel:
    def __init__(self, epochs=15, data_quantity=5000, use_pca=False, pca_components=25):
        self.data_quantity = data_quantity
        self.dim = -1
        self.nb_class = -1
        self.use_pca = use_pca
        self.pca_components = pca_components

        if int(epochs) > 0:
            self.epochs = int(epochs)
        else:
            self.epochs = 15

        self.model = None
        self.label = None
        self.images = None
        self.test_data = None
        self.trained = False

    def load(self):
        all_images = pd.read_csv(os.getenv('CSV_TRAIN_PATH'))
        self.label = all_images.iloc[:self.data_quantity, :1].values
        self.images = all_images.iloc[:self.data_quantity, 1:].values

    def process(self):
        self.images[self.images > 0] = 1
        sc = StandardScaler()
        self.images = sc.fit_transform(self.images)

        if self.use_pca:
            pca = PCA(n_components=self.pca_components)
            self.images = pca.fit_transform(self.images)

        self.label = np_utils.to_categorical(self.label)
        self.dim = self.images.shape[1]
        self.nb_class = self.label.shape[1]

    def set_model(self, model):
        self.model = model

    def train_model(self):
        if self.label is not None and self.images is not None and self.model is not None:
            self.model.fit(self.images, self.label, epochs=self.epochs)
            self.trained = True

    def load_test(self):
        test_images = pd.read_csv(os.getenv('CSV_TEST_PATH'))

        test_images[test_images > 0] = 1
        sc = StandardScaler()
        processed_test_images = sc.fit_transform(test_images)

        if self.use_pca:
            pca = PCA(n_components=self.pca_components)
            processed_test_images = pca.fit_transform(processed_test_images)

        self._test_data = test_images
        self.test_data = processed_test_images

    def predict(self, index):
        if self.test_data is not None and self.model is not None and self.trained:
            y = self.model.predict_classes(self.test_data[index: index + 1])
            return {'predicted': y[0],
                    'image': self._test_data.iloc[index].values.reshape((28, 28))}

        else:
            return {'error': 'And error occurred.'}
