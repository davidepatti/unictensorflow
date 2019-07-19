import tensorflow as tf
#converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter = tf.lite.TFLiteConverter.from_saved_model('myModel.h5')
converter.optimizations = [tf.lite.Optimize.OPTIMIZE_FOR_SIZE]
tflite_quant_model = converter.convert()
