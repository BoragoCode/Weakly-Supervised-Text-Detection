
import numpy as np
import cv2
from keras.models import Model
from keras.applications.resnet50 import ResNet50, preprocess_input

def resize_imgs(imgs):
    resized = []
    for img in imgs:
        resized.append(cv2.resize(img, (224,224)))
    resized = np.array(resized)
    return resized

class FeatureExtractor(object):
    def __init__(self):
        model = ResNet50(weights='imagenet')
        self._resnet = Model(inputs=model.input, 
                             outputs=(model.layers[-2].output))
    
    def run(self, images):
        """
        # Args
            images : array, shape of (N, H, W, C)
            
        # Returns
            features : array, shape of (N, 2048)
        """
        xs = resize_imgs(images)
        xs = xs.astype(np.float64)
        xs = preprocess_input(xs)
        features = self._resnet.predict(xs, verbose=1)
        return features

    def get_image_feature(self, images):
        model = ResNet50(weights='imagenet')
        image_feature_model = Model(inputs=model.input,
                                    outputs=(model.layers[-4].output)) 
        xs = resize_imgs(images)
        xs = xs.astype(np.float64)
        xs = preprocess_input(xs)
        features = image_feature_model.predict(xs)
        return features

if __name__ == "__main__":
    from keras.preprocessing import image
    img = image.load_img("..//images//dog.png", target_size=(224, 224))
    x = image.img_to_array(img)
    x = x.reshape(-1, 224, 224, 3)
    fe = FeatureExtractor()
    features = fe.run(x)
    print(features.shape)

