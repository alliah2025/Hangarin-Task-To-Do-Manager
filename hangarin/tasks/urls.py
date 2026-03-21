from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
    path('tasks/add/', views.TaskAddView.as_view(), name='task_add'),
    path('tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('tasks/<int:pk>/edit/', views.TaskEditView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # Notes
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/add/', views.NoteAddView.as_view(), name='note_add'),
    path('notes/<int:pk>/edit/', views.NoteEditView.as_view(), name='note_edit'),
    path('notes/<int:pk>/confirm-delete/', views.NoteConfirmDeleteView.as_view(), name='note_confirm_delete'),

    # Subtasks
    path('subtasks/', views.SubtaskListView.as_view(), name='subtask_list'),
    path('subtasks/add/', views.SubtaskAddView.as_view(), name='subtask_add'),
    path('subtasks/<int:pk>/edit/', views.SubtaskEditView.as_view(), name='subtask_edit'),
    path('subtasks/<int:pk>/confirm-delete/', views.SubtaskConfirmDeleteView.as_view(), name='subtask_confirm_delete'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryAddView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryEditView.as_view(), name='category_edit'),
    path('categories/<int:pk>/confirm-delete/', views.CategoryConfirmDeleteView.as_view(), name='category_confirm_delete'),

    # Priorities
    path('priorities/', views.PriorityListView.as_view(), name='priority_list'),
    path('priorities/add/', views.PriorityAddView.as_view(), name='priority_add'),
    path('priorities/<int:pk>/edit/', views.PriorityEditView.as_view(), name='priority_edit'),
    path('priorities/<int:pk>/confirm-delete/', views.PriorityConfirmDeleteView.as_view(), name='priority_confirm_delete'),
]