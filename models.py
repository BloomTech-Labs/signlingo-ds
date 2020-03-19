import tensorflow as tf


def initial_model():
    model = tf.keras.models.load_model('initial_model')
    return model
