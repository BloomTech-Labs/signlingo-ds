import tensorflow as tf


def process_img(input_image):
    """
    Function takes in an image and processes it for prediction via the initial model
    """
    input_image = tf.keras.preprocessing.image.load_img(input_image, grayscale=True, target_size=(28,28))
    input_image = tf.keras.preprocessing.image.img_to_array(input_image)
    input_image = input_image.flatten()/255
    return input_image
