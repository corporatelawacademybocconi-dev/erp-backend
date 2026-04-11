from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import timedelta
from .models import Goal, Habit, HabitLog
from .serializers import GoalSerializer, HabitSerializer, HabitLogSerializer


class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'target_date', 'progress']

    def get_queryset(self):
        return Goal.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cadence', 'goal']
    ordering_fields = ['created_at', 'streak']

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        habit = self.get_object()
        today = timezone.now().date()

        log, created = HabitLog.objects.get_or_create(
            habit=habit,
            date=today,
            defaults={'completed': True}
        )

        if not created:
            log.completed = not log.completed
            log.save()

        habit.completed_today = log.completed

        if log.completed:
            streak = 0
            check_date = today
            while HabitLog.objects.filter(habit=habit, date=check_date, completed=True).exists():
                streak += 1
                check_date -= timedelta(days=1)
            habit.streak = streak
        else:
            streak = 0
            check_date = today - timedelta(days=1)
            while HabitLog.objects.filter(habit=habit, date=check_date, completed=True).exists():
                streak += 1
                check_date -= timedelta(days=1)
            habit.streak = streak

        habit.save()
        return Response(HabitSerializer(habit).data)


class HabitLogViewSet(viewsets.ModelViewSet):
    serializer_class = HabitLogSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['habit', 'completed']
    ordering_fields = ['date']

    def get_queryset(self):
        return HabitLog.objects.filter(habit__owner=self.request.user)