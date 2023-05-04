from django.urls import path

from .views import TodoView


urlpatterns = [
    path('add-todolist', TodoView.as_view({'post': 'create'}), name='addtodo'),
    path('update-todo/<int:pk>', TodoView.as_view({'put': 'update'}), name='updatetodo'),
    path('delete-todo/<int:pk>', TodoView.as_view({'delete': 'destroy'}), name='deletetodo'),
]
