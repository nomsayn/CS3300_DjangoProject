from django.urls import path
from . import views

urlpatterns = [
# path function defines a url pattern
# '' is empty to represent based path to app
# views.index is the function defined in views.py
# name='index' parameter is to dynamically create url
# example in html <a href="{% url 'index' %}">Home</a>.
path('', views.index, name='index'),
path('students/', views.StudentListView.as_view(), name= 'students'),
path('student/<int:pk>', views.StudentDetailView.as_view(), name='student-detail'),
path('portfolio/<int:pk>', views.PortfolioDetailView.as_view(), name='portfolio-detail'),
path('portfolio/update_portfolio/<int:portfolio_id>/', views.updatePortfolio, name='update_portfolio'),
path('projects/', views.ProjectListView.as_view(), name= 'projects'),
path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
path('portfolio/<int:portfolio_id>/create_project/', views.createProject, name='create_project'),
path('portfolio/<int:portfolio_id>/update_project/<int:project_id>/', views.updateProject, name='update_project'),
path('DeleteProjectConfirm/<int:project_id>/delete/', views.deleteProject, name='delete_project'),
path('DeleteProjectConfirm/<int:pk>', views.DeleteProjectConfirmView.as_view(), name='delete-project-confirm'),
]
