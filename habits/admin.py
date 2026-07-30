from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "action",
        "user",
        "time",
        "place",
        "is_pleasant",
        "is_public",
        "periodicity",
        "execution_time",
    )
    list_filter = ("is_pleasant", "is_public", "periodicity")
    search_fields = ("action", "place", "user__email")
    raw_id_fields = ("user", "related_habit")
