from rest_framework import serializers
from .models import User, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class TaskSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(is_deleted=False), source='assigned_to', write_only=True, allow_null=True
    )

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'created_by', 'assigned_to', 'assigned_to_id', 'created_at', 'updated_at']