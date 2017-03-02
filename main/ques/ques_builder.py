from main.data_manage import random_load_words, get_word
import re

QUES_TYPE_WORD2DEF = "word2def"
QUES_TYPE_DEF2WORD = "def2word"
QUES_TYPE_SENT2WORD = "sent2word"

# 加载confusion_count个数的单词用于出题(排除word)
def load_ques_words(word, confusion_count=3):
    word = get_word(word.get("wordId"), word.get("word"))
    words = random_load_words(confusion_count, [word])
    return word, words

# 根据【题目类型】生成【题干类型】和【选项类型】
def get_content_option_type_by_ques_type(ques_type):
    content_type = ""
    option_type = ""
    if QUES_TYPE_WORD2DEF == ques_type:
        content_type = "word"
        option_type = "definition"
    elif QUES_TYPE_DEF2WORD == ques_type:
        content_type = "definition"
        option_type = "word"
    elif QUES_TYPE_SENT2WORD == ques_type:
        content_type = "sentence"
        option_type = "word"
    return content_type, option_type

# 题目生成基础逻辑
def baseic_gen_ques(word, type, confusion_count=3,is_debug=False):
    word, words = load_ques_words(word, confusion_count)
    ques = {}
    ques["type"] = type
    # eg: sentence word
    content_type, option_type = get_content_option_type_by_ques_type(type)

    ques["content"] = word.get(content_type)

    print("gen ques type : " + type)

    if type is QUES_TYPE_SENT2WORD:
        ques["content"] = dig_sentence_content(word.get("word"),ques["content"])
    options = []
    options.append({"option": word.get(option_type), "is_rignt": "1"})
    for w_word in words:
        options.append({"option": w_word.get(option_type), "is_rignt": "0"})
    ques["options"] = options
    if is_debug:
        print("ques >>> " + str(ques))
    return ques

def dig_sentence_content(word,sentence):
    print("dig sentence >> word:" + word + " sentence : " + sentence)
    dig_sent = re.sub("\[.*.\]", "____", sentence,count=1)
    if dig_sent:
        return dig_sent
    return re.sub(word, "____", sentence,count=1,flags=re.I)

# 根据单词生成【单词选释义题】
def gen_word2def_ques(word,is_debug=False):
    return baseic_gen_ques(word, QUES_TYPE_WORD2DEF, confusion_count=3,is_debug=is_debug)

# 根据单词生成【释义选单词题】
def gen_def2word_ques(word,is_debug=False):
    return baseic_gen_ques(word, QUES_TYPE_DEF2WORD, confusion_count=3,is_debug=is_debug)

# 根据单词生成【例句题】
def gen_sent2word_ques(word,is_debug=False):
    return baseic_gen_ques(word, QUES_TYPE_SENT2WORD, confusion_count=3,is_debug=is_debug)


# 命令行输出一道题目,is_debug 是否显示正确选项
def cmd_out_ques(ques, is_debug=False):
    ques_type = ques.get("type")
    ques_content = ques.get("content")
    ques_options = ques.get("options")
    print(">> 题目类型 : " + ques_type)
    print(">> 题目 : " + ques_content)
    print("--------")
    for i, option in enumerate(ques_options):
        if is_debug:
            print(">> [" + str(i) + "] " + str(option))
        else:
            print(">> [" + str(i) + "] " + str(option.get("option")))


# print(load_ques_words({"wordId": 55661, "word": "feel"}))
# cmd_out_ques(gen_word2def_ques({"wordId": 55661, "word": "feel"}))
# cmd_out_ques(gen_def2word_ques({"wordId": 55661, "word": "feel"}))

# cmd_out_ques(gen_sent2word_ques({"wordId": 55661, "word": "feel"},is_debug=True))
