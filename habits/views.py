from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPagination
from habits.permissions import IsOwnerOrReadOnlyPublic
from habits.serializers import HabitPublicSerializer, HabitSerializer


class HabitListCreateAPIView(generics.ListCreateAPIView):
    """Список привычек текущего пользователя + создание."""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Получение / редактирование / удаление своей привычки."""

    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnlyPublic)

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)


class HabitPublicListAPIView(generics.ListAPIView):
    """Список публичных привычек (только чтение)."""

    serializer_class = HabitPublicSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = HabitPagination

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
