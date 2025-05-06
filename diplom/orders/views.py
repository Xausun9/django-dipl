from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import TaskForm
from .models import Task

@login_required
def index(request):
    tasks = request.user.tasks.all()
    return render(request, 'orders/index.html', {'title': 'Home', 'tasks': tasks})

@login_required
def new_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = Task(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                user=request.user
            )
            task.save()
            messages.success(request, 'Your task has been created!')
            return redirect('orders:index')
    else:
        form = TaskForm()
    
    return render(request, 'orders/task_form.html', {'form': form, 'title': 'New Task'})