from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class SignUpTests(TestCase):

    def test_beginner_rating_exists(self):
        user = User.objects.create_staffuser(
                'temporary',
                'temporary@gmail.com',
                'temporary')
        rating = user.rating.latest()

        self.assertIsNotNone(rating)
        self.assertEqual(rating.league,
                         rating._meta.model.LEAGUE.BEGINNER)

    def test_beginner_rating_is_100(self):
        user = User.objects.create_staffuser(
                'temporary',
                'temporary@gmail.com',
                'temporary')
        rating = user.rating.latest()
        beginner_rating = rating.beginner_rating.first()

        self.assertEqual(beginner_rating.value, 100)
