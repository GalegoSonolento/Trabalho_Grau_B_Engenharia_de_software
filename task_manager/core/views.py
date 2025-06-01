from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import User, Task
from .serializers import UserSerializer, TaskSerializer
import logging

logger = logging.getLogger(__name__)

class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User created: {serializer.data['username']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"User creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            user = User.objects.get(id=id, is_deleted=False)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            logger.warning(f"User not found: id={id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            user = User.objects.get(id=id, is_deleted=False)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User updated: id={id}")
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.warning(f"User not found: id={id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id, is_deleted=False)
            user.soft_delete()
            logger.info(f"User soft deleted: id={id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            logger.warning(f"User not found: id={id}")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            logger.info(f"Task created: {serializer.data['title']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Task creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Task.DoesNotExist:
            logger.warning(f"Task not found: id={id}")
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Task updated: id={id}")
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Task.DoesNotExist:
            logger.warning(f"Task not found: id={id}")
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            logger.info(f"Task deleted: id={id}")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            logger.warning(f"Task not found: id={id}")
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

class TaskListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assigned_to = request.query_params.get('assignedTo')
        if assigned_to:
            tasks = Task.objects.filter(assigned_to_id=assigned_to)
        else:
            tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)