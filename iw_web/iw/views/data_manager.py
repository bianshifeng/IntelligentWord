from random import sample

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from ..ml_logic.ml_data_manage import single_vector_data_train, gen_train_test_data, gen_forecate_data
from ..ml_logic.train_logic_new import ml_train
from ..models import Word, QuesRecord
from ..utils import get_main_path, get_user
import os, json,numpy


@login_required(login_url="/iw/login/")
def index(request):
    return render(request, 'data_manager.html')


@login_required(login_url="/iw/login/")
def init(request):
    print(">>> 开始初始化数据")
    origin_data_json = os.path.join(get_main_path(), "origin_data", "response.json")
    word_list = load_word_list(origin_data_json)

    # 为了方便测试,目前只随机取20条记录
    word_list = sample(word_list, 20)

    save_word_modle(request, word_list)
    print(">>> 初始化数据结束")
    return render(request, 'data_manage_result.html', {
        "tips": "初始化成功!"
    })


def load_word_list(json_path):
    with open(json_path, "r", encoding="utf8") as json_file:
        json_str = json_file.read()
        result = json.loads(json_str)
        word_list = result["data"]["wordList"]
        return word_list


def save_word_modle(requset, word_list):
    for w in word_list:
        sent = ""
        sent_def = ""
        if w.get("sentList"):
            sentObj = w.get("sentList")[0]
            sent = sentObj.get("sentence")
            sent_def = sentObj.get("trans")

        Word.objects.save(user=get_user(request=requset),
                          fromLang=w.get("fromLang") if w.get("fromLang") else "",
                          toLang=w.get("toLang") if w.get("toLang") else "",
                          definition=w.get("definition") if w.get("definition") else "",
                          phonetic=w.get("symbol1") if w.get("symbol1") else "",
                          word=w.get("word") if w.get("word") else "",
                          audio=w.get("audio") if w.get("audio") else "",
                          sentence=sent,
                          trans=str(sent_def)
                          )


@login_required(login_url="/iw/login/")
def clear_words(request):
    user = get_user(request)
    QuesRecord.objects.delete_all(user)
    Word.objects.delete_all(get_user(request))
    return render(request, 'data_manage_result.html', {
        "tips": "背词记录 和 单词 信息已经清空!"
    })


@login_required(login_url="/iw/login/")
def clear_records(request):
    user = get_user(request)
    QuesRecord.objects.delete_all(user)
    return render(request, 'data_manage_result.html', {
        "tips": "背词记录信息已经清空!"
    })


@login_required(login_url="/iw/login/")
def dump_origin_data(request, max_record_size):
    max_record_size = int(max_record_size)
    user = get_user(request)
    dump_log = json.dumps(Word.objects.dump_ml_training_log(user, max_record_size))
    return HttpResponse(dump_log)


@login_required(login_url="/iw/login/")
def dump_processed_data(request, max_record_size):
    max_record_size = int(max_record_size)
    dump_log = json.dumps(single_vector_data_train(request, max_record_size))
    return HttpResponse(dump_log)


# 生成用于训练和测试的矩阵数据
@login_required(login_url="/iw/login/")
def dump_train_test_nparray_data(request, max_record_size):
    max_record_size = int(max_record_size)
    train_x, train_y, test_x, test_y = gen_train_test_data(request, max_record_size)
    return render(request, 'train_test_data.html', {
        "train_x": train_x,
        "train_y": train_y,
        "test_x": test_x,
        "test_y": test_y
    })


@login_required(login_url="/iw/login/")
def dump_forecate_nparray_data(request, max_record_size):
    max_record_size = int(max_record_size)
    forecate_x, forecast_log, forecast_word_list = gen_forecate_data(request, max_record_size)
    return render(request, 'forecate_data.html', {
        "forecate_x": forecate_x,
        "forecast_log": forecast_log,
        "forecast_word_list": forecast_word_list
    })


@login_required(login_url="/iw/login/")
def training(request, max_record_size):
    max_record_size = int(max_record_size)
    train_result = ml_train(request, max_record_size)

    list_y = train_result.get("y")
    word_list = train_result.get("forecast_word_list")
    forecast_word_list = []
    for index, item in enumerate(list_y):
        word = word_list[index]
        if int(item) is 1:
            forecast = "认识"
        else:
            forecast = "不认识"
        forecast_word_list.append({"word":word,
                                   "forecast":forecast})

    return render(request, 'train_result.html', {
        "accuracy_score": train_result.get("accuracy_score"),
        "forecast_word_list": forecast_word_list,
        "model_dir": train_result.get("model_dir")
    })
