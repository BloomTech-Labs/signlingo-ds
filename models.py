import tensorflow as tf


def initial_model():
    model = tf.keras.models.load_model('initial_model')
    return model


def best_current_model():
    model = tf.keras.models.load_model('best_current_model')
    return model
