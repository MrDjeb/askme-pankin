from django.contrib import admin
from django.urls import path
from askme import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.log_in, name="login"),
    path('logout/', views.log_out, name='logout'),
    path('signup/', views.signup, name="signup"),
    path('settings/', views.settings, name="settings"),
    path('hot/', views.hot, name="hot"),
    path('question/<int:question_id>/', views.question, name="question"),
    path('tag/<str:tag_title>/', views.tag, name="tag"),
    path('ask/', views.ask, name="ask"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)