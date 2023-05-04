from rest_framework import serializers
from .models import TodoListModel


class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TodoListModel
        fields = ('created', 'title', 'description', 'status', 'deadline')
