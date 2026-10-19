from django.urls import path
from . import views

app_name = 'evaluations'

urlpatterns = [
    path('dashboard/', views.supervisor_dashboard, name='dashboard'),
    path('review/<int:project_id>/', views.evaluate_project, name='evaluate_project'),
]
