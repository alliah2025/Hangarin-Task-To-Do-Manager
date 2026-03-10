from django.shortcuts import render
from django.utils import timezone
from .models import Task, Category

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
    context = {
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
    }
    return render(request, 'tasks/task_list.html', context)