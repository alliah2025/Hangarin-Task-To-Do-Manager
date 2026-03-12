from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task, Category, Priority
from .forms import TaskForm


def dashboard(request):
    tasks = Task.objects.select_related('priority', 'category').order_by('-created_at')[:10]
    total_tasks = Task.objects.count()
    completed = Task.objects.filter(status='Completed').count()
    in_progress = Task.objects.filter(status='In Progress').count()
    pending = Task.objects.filter(status='Pending').count()

    category_progress = []
    for cat in Category.objects.all():
        cat_tasks = Task.objects.filter(category=cat)
        total = cat_tasks.count()
        done = cat_tasks.filter(status='Completed').count()
        percent = round((done / total) * 100) if total > 0 else 0
        category_progress.append({'name': cat.name, 'percent': percent})

    upcoming = Task.objects.filter(
        deadline__gte=timezone.now()
    ).exclude(status='Completed').order_by('deadline')[:4]

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed': completed,
        'in_progress': in_progress,
        'pending': pending,
        'category_progress': category_progress,
        'upcoming': upcoming,
    }
    return render(request, 'tasks/dashboard.html', context)


def task_list(request):
    tasks = Task.objects.select_related('priority', 'category').order_by('-created_at')
    status_filter = request.GET.get('status', '')
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    search = request.GET.get('search', '')
    if search:
        tasks = tasks.filter(title__icontains=search)
    context = {
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
        'status_filter': status_filter,
        'search': search,
    }
    return render(request, 'tasks/task_list.html', context)


def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    subtasks = task.subtask_set.all()
    notes = task.note_set.all()
    context = {
        'task': task,
        'subtasks': subtasks,
        'notes': notes,
        'total_tasks': Task.objects.count(),
    }
    return render(request, 'tasks/task_detail.html', context)


def task_add(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    context = {
        'form': form,
        'title': 'Add New Task',
        'total_tasks': Task.objects.count(),
    }
    return render(request, 'tasks/task_form.html', context)


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    form = TaskForm(instance=task)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=pk)
    context = {
        'form': form,
        'task': task,
        'title': 'Edit Task',
        'total_tasks': Task.objects.count(),
    }
    return render(request, 'tasks/task_form.html', context)


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    context = {
        'task': task,
        'total_tasks': Task.objects.count(),
    }
    return render(request, 'tasks/task_confirm_delete.html', context)