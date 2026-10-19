from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.project_gallery, name='gallery'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('project/create/', views.project_create, name='project_create'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
]
