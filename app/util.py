
from .models import User


def get_user(id):
    try:
        user = User.objects.get_by_id(id).first()
    except:
        user = None
    return user