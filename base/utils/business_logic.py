from base.models import User


def match_create_user(request):
    tmp = 0
    B = [5] * 7
    for i in range(1, 7 + 1):
        tmp += (B[i - 1] - int(request.get(f'contact{i}'))) ** 2
    return tmp


def show_match_people(user):
    people = User.objects.filter(likes__gte=(user.likes - 20), likes__lte=(user.likes + 20)).exclude(email=user.email)
    return people
