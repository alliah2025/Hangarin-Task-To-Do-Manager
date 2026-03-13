from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/add/', views.task_add, name='task_add'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Notes
    path('notes/', views.note_list, name='note_list'),
    path('notes/add/', views.note_add, name='note_add'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/confirm-delete/', views.note_confirm_delete, name='note_confirm_delete'),

    # Subtasks
    path('subtasks/', views.subtask_list, name='subtask_list'),
    path('subtasks/add/', views.subtask_add, name='subtask_add'),
    path('subtasks/<int:pk>/edit/', views.subtask_edit, name='subtask_edit'),
    path('subtasks/<int:pk>/confirm-delete/', views.subtask_confirm_delete, name='subtask_confirm_delete'),

    # Categories
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_add, name='category_add'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]