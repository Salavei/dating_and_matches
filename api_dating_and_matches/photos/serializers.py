from rest_framework import serializers
from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Photo model.

    This serializer is used to convert Photo model instances into a serialized format,
    which can be easily rendered into JSON or other content types.
    It includes a custom field 'photo' that returns the absolute URL of the photo.

    Fields:
    - id: The ID of the photo.
    - name: The name of the photo.
    - photo: The absolute URL of the photo.

    Methods:
    - get_photo_url: Custom method to retrieve the absolute URL of the photo.

    """

    photo = serializers.SerializerMethodField('get_photo_url')

    class Meta:
        model = Photo
        fields = ('id', 'name', 'photo')

    def get_photo_url(self, obj):
        """
        Get the absolute URL of the photo.

        Parameters:
        - obj: The Photo model instance.

        Returns:
        - The absolute URL of the photo.

        """
        request = self.context.get("request")
        return request.build_absolute_uri(obj.photo.url)
