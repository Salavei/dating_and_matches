from base.models import User, Photo


def match_create_user(request):
    count_photo = Photo.objects.all().count()
    tmp = 0
    data_for_evaluation = [5] * count_photo
    for i in range(1, count_photo + 1):
        if request.get(f'contact{i}') != None:
            tmp += (data_for_evaluation[i - 1] - int(request.get(f'contact{i}'))) ** 2
        else:
            return False
    return tmp


def show_match_people(user):
    people = User.objects.filter(likes__gte=(user.likes - 20), likes__lte=(user.likes + 20)).exclude(email=user.email)
    return people
