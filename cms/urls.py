from django.urls import path
from .views import PageView

app_name = 'cms'

urlpatterns = [
    path('pages/<str:page_slug>', PageView.as_view(), name='page'),

]