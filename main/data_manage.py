import json
from random import sample


# save_init_json_data("../data/response.json","../data/word_list.json")
from main.config import config, get_config
from main.parser import parse_response_json


def save_init_json_data(json_path, to_json_path):
    config("init_word_list_json_path", to_json_path)
    word_list = parse_response_json(json_path)
    init_word_list = []
    for word in word_list:
        word["mark"] = 0
        word["ques_word2def_wrong_times"] = 0
        word["ques_def2word_wrong_times"] = 0
        word["ques_sentence_wrong_times"] = 0
        word["ques_spell_wrong_times"] = 0

        word["ques_word2def_newest_record"] = []
        word["ques_def2word_newest_record"] = []
        word["ques_sentence_newest_record"] = []
        word["ques_spell_newest_record"] = []

        init_word_list.append(word)
    save_json_data(init_word_list, to_json_path)


# 保存数据
def save_json_data(word_list, to_json_path=get_config("init_word_list_json_path")):
    json.dump(word_list, fp=open(to_json_path, 'w',encoding="utf8"))


# 得到当前的单词总列表
def load_word_list():
    init_word_list_json_path = get_config("init_word_list_json_path")
    with open(init_word_list_json_path, "r", encoding="utf8") as json_file:
        word_list = json.loads(json_file.read())
        return word_list


# 随机从word list 中取一定数量的单词
def random_load_words(size,except_words=[]):
    word_list = load_word_list()
    sub_word_list = [i for i in word_list if i not in except_words]
    return sample(sub_word_list, size)


# 更新单词列表
def update_word_list(update_words):
    word_list = load_word_list()
    old_words = []
    new_words = []
    for u_word in update_words:
        for t_word in word_list:

            # 校验是否是同一个单词 这里不确定主键是什么,暂定为wordId和word 唯一确定一个词
            if t_word.get("wordId") == u_word.get("wordId") \
                    and t_word.get("word") == u_word.get("word"):
                old_words.append(t_word)
                new_words.append(u_word)

    for ow in old_words:
        # print(">>> remove word : " + str(ow))
        word_list.remove(ow)

    # print(">>> add words : " + str(new_words))
    word_list.extend(new_words)

    save_json_data(word_list)

# 根据wordId 和 word 查询一个单词
def get_word(wordId, word):
    for w in load_word_list():
        if str(w.get("wordId")) == str(wordId) and w.get("word") == word:
            return w

# 获取word为指定字符串的单词列表
def get_words(word):
    words = []
    for w in load_word_list():
        if w.get("word") == word:
            words.append(w)
    return words
