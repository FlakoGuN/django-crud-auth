from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TaskForm, Tasks
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render ( request, 'home.html')

@login_required
def tasks(request):
    task=Tasks.objects.filter(user=request.user, datecompleted__isnull=True)
    return render ( request, 'tasks.html',{'tasks':task})
@login_required
def tasks_completed(request):
    task=Tasks.objects.filter(user=request.user, datecompleted__isnull=False)
    return render ( request, 'tasks.html',{'tasks':task})    

def singup(request):
    if request.method == 'GET':
        return render (request, 'singup.html', {'form': UserCreationForm})
    else:
        if request.POST ['password1'] == request.POST ['password2']:
            try:
               user = User.objects.create_user(username=request.POST['username'],
               password=request.POST['password2']) 
               user.save()
               login (request, user)
               return redirect ('/singin')
            except IntegrityError:
               return render(request, 'singup.html', {'form': UserCreationForm, 'error':'El Usuario ya existe'})
     
        return render(request, 'singup.html', {'form': UserCreationForm, 'error':'Las claves no cuadran'})

@login_required
def singout (request):
   logout(request)
   return redirect('home')

def singin (request):
    if request.method == 'GET':
      return render(request, 'singin.html', {'form': AuthenticationForm})
    else:
       user= authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return render(request, 'singin.html', {'form': AuthenticationForm, 'error':'Usuario no encontrado'})
    else:
        login (request, user)
        return redirect ('tasks')

@login_required
def create_tasks(request):
    if request.method == 'GET':
      return render ( request, 'create_tasks.html', {'form': TaskForm})
    else:
       try:
        form = TaskForm(request.POST)
        new_task = form.save(commit=False)
        new_task.user = request.user
        new_task.save()
        return redirect('tasks')
       except:
        return render ( request, 'create_tasks.html', {'form': TaskForm, 'error':'Meta datos validos por favor'})

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
       task = get_object_or_404(Tasks, pk=task_id, user=request.user)
       form = TaskForm(instance=task)
       return render ( request, 'task_detail.html',{'task':task, 'form': form})
    else:
        try:
         task = get_object_or_404(Tasks, pk=task_id, user=request.user)
         form = TaskForm(request.POST, instance=task)
         form.save()
         return redirect('tasks')
        except:
            return render ( request, 'task_detail.html',{'task':task, 'form': form, 'error':'Meta datos validos por favor'})
    
@login_required
def complete_task(request, task_id):
  task = get_object_or_404(Tasks, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
  task = get_object_or_404(Tasks, pk=task_id, user=request.user)
  if request.method == 'POST':
    task.delete()
    return redirect('tasks')

