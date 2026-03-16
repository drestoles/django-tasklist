from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from .forms import TaskForm
from .models import TaskGroup, Task, Profile

tasks = []

def index(request):
    return HttpResponse('Hello world! This came from the index view.')

def task_list(request):
    form = TaskForm()
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.profile = Profile.objects.get(user=request.user)
            task.save()
            return redirect('blogpage:task_detail', pk=task.pk)
        
            task = Task()
            task.name = form.cleaned_data.get('task_name') 
            task.due_date = form.cleaned_data.get('task_date')
            task.taskgroup = form.cleaned_data.get('taskgroup')
            task.profile = Profile.objects.get(user=request.user)
            task.save()
            return redirect('blogpage:task_detail', pk=task.pk)
    else:
        form = TaskForm()

    tasks = Task.objects.all()

    return render(request, "blogpage/task_list.html", {
        "form": form,
        "task_list": tasks,
        "taskgroups": TaskGroup.objects.all(),
    })

@login_required
def task_detail(request, id):
    task = Task.objects.get(pk=id)

    return render(request, "blogpage/task_detail.html", {
        "task": task,
    })


class TaskListView(ListView):
    model = Task
    template_name = 'blogpage/task_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["task_list"] = Task.objects.filter(profile__user=self.request.user)
        return context
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset(**kwargs)
        context = self.get_context_data(**kwargs)
        context['form'] = TaskForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.profile = Profile.objects.get(user=request.user)
            task.save()

            return self.get(request, *args, **kwargs)
        else:
            self.object_list = self.get_queryset(**kwargs)
            context = self.get_context_data(**kwargs)
            context['form'] = form
            return self.render_to_response(context)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'blogpage/task_detail.html'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    # template_name = "task_form.html"

    def form_valid(self, form):
        form.instance.profile = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "blogpage/task_update.html"