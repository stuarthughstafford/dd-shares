from django.urls import path

from . import views

app_name = 'myapp'
urlpatterns = [
    # new page
    path('', views.index, name='index'),
    path('test.html', views.test, name='test'),
]