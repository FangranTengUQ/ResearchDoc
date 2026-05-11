from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('project/<int:project_pk>/add/', views.resource_create, name='create'),
    path('<int:pk>/edit/', views.resource_edit, name='edit'),
    path('<int:pk>/delete/', views.resource_delete, name='delete'),
]
