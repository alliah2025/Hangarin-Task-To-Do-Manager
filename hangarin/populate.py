import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin.settings')
django.setup()

from faker import Faker
from django.utils import timezone
from tasks.models import Category, Priority, Task, Note, SubTask

fake = Faker()

#Priorities
priorities = ['High', 'Medium', 'Low', 'Critical', 'Optional']
for p in priorities:
    Priority.objects.get_or_create(name=p)
print("Priorities created")

#Categories
categories = ['Work', 'School', 'Personal', 'Finance', 'Projects']
for c in categories:
    Category.objects.get_or_create(name=c)
print("Categories created")

#Tasks
priority_list = list(Priority.objects.all())
category_list = list(Category.objects.all())

for _ in range(10):
    task = Task.objects.create(
        title=fake.sentence(nb_words=5),
        description=fake.paragraph(nb_sentences=3),
        deadline=timezone.make_aware(fake.date_time_this_month()),
        status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
        priority=fake.random_element(elements=priority_list),
        category=fake.random_element(elements=category_list),
    )

    #Notes for each Task
    for _ in range(2):
        Note.objects.create(
            task=task,
            content=fake.paragraph(nb_sentences=2),
        )

    #SubTasks for each Task
    for _ in range(3):
        SubTask.objects.create(
            parent_task=task,
            title=fake.sentence(nb_words=4),
            status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
        )

print("Tasks, Notes, and SubTasks created")