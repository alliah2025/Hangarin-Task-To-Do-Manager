from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.db.models import Q
from django.views.generic.list import ListView

from .models import Task, Category, Priority, Note, SubTask
from .forms import TaskForm

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
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

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('priority', 'category').order_by('-created_at')
        search = self.request.GET.get('search', '')
        status_filter = self.request.GET.get('status', '')
        category_filter = self.request.GET.get('category', '')
        priority_filter = self.request.GET.get('priority', '')

        if search:
            qs = qs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if status_filter:
            qs = qs.filter(status=status_filter)
        if category_filter:
            qs = qs.filter(category_id=category_filter)
        if priority_filter:
            qs = qs.filter(priority_id=priority_filter)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['category_filter'] = self.request.GET.get('category', '')
        context['priority_filter'] = self.request.GET.get('priority', '')
        return context


class TaskDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'subtasks': task.subtask_set.all(),
            'notes': task.note_set.all(),
            'total_tasks': Task.objects.count(),
        })


class TaskAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/task_form.html', {
            'form': TaskForm(),
            'title': 'Add New Task',
            'total_tasks': Task.objects.count(),
        })

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
        return render(request, 'tasks/task_form.html', {
            'form': form,
            'title': 'Add New Task',
            'total_tasks': Task.objects.count(),
        })


class TaskEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_form.html', {
            'form': TaskForm(instance=task),
            'task': task,
            'title': 'Edit Task',
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=pk)
        return render(request, 'tasks/task_form.html', {
            'form': form,
            'task': task,
            'title': 'Edit Task',
            'total_tasks': Task.objects.count(),
        })


class TaskDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'tasks/task_confirm_delete.html', {
            'task': task,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('task_list')

class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'tasks/note_list.html'
    context_object_name = 'notes'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('task').order_by('-created_at')
        search = self.request.GET.get('search', '')
        task_filter = self.request.GET.get('task', '')
        date_filter = self.request.GET.get('date', '')

        if search:
            qs = qs.filter(content__icontains=search)
        if task_filter:
            qs = qs.filter(task_id=task_filter)
        if date_filter:
            qs = qs.filter(created_at__date=date_filter)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()
        context['tasks'] = Task.objects.all()
        context['search'] = self.request.GET.get('search', '')
        context['task_filter'] = self.request.GET.get('task', '')
        context['date_filter'] = self.request.GET.get('date', '')
        return context

class NoteAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/note_form.html', {
            'tasks': Task.objects.all(),
            'total_tasks': Task.objects.count(),
        })

    def post(self, request):
        task_id = request.POST.get('task')
        content = request.POST.get('content')
        if task_id and content:
            Note.objects.create(task_id=task_id, content=content)
        return redirect('note_list')


class NoteEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        return render(request, 'tasks/note_form.html', {
            'tasks': Task.objects.all(),
            'note': note,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        task_id = request.POST.get('task')
        content = request.POST.get('content')
        if task_id and content:
            note.task_id = task_id
            note.content = content
            note.save()
        return redirect('note_list')


class NoteConfirmDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        return render(request, 'tasks/note_confirm_delete.html', {
            'note': note,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return redirect('note_list')

class SubtaskListView(LoginRequiredMixin, ListView):
    model = SubTask
    template_name = 'tasks/subtask_list.html'
    context_object_name = 'subtasks'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('parent_task').order_by('-id')
        task_filter = self.request.GET.get('task', '')
        status_filter = self.request.GET.get('status', '')
        search = self.request.GET.get('search', '')

        if task_filter:
            qs = qs.filter(parent_task_id=task_filter)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if search:
            qs = qs.filter(title__icontains=search)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_tasks'] = Task.objects.count()
        context['tasks'] = Task.objects.all()
        context['task_filter'] = self.request.GET.get('task', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['search'] = self.request.GET.get('search', '')
        return context

class SubtaskAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/subtask_form.html', {
            'tasks': Task.objects.all(),
            'total_tasks': Task.objects.count(),
        })

    def post(self, request):
        task_id = request.POST.get('task')
        title = request.POST.get('title')
        status = request.POST.get('status', 'Pending')
        if task_id and title:
            SubTask.objects.create(parent_task_id=task_id, title=title, status=status)
        return redirect('subtask_list')


class SubtaskEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        return render(request, 'tasks/subtask_form.html', {
            'tasks': Task.objects.all(),
            'subtask': subtask,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        task_id = request.POST.get('task')
        title = request.POST.get('title')
        status = request.POST.get('status', 'Pending')
        if task_id and title:
            subtask.parent_task_id = task_id
            subtask.title = title
            subtask.status = status
            subtask.save()
        return redirect('subtask_list')


class SubtaskConfirmDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        return render(request, 'tasks/subtask_confirm_delete.html', {
            'subtask': subtask,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        subtask = get_object_or_404(SubTask, pk=pk)
        subtask.delete()
        return redirect('subtask_list')

class CategoryListView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search', '')
        categories = Category.objects.all()
        if search:
            categories = categories.filter(name__icontains=search)
        cat_data = []
        for cat in categories:
            total = Task.objects.filter(category=cat).count()
            done = Task.objects.filter(category=cat, status='Completed').count()
            percent = round((done / total) * 100) if total > 0 else 0
            cat_data.append({'obj': cat, 'total': total, 'done': done, 'percent': percent})
        return render(request, 'tasks/category_list.html', {
            'categories': cat_data,
            'total_tasks': Task.objects.count(),
            'search': search,
        })


class CategoryAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/category_form.html', {
            'total_tasks': Task.objects.count(),
        })

    def post(self, request):
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
        return redirect('category_list')


class CategoryEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, 'tasks/category_form.html', {
            'category': category,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
        return redirect('category_list')


class CategoryConfirmDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        return render(request, 'tasks/category_confirm_delete.html', {
            'category': category,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return redirect('category_list')

class PriorityListView(LoginRequiredMixin, View):
    def get(self, request):
        search = request.GET.get('search', '')
        priorities = Priority.objects.all()
        if search:
            priorities = priorities.filter(name__icontains=search)
        pri_data = []
        for pri in priorities:
            total = Task.objects.filter(priority=pri).count()
            done = Task.objects.filter(priority=pri, status='Completed').count()
            percent = round((done / total) * 100) if total > 0 else 0
            pri_data.append({'obj': pri, 'total': total, 'done': done, 'percent': percent})
        return render(request, 'tasks/priority_list.html', {
            'priorities': pri_data,
            'total_tasks': Task.objects.count(),
            'search': search,
        })


class PriorityAddView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tasks/priority_form.html', {
            'total_tasks': Task.objects.count(),
        })

    def post(self, request):
        name = request.POST.get('name')
        if name:
            Priority.objects.create(name=name)
        return redirect('priority_list')


class PriorityEditView(LoginRequiredMixin, View):
    def get(self, request, pk):
        priority = get_object_or_404(Priority, pk=pk)
        return render(request, 'tasks/priority_form.html', {
            'priority': priority,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        priority = get_object_or_404(Priority, pk=pk)
        name = request.POST.get('name')
        if name:
            priority.name = name
            priority.save()
        return redirect('priority_list')


class PriorityConfirmDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        priority = get_object_or_404(Priority, pk=pk)
        return render(request, 'tasks/priority_confirm_delete.html', {
            'priority': priority,
            'total_tasks': Task.objects.count(),
        })

    def post(self, request, pk):
        priority = get_object_or_404(Priority, pk=pk)
        priority.delete()
        return redirect('priority_list')