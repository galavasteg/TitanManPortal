from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from rating.models import Rating, BeginnerRatingDetail


User = get_user_model()


class RatingService:

    @staticmethod
    def post_rating_save(sender: type(Rating), instance: Rating,
                         created: bool, *args, **kwargs):
        rating = instance
        if created:
            if rating.league == Rating.LEAGUE.BEGINNER:
                new_rating_detail = BeginnerRatingDetail(
                        rating=rating, current_rating=100)
                rating.beginner_rating.set([new_rating_detail], bulk=False)
