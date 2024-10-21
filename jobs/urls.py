from django.urls import path
from . import views

urlpatterns = [
    path('run_job_retrieval/', views.run_job_retrieval, name='run_job_retrieval'),
    path('download_jobs/', views.download_jobs, name='download_jobs'),
]
