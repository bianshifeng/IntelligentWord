def option_size(ques):
    return len(ques["options"])


def is_right(ques, option_index):
    op_size = option_size(ques)
    option_index = int(option_index)
    if option_index < 0 or option_index >= int(op_size):
        raise Exception("option_index out of range, must between [0," + str(op_size - 1) + "].")
    option = ques.get("options")[option_index]
    return option.get("isRight")
