from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Task, Category, Priority, Note, SubTask
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

def note_list(request):
    notes = Note.objects.select_related('task').order_by('-created_at')
    tasks = Task.objects.all()

    task_filter = request.GET.get('task', '')
    sort = request.GET.get('sort', 'newest')

    if task_filter:
        notes = notes.filter(task_id=task_filter)
    if sort == 'oldest':
        notes = notes.order_by('created_at')
    else:
        notes = notes.order_by('-created_at')

    return render(request, 'tasks/note_list.html', {
        'notes': notes,
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
        'task_filter': task_filter,
        'sort': sort,
    })

def note_add(request):
    if request.method == 'POST':
        task_id = request.POST.get('task')
        content = request.POST.get('content')
        if task_id and content:
            Note.objects.create(task_id=task_id, content=content)
        return redirect('note_list')
    tasks = Task.objects.all()
    return render(request, 'tasks/note_form.html', {
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
    })

def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.delete()
    return redirect('note_list')

def subtask_list(request):
    subtasks = SubTask.objects.select_related('parent_task').order_by('-id')
    return render(request, 'tasks/subtask_list.html', {
        'subtasks': subtasks,
        'total_tasks': Task.objects.count(),
    })

def subtask_add(request):
    if request.method == 'POST':
        task_id = request.POST.get('task')
        title = request.POST.get('title')
        status = request.POST.get('status', 'Pending')
        if task_id and title:
            SubTask.objects.create(parent_task_id=task_id, title=title, status=status)
        return redirect('subtask_list')
    tasks = Task.objects.all()
    return render(request, 'tasks/subtask_form.html', {
        'tasks': tasks,
        'total_tasks': Task.objects.count(),
    })

def subtask_delete(request, pk):
    subtask = get_object_or_404(SubTask, pk=pk)
    if request.method == 'POST':
        subtask.delete()
    return redirect('subtask_list')

def category_list(request):
    categories = Category.objects.all()
    cat_data = []
    for cat in categories:
        total = Task.objects.filter(category=cat).count()
        done = Task.objects.filter(category=cat, status='Completed').count()
        percent = round((done / total) * 100) if total > 0 else 0
        cat_data.append({'obj': cat, 'total': total, 'done': done, 'percent': percent})
    return render(request, 'tasks/category_list.html', {
        'categories': cat_data,
        'total_tasks': Task.objects.count(),
    })

def category_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
        return redirect('category_list')
    return render(request, 'tasks/category_form.html', {
        'total_tasks': Task.objects.count(),
    })

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
    return redirect('category_list')