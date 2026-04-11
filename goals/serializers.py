from rest_framework import serializers
from .models import Goal, Habit, HabitLog


class HabitLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = HabitLog
        fields = '__all__'
        read_only_fields = ['created_at']


class HabitSerializer(serializers.ModelSerializer):
    logs = HabitLogSerializer(many=True, read_only=True)
    streak = serializers.IntegerField(read_only=True)

    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ['owner', 'streak', 'created_at', 'updated_at']


class GoalSerializer(serializers.ModelSerializer):
    habits = HabitSerializer(many=True, read_only=True)
    habit_count = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'updated_at']

    def get_habit_count(self, obj):
        return obj.habits.count()