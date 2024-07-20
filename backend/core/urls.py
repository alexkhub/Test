from django.urls import path

from .views import *

urlpatterns = [
    path('new_file/', FileCreateView.as_view(), name='new_file'),
    path('list_file/', FileListView.as_view(), name='list_file'),
    path('update_file/<int:id>/', FileRetrieveUpdateDestroyView.as_view(), name='update_file')

]