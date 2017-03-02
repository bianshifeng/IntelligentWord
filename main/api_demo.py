
# 初始化数据 将服务端返回的json数据 初始化处理为一个用于智能背词的数据格式 存在目标文件中
from main import get_main_path
from main.data_manage import save_init_json_data, load_word_list, random_load_words, update_word_list, get_word, \
    get_words

# 是否执行过初始化
is_init = True

if not is_init:
    save_init_json_data(get_main_path() + "/../data/response.json",
                        get_main_path() + "/../data/word_list.json")
else:
    # 加载全部的单词列表
    load_word_list()

    # 随机取一定数量的单词 (except_words为不包含的单词列表)
    random_load_words(3, except_words=[get_word(3462493, "明日")])

    # 更新单词列表
    update_word_list([{"wordId": 55661, "word": "feel"}])

    # 根据主键获取一个单词
    get_word(3462493, "明日")

    # 获取word为指定字符串的单词列表
    get_words("明日")
