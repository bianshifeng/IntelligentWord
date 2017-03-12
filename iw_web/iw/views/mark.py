from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from ..models import Word
from ..utils import get_user

@login_required(login_url="/login/")
def word_list(request):
    word_list = Word.objects.get_user_word_list(get_user(request))
    return render(request, 'word_list.html', {
        "word_list_count":len(word_list),
        "word_list": word_list
    })

@login_required(login_url="/login/")
def word_list_mark_is_known(request,word_id,is_known):
    Word.objects.update_word_is_known(word_id,is_known)
    return HttpResponseRedirect("/mark/word_list/")

@login_required(login_url="/login/")
def word_detail(request,word_id):

    word = Word.objects.get_word(word_id)

    return render(request, 'mark.html', {
        "word":word
    })


@login_required(login_url="/login/")
def mark_is_known(request,word_id,is_known):
    Word.objects.update_word_is_known(word_id,is_known)
    return HttpResponseRedirect("/mark/word_detail/" + str(word_id))