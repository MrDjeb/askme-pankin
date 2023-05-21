from django.contrib import admin
from django.urls import path
from askme import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('settings/', views.settings, name="settings"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('tag/<str:tag_title>/', views.tag, name="tag"),
    path('ask/', views.ask, name="ask"),
]