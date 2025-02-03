from django.urls import path, re_path
from . import views

urlpatterns = [
    path('certificate', views.certificate, name='certificate'),

    path('certificate/<int:task_id>/', views.certificate_task, name='certificate'),

    path('gifts/', views.gifts, name='gifts'),

    path('support/', views.support, name='support'),

    path('portfolio/', views.portfolio, name='portfolio'),

    path('project-defense/', views.project_defense, name='project_defense'),

    path('project-defense/<int:task_id>', views.project_defense_task, name='project_defense'),
]