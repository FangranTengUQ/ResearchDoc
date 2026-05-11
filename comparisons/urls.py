from django.urls import path
from . import views

app_name = 'comparisons'

urlpatterns = [
    path('project/<int:project_pk>/create/', views.comparison_create, name='create'),
    path('<int:pk>/editor/', views.comparison_editor, name='editor'),
    path('<int:pk>/delete/', views.comparison_delete, name='delete'),
    path('project/<int:project_pk>/ai-generate/', views.ai_generate_comparison, name='ai_generate'),
]
