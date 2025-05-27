from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project-delete'),
] 