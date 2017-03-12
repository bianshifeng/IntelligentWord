from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .ques import has_start_exercises

@login_required(login_url="/login/")
def index(request):
    return render(request, 'index.html', {
        "has_start":has_start_exercises(request)
    })