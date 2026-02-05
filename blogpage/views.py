from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import TaskForm

tasks = []

def index(request):
    return HttpResponse('Hello world! This came from the index view.')

def task_list(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            tasks.append( (form.cleaned_data['task_name'], form.cleaned_data['task_date']) )
            return redirect('/blogpage/list')
    else:
        form = TaskForm()

    return render(request, "blogpage/task_list.html", {
        "form": form,
        "tasks": tasks,
    })