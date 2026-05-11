from django.urls import path
from . import views

app_name = 'summaries'

urlpatterns = [
    path('project/<int:project_pk>/create/', views.summary_create, name='create'),
    path('<int:pk>/editor/', views.summary_editor, name='editor'),
    path('<int:pk>/delete/', views.summary_delete, name='delete'),
    path('project/<int:project_pk>/ai-generate/', views.ai_generate_summary, name='ai_generate'),
]
