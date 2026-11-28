from .models import UserStamp

def give_stamp(user, place):
    stamp, created = UserStamp.objects.get_or_create(user=user, place=place)
    return stamp, created