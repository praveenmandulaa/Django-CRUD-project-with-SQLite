from django.contrib import admin
from django.urls import path, include
from tasks import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('tasks', views.TaskViewSet, basename='api-task')
urlpatterns = [path('admin/', admin.site.urls), path('accounts/', include('django.contrib.auth.urls')), path('signup/', views.signup, name='signup'), path('', views.dashboard, name='dashboard'), path('tasks/new/', views.TaskCreate.as_view(), name='task-create'), path('tasks/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'), path('tasks/<int:pk>/edit/', views.TaskUpdate.as_view(), name='task-update'), path('tasks/<int:pk>/delete/', views.TaskDelete.as_view(), name='task-delete'), path('api/', include(router.urls))]
