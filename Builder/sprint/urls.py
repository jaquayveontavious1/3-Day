from django.urls import path
from . import views
from .views import CustomLogoutView
from django.contrib.auth import views as auth_views
from .views import leaderboard_view
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('create-sprint/', views.create_sprint_view, name='create'),
    ##path('update-goal/<int:goal_id>/', views.update_goal, name='update'),
    path('update-my-sprint/', views.update_my_sprint, name='update_my_sprint'),
    path('sprint-history/', views.sprint_history_view, name='sprint_history'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('logout/', CustomLogoutView.as_view(next_page='login'), name='logout'),
    

]