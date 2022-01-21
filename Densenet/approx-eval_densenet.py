import sys
if len(sys.argv) < 3:
    print('Usage: '+sys.argv[0]+' <h5file> <input>')
    print('- just use imagenet as h5 file name to download and use default h5')
    print('- use summary as argument to get the network layers description')
    exit(0)

sys.path.append(".")
sys.path.append('../keras-applications')

import keras_approx
from keras_approx.densenet import DenseNet201
#from keras.applications.densenet import DenseNet201

from tensorflow.keras.preprocessing import image
#from keras.applications.densenet import preprocess_input
#from keras.applications.densenet import decode_predictions
from keras_approx.densenet import preprocess_input
from keras_approx.densenet import decode_predictions

from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD
import numpy as np
#import cv2
from tensorflow.keras.layers import Input

weights_path = sys.argv[1]


#model = InceptionV3(include_top=True, weights=weights_path, input_tensor=None, input_shape=None, pooling=None, classes=1000)
model = DenseNet201(include_top=True, weights='imagenet', input_tensor=None, input_shape=(224,224,3), pooling=None, classes=1000)
#model = InceptionV3(include_top=True, weights='imagenet', input_tensor=None, input_shape=(299,299,3), pooling=None, classes=1000)

#model.save('inception.h5')

#Alternative custom input shape
#input_tensor = Input(shape=(224, 224, 3))
#model = InceptionV3(input_tensor=input_tensor, weights='imagenet', include_top=True)


if __name__ == "__main__":

    if sys.argv[2] == 'summary':
        model.summary()
        exit(0)

    img_path = sys.argv[2]
    #img = image.load_img(img_path, target_size=(299, 299))
    img = image.load_img(img_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    print('Input image shape:', x.shape)

    preds = model.predict(x)
    print(decode_predictions(preds))

#########################################
    print('--> Starting evalutation...')
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    from tensorflow.keras import metrics
    
    def in_top_k(y_true, y_pred):
        return metrics.top_k_categorical_accuracy(y_true,y_pred,k=5)

    val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    validation_generator = val_datagen.flow_from_directory('./imagenet-data/validation',
		target_size=(224, 224), 
		#target_size=(299, 299), 
		batch_size=10,
		class_mode='categorical',
		shuffle=False)

    model.trainable=False
    model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy', in_top_k])

    results = model.evaluate(validation_generator, steps=1000, workers=1, max_queue_size=1)

    print('--> Results for '+sys.argv[1])
    print(model.metrics_names)
    print(results)

#########################################


