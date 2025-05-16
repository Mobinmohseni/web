from django.urls import path
from . import views

urlpatterns = [
    path('', views.resume_view, name='resume'),
    path('<int:user_id>/', views.resume_view, name='resume_user'),
]



