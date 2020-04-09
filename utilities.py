import tensorflow as tf


def process_img(input_image):
    """
    Function takes in an image and processes it for prediction via the classifier model
    """
    input_image = tf.keras.preprocessing.image.load_img(input_image, target_size=(200, 200))
    input_image = tf.keras.preprocessing.image.img_to_array(input_image)
    input_image = input_image/255
    return input_image
