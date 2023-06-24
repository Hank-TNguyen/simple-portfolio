import tensorflow as tf
import tensorflow_hub as hub
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def super_resolve_image(image_path):
    print("Loading the image...")
    # Load the image
    img = cv2.imread(image_path)

    # Convert color space from BGR to RGB
    image_plot = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    print("Original image shape: ", image_plot.shape)

    esrgn_path = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
    model_dir = "./esrgan_model" # Modify this as needed
    model_path = os.path.join(model_dir, "saved_model.pb")

    # Check if the model is saved locally
    if os.path.exists(model_path):
        print("Loading the local ESRGAN model...")
        model = tf.saved_model.load(model_dir)
    else:
        print("Downloading the ESRGAN model...")
        model = hub.load(esrgn_path)
        # Save the model locally
        tf.saved_model.save(model, model_dir)

    # Function to preprocess the images
    def preprocessing(img):
        print("Preprocessing the image...")
        imageSize = (tf.convert_to_tensor(img.shape[:-1]) // 4) * 4
        cropped_image = tf.image.crop_to_bounding_box(
            img, 0, 0, imageSize[0], imageSize[1])
        preprocessed_image = tf.cast(cropped_image, tf.float32)
        return tf.expand_dims(preprocessed_image, 0)

    # Function to employ the model
    def srmodel(img):
        print("Applying super resolution...")
        preprocessed_image = preprocessing(img)  # Preprocess the LR Image
        new_image = model(preprocessed_image)  # Runs the model
        # returns the size of the original argument that is given as input
        return tf.squeeze(new_image)

    # Apply super resolution
    hr_image = srmodel(image_plot)

    print("Super resolution complete. Saving the image...")

    # Convert the tensor to numpy array and then scale it to range [0, 255]
    hr_image = np.clip(hr_image.numpy() * 255, 0, 255).astype(np.uint8)
    plt.imshow(hr_image)

    # Save the result
    output_image_path = "output_image.jpg"
    cv2.imwrite(output_image_path, cv2.cvtColor(hr_image, cv2.COLOR_RGB2BGR))

    print("Saved the super resolved image as ", output_image_path)

# Usage: 
super_resolve_image('lr_me.jpg')
