import hashlib
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from photos.models import Photo


def calculate_grades_and_create_cache(request):
    """
    Calculate grades and create cache based on the provided ratings.

    Args:
        request (dict): Dictionary containing photo ratings.

    Returns:
        str: Final hash generated from the photo ratings.

    Raises:
        Response: If the number of photo ratings is invalid or if a rating value is invalid.

    Example Usage:
        ratings = {
            'photo_1': 5,
            'photo_2': 4,
            'photo_3': 3,
        }
        final_hash = calculate_grades_and_create_cache(ratings)
    """
    photo_keys = [k for k in request if k.startswith("photo_")]
    if len(photo_keys) != Photo.objects.all().count():
        return Response({'message': 'Invalid number of photo ratings'},
                        status=status.HTTP_400_BAD_REQUEST)

    hash_for_match = ''
    for photo_id in photo_keys:
        rating = request[photo_id]
        get_photo_id = int(photo_id.replace("photo_", ""))
        #  get_object_or_404 -> "detail": "Not found."
        get_object_or_404(Photo, id=get_photo_id)
        if not (1 <= int(rating) <= 5):
            return Response({'message': "Invalid rating value"}, status=status.HTTP_400_BAD_REQUEST)

        hash_for_match += hashlib.sha256(photo_id.encode()).hexdigest() + hashlib.sha256(
            str(rating).encode()).hexdigest()

    final_hash = hashlib.sha256(hash_for_match.encode()).hexdigest()
    return final_hash
