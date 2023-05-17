from base.models import User, Photo


def match_create_user(request):
    """
    Calculates a match score for the user based on their photo evaluations.

    Args:
        request: The HTTP request object containing the user's photo evaluations.

    Returns:
        The match score for the user, or False if there is an invalid evaluation.
    """
    count_photo = Photo.objects.all().count()
    tmp = 0
    data_for_evaluation = [5] * count_photo
    for i in range(1, count_photo + 1):
        if request.get(f'contact{i}') is not None:
            tmp += (data_for_evaluation[i - 1] - int(request.get(f'contact{i}'))) ** 2
        else:
            return False
    return tmp


def show_match_people(user):
    """
    Retrieves a list of people who match the given user's preferences.

    Args:
        user: The user object for whom to find matching people.

    Returns:
        A queryset of User objects representing the matching people.
    """
    people = User.objects.filter(likes__gte=(user.likes - 20), likes__lte=(user.likes + 20)).exclude(email=user.email)
    return people
