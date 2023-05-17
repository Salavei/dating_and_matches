from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ratings.models import MatchGroup


class MatchesView(APIView):
    """
    API view to retrieve a list of matches for the authenticated user.

    Requires authentication to access.

    Available query parameters for filtering and sorting:
    - sort_by: Sort the matches by a specific attribute (e.g., 'birthday').
    - gender: Filter matches by gender.
    - birthday_min: Filter matches by minimum birthday.
    - birthday_max: Filter matches by maximum birthday.

    Returns a response with the list of matches and the authenticated user's details.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Retrieve the match group for the authenticated user
        group = MatchGroup.objects.filter(users=request.user).first()

        if group:
            all_users_in_your_group = group.users.all()

            # Sorting options
            sort_by = request.query_params.get('sort_by', None)
            gender = request.query_params.get('gender', None)
            birthday_min = request.query_params.get('birthday_min', None)
            birthday_max = request.query_params.get('birthday_max', None)

            # Filter users by gender
            if gender:
                all_users_in_your_group = all_users_in_your_group.filter(gender=gender)

            # Filter users by birthday day range
            if birthday_min and birthday_max:
                all_users_in_your_group = all_users_in_your_group.filter(birthday__gte=birthday_min,
                                                                         birthday__lte=birthday_max)

            # Sort users by age
            if sort_by == 'birthday':
                all_users_in_your_group = all_users_in_your_group.order_by('-birthday')

            all_users = all_users_in_your_group.values('id', 'username', 'birthday',
                                                       'gender', 'avatar', 'bio', 'hash')

            # Prepare response data
            data = {
                'id': request.user.id,
                'email': request.user.email,
                'username': request.user.username,
                'birthday': request.user.birthday,
                'gender': request.user.gender,
                'avatar': request.user.avatar.url,
                'bio': request.user.bio,
                'all_users_in_your_group': all_users
            }
            return Response(data)
        else:
            return Response({'message': 'Some error'}, status=status.HTTP_400_BAD_REQUEST)
