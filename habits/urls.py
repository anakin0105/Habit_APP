from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (
    HabitListCreateAPIView,
    HabitPublicListAPIView,
    HabitRetrieveUpdateDestroyAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("", HabitListCreateAPIView.as_view(), name="habit-list-create"),
    path(
        "<int:pk>/",
        HabitRetrieveUpdateDestroyAPIView.as_view(),
        name="habit-detail",
    ),
    path("public/", HabitPublicListAPIView.as_view(), name="habit-public-list"),
]
