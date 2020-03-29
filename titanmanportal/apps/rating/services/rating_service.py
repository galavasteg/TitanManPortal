from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from periods.services import PeriodService
from rating.models import Rating, BeginnerRatingDetail


User = get_user_model()


class RatingService:
    
    @staticmethod
    def get_current_member_rating(rating: Rating):
        member = rating.member
        current_user_rating = PeriodService.get_last_user_period(member)
        return current_user_rating

    @staticmethod
    def post_rating_save(sender: type(Rating), instance: Rating,
                         created: bool, *args, **kwargs):
        rating = instance
        if created:
            if rating.league == Rating.LEAGUE.BEGINNER:
                current_rating = RatingService.get_current_member_rating(rating)
                new_rating_detail = BeginnerRatingDetail(
                        current_rating=current_rating)
                rating.beginner_rating.add(new_rating_detail)
                rating.save()
