from ..models import Word
import numpy as np
import random
from ..utils import get_user


# 获取训练和测试数据集
def gen_train_test_data(request, maxrecord_size):
    orign_single_vector_data = single_vector_data_train(request, maxrecord_size)
    # 从原数据中随机取70%数据作为训练数据
    train_data = random.sample(orign_single_vector_data, int(len(orign_single_vector_data) * 0.7))
    # 元数据中剩余的数据作为测试数据
    test_data = []
    for orign_item in orign_single_vector_data:
        if orign_item not in train_data:
            test_data.append(orign_item)
    train_x, train_y = process_data(train_data)
    test_x, test_y = process_data(test_data)
    return train_x, train_y, test_x, test_y


# 获取需要预测的数据
def gen_forecate_data(request, maxrecord_size):
    orign_single_vector_data = single_vector_data_forecast(request, maxrecord_size)
    forecate_x, forecate_y = process_data(orign_single_vector_data)
    forecast_log = Word.objects.dump_ml_forecast_log(get_user(request), maxrecord_size)
    forecast_word_list = []
    for item in forecast_log:
        fw = Word.objects.get_word(item["word_id"])
        forecast_word_list.append(fw)
    return forecate_x, forecast_log, forecast_word_list


# 处理训练数据
# 将数据分为特征组x 和预测特征y
# x中去除word_id,is_known;  y中记录的是is_known
def process_data(processed_data_list):
    x_group_data = []
    y_group_data = []
    for processed_data in processed_data_list:
        x_item_data = []
        for k in processed_data.keys():
            if k != "word_id" and k != "is_known":
                x_item_data.append(int(processed_data[k]))
        x_group_data.append(x_item_data)
        is_know = int(processed_data["is_known"])
        y_group_data.append(is_know)
    x = np.array(x_group_data)
    y = np.array(y_group_data)
    return x, y


# 训练数据处理
def single_vector_data_train(request, max_record_size):
    return data_to_single_vector(get_train_log(request, max_record_size))


# 预测数据处理
def single_vector_data_forecast(request, max_record_size):
    return data_to_single_vector(get_forecate_log(request, max_record_size))


# 获取数据库中的训练数据日志
def get_train_log(requset, max_record_size):
    return Word.objects.dump_ml_training_log(get_user(requset), max_record_size)


# 获取数据库中的需要被预测的数据日志
def get_forecate_log(requset, max_record_size):
    return Word.objects.dump_ml_forecast_log(get_user(requset), max_record_size)


# 处理数据
# 将每个单词的数据格式处理为数值化的行向量形式
def data_to_single_vector(log_data):
    processed_data_list = []
    dump_log_list = log_data
    for dump_log in dump_log_list:
        processed_data = {}
        processed_data["word_id"] = dump_log["word_id"]
        processed_data["is_known"] = dump_log["is_known"]
        # processed_data["mark_time"] = dump_log["mark_time"]

        mark_time = int(dump_log["mark_time"])
        ques_record_log = dump_log["ques_record_log"]

        # 做题结果表示为行向量的形式,
        # 第0,1,2维度分别代表 三种题型:word2def def2word sent2word
        # 每个维度正数表达做对,负数表达做错,0表示没有做题
        # 大小代表做题时间距离标记认识时间的总和
        ques_vector = [0, 0, 0]

        for ques_record in ques_record_log:
            record_time = int(ques_record["record_time"])
            dtime = mark_time - record_time
            if ques_record["is_right"]:
                dtime = abs(dtime)
            else:
                dtime = -abs(dtime)

            ques_type = ques_record["ques_type"]
            if ques_type == "word2def":
                ques_vector[0] += dtime
            elif ques_type == "def2word":
                ques_vector[1] += dtime
            elif ques_type == "sent2word":
                ques_vector[2] += dtime

        for i, v in enumerate(ques_vector):
            processed_data["v_" + str(i)] = v

        processed_data_list.append(processed_data)
    return processed_data_list
