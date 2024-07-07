# views.py

from rest_framework import generics, status
from rest_framework.response import Response
from ..models import ToDo
from ..serializers import ToDoSerializer
from django.core.cache import cache
from django.shortcuts import get_object_or_404

class ToDoListCreate(generics.ListCreateAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer

    def get(self, request, *args, **kwargs):
        todos = cache.get("todos")
        if not todos:
            todos = ToDo.objects.all()
            cache.set("todos", todos, timeout=60 * 15)  
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ToDoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.delete("todos")  # Invalidate the list cache
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = ToDo.objects.all()
    serializer_class = ToDoSerializer

    def get(self, request, *args, **kwargs):
        todo_id = kwargs.get('pk')
        todo = cache.get(f'todo_{todo_id}')
        if not todo:
            todo = get_object_or_404(ToDo, pk=todo_id)
            serializer = ToDoSerializer(todo)
            cache.set(f'todo_{todo_id}', serializer.data, timeout=60*15)  
        else:
            serializer = ToDoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        todo_id = kwargs.get("pk")
        try:
            todo = self.get_object()
        except ToDo.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ToDoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            cache.set(f"todo_{todo_id}", serializer.data, timeout=60 * 15)
            cache.delete("todos")  # Invalidate the list cache
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        todo_id = kwargs.get("pk")
        try:
            todo = self.get_object()
        except ToDo.DoesNotExist:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        todo.delete()
        cache.delete(f"todo_{todo_id}")
        cache.delete("todos")  # Invalidate the list cache
        return Response({"message" : "Todo deleted successfully"},status=status.HTTP_204_NO_CONTENT)
