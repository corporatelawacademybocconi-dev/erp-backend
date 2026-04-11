from rest_framework import serializers
from .models import Project, Task, ProjectHistory


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ProjectHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectHistory
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    task_count = serializers.SerializerMethodField()
    history = ProjectHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_task_count(self, obj):
        return obj.tasks.count()