from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import tensorflow as tf
import numpy as np
from .ml_data_manage import gen_train_test_data, gen_forecate_data, get_modle_dir


# 训练
def ml_train(request, max_record_size):
    # Data sets
    # 训练数据 测试数据 获取
    batch_xs, batch_ys, test_xs, test_ys = gen_train_test_data(request, max_record_size)
    if len(batch_xs) is 0:
        raise Exception("训练数据为空,请生成一些训练数据")
    elif len(test_xs) is 0:
        raise Exception("测试数据为空,请生成一些测试数据")
    # 待预测数据
    forcate_data, forecast_log, forecast_word_list = gen_forecate_data(request, max_record_size)
    if len(forecast_word_list) is 0:
        raise Exception("预测数据为空,请生成一些预测数据")
    # 训练模型保存目录
    model_dir = get_modle_dir(request)
    # Load datasets.

    # Specify that all features have real-value data
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=3)]
    # Build 3 layer DNN with 10, 20, 10 units respectively.
    classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                                hidden_units=[10, 20, 10],
                                                n_classes=3,
                                                model_dir=model_dir)
    # Fit model.
    classifier.fit(x=batch_xs,
                   y=batch_ys,
                   steps=2000)
    # Evaluate accuracy.
    accuracy_score = classifier.evaluate(x=test_xs,
                                         y=test_ys)["accuracy"]
    print('Accuracy: {0:f}'.format(accuracy_score))

    new_samples = np.array(forcate_data, dtype=float)
    y = list(classifier.predict(new_samples, as_iterable=True))
    print('Predictions: {}'.format(str(y)))

    train_result = {
        "accuracy_score": accuracy_score,
        "y": y,
        "forecast_word_list": forecast_word_list,
        "model_dir": model_dir
    }
    return train_result
