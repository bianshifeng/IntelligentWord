import random

import re

from ..models import Word
from ..utils import get_user

TYPE_WORD2DEF = "word2def"
TYPE_DEF2WORD = "def2word"
TYPE_SENT2WORD = "sent2word"


def gen_ques_list(requset, size, option_count=4, shuffle=True):
    words = Word.objects.get_random_user_words(get_user(requset), size)
    ques_list = []
    for w in words:
        q_w2d = gen_ques(requset, w.id, TYPE_WORD2DEF, option_count=option_count, shuffle=shuffle)
        q_d2w = gen_ques(requset, w.id, TYPE_DEF2WORD, option_count=option_count, shuffle=shuffle)
        q_s2w = gen_ques(requset, w.id, TYPE_SENT2WORD, option_count=option_count, shuffle=shuffle)
        if q_w2d:
            ques_list.append(q_w2d)
        if q_d2w:
            ques_list.append(q_d2w)
        if q_s2w:
            ques_list.append(q_s2w)
    random.shuffle(ques_list)
    return ques_list


def gen_ques(requset, word_id, ques_type, option_count=4, shuffle=True):
    ques = {}
    ques["word_id"] = word_id
    ques["ques_type"] = ques_type
    ques["title"] = gen_ques_title(word_id, ques_type)
    ques["options"] = gen_ques_options(requset, word_id, ques_type, option_count=option_count, shuffle=shuffle)
    if is_good_ques(ques):
        return ques
    else:
        return


def gen_ques_title(word_id, ques_type):
    w = Word.objects.get_word(word_id)
    if TYPE_WORD2DEF is ques_type:
        return w.word
    elif TYPE_DEF2WORD is ques_type:
        return w.definition
    elif TYPE_SENT2WORD is ques_type:
        return dig_sentence_content(w.word, w.sentence)


def dig_sentence_content(word, sentence):
    print("dig sentence >> word:" + word + " sentence : " + sentence)
    dig_sent = re.sub("\[.*.\]", "____", sentence, count=1)
    if dig_sent != sentence:
        return dig_sent
    return re.sub(word, "____", sentence, count=1, flags=re.I)


def gen_ques_options(requset, word_id, ques_type, option_count=4, shuffle=True):
    cw, ows = gen_cw_ows(requset, option_count - 1, word_id)
    options = []
    if ques_type is TYPE_WORD2DEF:
        option = {"option": cw.definition, "isRight": 1}
        options.append(option)
        for ow in ows:
            option = {"option": ow.definition, "isRight": 0}
            options.append(option)
    elif ques_type is TYPE_DEF2WORD or ques_type is TYPE_SENT2WORD:
        option = {"option": cw.word, "isRight": 1}
        options.append(option)
        for ow in ows:
            option = {"option": ow.word, "isRight": 0}
            options.append(option)
    if shuffle:
        random.shuffle(options)
    return options


# 生成用于出题的单词,包括当前单词和选项单词
def gen_cw_ows(requset, count, word_id):
    word = Word.objects.get_word(word_id)
    user = get_user(requset)
    words = Word.objects.get_random_user_words_except_word(user, word_id, count)
    return word, words


def is_good_ques(ques):
    if not ques["title"]:
        print(str(ques["word_id"]) + ">>>>>>" + str(
            ques["ques_type"]) + " not gen success, because question title is empty")
        return False
    options = ques["options"]
    for option in options:
        if option["isRight"] and not option["option"]:
            print(str(ques["word_id"]) + ">>>>>>" + str(
                ques["ques_type"]) + " not gen success, because question right option is empty")
            return False
    return True
