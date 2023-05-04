from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from todo.models import TodoListModel, UserModel
from todo.serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated


class TodoView(ModelViewSet):
    serializer_class = TodoSerializer
    queryset = TodoListModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        user = UserModel.objects.get(id=self.request.user.id)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = TodoListModel.objects.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = TodoListModel.objects.get(pk=kwargs.get('pk'))
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


