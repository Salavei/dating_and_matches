from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Photo
from .serializers import PhotoSerializer


class PhotoListAPIView(APIView):
    """
    API view for retrieving a list of photos.

    This view allows GET requests to fetch all photos from the database.
    The retrieved photos are serialized using the PhotoSerializer.

    Methods:
    - get: Handles GET requests and returns a response with serialized photo data.

    """

    def get(self, request):
        """
        Handle GET requests to retrieve a list of photos.

        Returns:
        - Response object containing serialized photo data.

        """
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many=True, context={"request": request})
        return Response(serializer.data)
