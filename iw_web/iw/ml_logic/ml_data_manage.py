from ..models import Word
import numpy as np
import random
from ..utils import get_user


def get_trainning_data(requset, max_record_size):
    orign_processed_data = data_processing(requset, max_record_size)
    # 从全部的被处理的数据中随机选取70%的数据用于做训练数据
    processed_data_list = random.sample(orign_processed_data, int(len(orign_processed_data) * 0.7))
    x, y = process_data_for_train(processed_data_list)
    return x, y


def get_validate_data(requset, max_record_size):
    orign_processed_data = data_processing(requset, max_record_size)
    # 从全部的被处理的数据中随机选取30%的数据用于做测试数据
    processed_data_list = random.sample(orign_processed_data, int(len(orign_processed_data) * 0.3))
    x, y = process_data_for_train(processed_data_list)
    return x, y


def process_data_for_train(processed_data_list):
    x_group_data = []
    y_group_data = []
    for processed_data in processed_data_list:
        x_item_data = []
        for k in processed_data.keys():
            if k != "word_id":
                x_item_data.append(int(processed_data[k]))
        x_group_data.append(x_item_data)

        is_know = int(processed_data["is_known"])
        if is_know == 0:
            y_lable = [1, 0, 0]
        elif is_know == 1:
            y_lable = [0, 1, 0]
        else:
            y_lable = [0, 0, 1]
        y_group_data.append(y_lable)
    x = np.array(x_group_data)
    y = np.array(y_group_data)
    return x, y


def data_processing(requset, max_record_size):
    processed_data_list = []
    user = get_user(requset)
    dump_log_list = Word.objects.dump_ml_training_log(user, max_record_size)
    for dump_log in dump_log_list:
        processed_data = {}
        processed_data["word_id"] = dump_log["word_id"]
        processed_data["is_known"] = dump_log["is_known"]
        processed_data["mark_time"] = dump_log["mark_time"]

        mark_time = int(dump_log["mark_time"])
        ques_record_log = dump_log["ques_record_log"]

        # 做题记录数据处理
        processed_record_list = []
        # 还差几个数据 用0补齐
        dcount = max_record_size - len(ques_record_log)

        for ques_record in ques_record_log:
            record = {}
            record_time = int(ques_record["record_time"])
            record["dtime"] = mark_time - record_time
            ques_type = ques_record["ques_type"]
            if ques_type == "word2def":
                record["ques_type"] = 1
            elif ques_type == "def2word":
                record["ques_type"] = 2
            elif ques_type == "sent2word":
                record["ques_type"] = 3

            if ques_record["is_right"]:
                record["is_right"] = 1
            else:
                record["is_right"] = 2
            processed_record_list.append(record)

        if dcount > 0:
            for i in range(dcount):
                processed_record_list.append({
                    "dtime": 100000000,  # 补充的数据  初始时间差设置为一个很大的数字
                    "ques_type": 0,
                    "is_right": 0
                })

        processed_record_list.sort(key=lambda obj: obj.get('dtime'))

        # 将record list 并为一条数据
        for i, record in enumerate(processed_record_list):
            processed_data["dtime__" + str(i)] = record["dtime"]
            processed_data["ques_type__" + str(i)] = record["ques_type"]
            processed_data["is_right__" + str(i)] = record["is_right"]

        processed_data_list.append(processed_data)
    return processed_data_list
