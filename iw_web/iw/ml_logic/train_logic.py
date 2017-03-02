import tensorflow as tf
from .ml_data_manage import get_trainning_data, get_validate_data


# 训练
def ml_train(requset, max_record_size):
    x = tf.placeholder(tf.float32, [None, max_record_size * 3 + 2])
    W = tf.Variable(tf.zeros([max_record_size * 3 + 2, 3]))
    b = tf.Variable(tf.zeros([3]))

    y = tf.nn.softmax(tf.matmul(x, W) + b)
    y_ = tf.placeholder(tf.float32, [None, 3])
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
    train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

    sess = tf.InteractiveSession()
    tf.global_variables_initializer().run()

    # 训练逻辑
    batch_xs, batch_ys = get_trainning_data(requset, max_record_size)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

    # # 使用测试集验证结果  目前数据量过小  需要提升数据量
    test_xs, test_ys = get_validate_data(requset, max_record_size)
    correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    result = sess.run(accuracy, feed_dict={x: test_xs, y_: test_ys})
    return result
