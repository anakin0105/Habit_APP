from datetime import time

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.other = User.objects.create_user(
            email="other@example.com", password="testpass123"
        )
        self.pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(20, 0),
            action="Принять ванну",
            is_pleasant=True,
            execution_time=60,
            periodicity=1,
        )
        self.habit = Habit.objects.create(
            user=self.user,
            place="Улица",
            time=time(8, 0),
            action="Прогулка",
            is_pleasant=False,
            reward="Кофе",
            execution_time=90,
            periodicity=1,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_list_own_habits(self):
        url = reverse("habits:habit-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_habit(self):
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Офис",
            "time": "09:00:00",
            "action": "Стакан воды",
            "is_pleasant": False,
            "reward": "Улыбка",
            "periodicity": 1,
            "execution_time": 30,
            "is_public": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.filter(user=self.user).count(), 3)

    def test_create_habit_with_related(self):
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Дом",
            "time": "19:00:00",
            "action": "Зарядка",
            "is_pleasant": False,
            "related_habit": self.pleasant.pk,
            "periodicity": 1,
            "execution_time": 100,
            "is_public": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cannot_set_reward_and_related(self):
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Дом",
            "time": "19:00:00",
            "action": "Зарядка",
            "is_pleasant": False,
            "reward": "Торт",
            "related_habit": self.pleasant.pk,
            "periodicity": 1,
            "execution_time": 60,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_execution_time_limit(self):
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Долгое действие",
            "is_pleasant": False,
            "reward": "Отдых",
            "periodicity": 1,
            "execution_time": 200,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_periodicity_limit(self):
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Дом",
            "time": "10:00:00",
            "action": "Редкая привычка",
            "is_pleasant": False,
            "reward": "Отдых",
            "periodicity": 14,
            "execution_time": 30,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_pleasant_cannot_have_reward(self):
        url = reverse("habits:habit-list-create")
        data = {
            "place": "Дом",
            "time": "21:00:00",
            "action": "Чтение",
            "is_pleasant": True,
            "reward": "Чай",
            "periodicity": 1,
            "execution_time": 60,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_own_habit(self):
        url = reverse("habits:habit-detail", args=[self.habit.pk])
        response = self.client.patch(url, {"action": "Бег"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.action, "Бег")

    def test_delete_own_habit(self):
        url = reverse("habits:habit-detail", args=[self.habit.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(pk=self.habit.pk).exists())

    def test_cannot_access_other_user_habit(self):
        other_habit = Habit.objects.create(
            user=self.other,
            place="Парк",
            time=time(7, 0),
            action="Йога",
            execution_time=60,
            periodicity=1,
        )
        url = reverse("habits:habit-detail", args=[other_habit.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_list(self):
        url = reverse("habits:habit-public-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_pagination(self):
        for i in range(6):
            Habit.objects.create(
                user=self.user,
                place="Дом",
                time=time(10, i),
                action=f"Habit {i}",
                execution_time=30,
                periodicity=1,
            )
        url = reverse("habits:habit-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 5)
