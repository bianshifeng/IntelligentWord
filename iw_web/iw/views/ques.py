from django.http import HttpResponseRedirect
from django.shortcuts import render

from ..biz.recorder import record
from ..biz.ques_builder import gen_ques_list
from ..biz.exercise import is_right
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def ques_list(request, size):
    return render(request, 'ques.html', {
        "tips": gen_ques_list(request,int(size))
    })


def get_ques_response(request, pre_ques_is_right=-1):
    ques_session = get_ques_session(request)
    if ques_session:
        ques_list = ques_session.get("ques_list")
        if len(ques_list) is 0:
            del_ques_session(request)
            return HttpResponseRedirect("/data/")
        index = ques_session.get("ques_index")
        progress = index / len(ques_list) * 100;
        return render(request, 'ques.html', {
            "pre_ques_is_right": pre_ques_is_right,
            "count": len(ques_list),
            "index": index,
            "progress": progress,
            "ques": ques_list[index]
        })
    else:
        return render(request, 'ques.html', {
            "tips": "题目为空"
        })


# 开始答题  包括题目生成逻辑
@login_required(login_url="/login/")
def start_exercise(request, size=10):
    if has_start_exercises(request):
        return get_ques_response(request)

    ques_list = gen_ques_list(request,int(size))
    request.session['has_start'] = True
    gen_ques_session(request, ques_list, 0)
    return get_ques_response(request)


# 答题
@login_required(login_url="/login/")
def answer(request, option_pos):
    option_index = int(option_pos) - 1

    if not has_start_exercises(request):
        return HttpResponseRedirect("/ques/start_exercise/10")
    else:
        ques_session = get_ques_session(request)
        size = len(ques_session.get("ques_list"))
        index = ques_session.get("ques_index")

        ques = get_ques_in_session(request, index)
        pre_ques_is_right = is_right(ques, option_index)

        # session 中保存做题记录
        record(request,ques, pre_ques_is_right)

        if index < size - 1:
            update_ques_session_index(request, index + 1)
            return get_ques_response(request, pre_ques_is_right)
        else:
            return end_exercise(request)


# 答题结束
@login_required(login_url="/login/")
def end_exercise(request):
    del_ques_session(request)
    return render(request, 'ques.html', {
        "tips": "测试结束"
    })


# -------session 管理逻辑 start--------

def has_start_exercises(request):
    return request.session.get('has_start', False)


def get_ques_in_session(request, index):
    return get_ques_session(request)["ques_list"][index]


def gen_ques_session(request, ques_list, index=0):
    ques_session = {"ques_list": ques_list,
                    "ques_index": index}
    request.session["ques_session"] = ques_session


def get_ques_session(request):
    return request.session.get('ques_session')


def update_ques_session_index(request, index):
    ques_session = get_ques_session(request)
    ques_session["ques_index"] = index
    request.session["ques_session"] = ques_session


def del_ques_session(request):
    if request.session.get('has_start'):
        del request.session['has_start']
    if request.session.get('ques_session'):
        del request.session["ques_session"]

# -------session 管理逻辑 end----------
