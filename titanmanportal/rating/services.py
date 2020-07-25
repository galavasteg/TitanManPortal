from rating.models import Rating, Beginner


def rating_save_callback(sender: type(Rating), instance: Rating,
                         created: bool, *args, **kwargs):
    rating = instance
    if created:
        if rating.league == Rating.LEAGUE.BEGINNER:
            new_rating_detail = Beginner(
                    rating=rating, value=100)
            rating.beginner_rating.set(
                [new_rating_detail], bulk=False)
