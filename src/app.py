import config_prop
import os
import json
import numpy as np
from flask import Flask, render_template, request, jsonify
import multi_layer_perceptron_model as mlp_model
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Dropout
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


app = Flask(__name__)
global_model = None
config = config_prop.get_conf()


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/train-model', methods=['POST'])
def train_model():
    global global_model
    conf = request.get_json(silent=True)
    model = mlp_model.MultiLayerPerceptronModel(epochs=conf['epochs'], data_quantity=int(config['TRAIN_SIZE']),
                                                use_pca=conf['usePca'], pca_components=conf['nbComponents'])
    model.load()
    model.process()

    mlp = Sequential()
    mlp.add(Dense(128, input_dim=model.dim))
    mlp.add(Activation('relu'))
    mlp.add(Dropout(0.15))
    mlp.add(Dense(128))
    mlp.add(Activation('relu'))
    mlp.add(Dropout(0.15))
    mlp.add(Dense(model.nb_class))
    mlp.add(Activation('softmax'))
    mlp.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    model.set_model(mlp)
    model.train_model()

    global_model = model
    return jsonify(conf)


@app.route('/predict/<index>', methods=['GET'])
def predict_image(index):
    global global_model
    global_model.load_test()
    return json.dumps(global_model.predict(int(index)), cls=NumpyEncoder)


@app.route('/already-trained')
def already_trained():
    global global_model

    if global_model is not None:
        return jsonify({'trained': global_model.trained})
    return jsonify({'trained': False})


@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
