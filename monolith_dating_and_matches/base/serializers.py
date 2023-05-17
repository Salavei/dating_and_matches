from rest_framework.serializers import ModelSerializer
from dating_and_matches.base.forms import MyUserCreationForm
from dating_and_matches.base.models import Photo

class MyUserCreationSerializer(ModelSerializer):
    """
    Serializer for the MyUserCreationForm model.
    """
    class Meta:
        model = MyUserCreationForm
        fields = '__all__'

class PhotoSerializer(ModelSerializer):
    """
    Serializer for the Photo model.
    """
    class Meta:
        model = Photo
        fields = '__all__'
