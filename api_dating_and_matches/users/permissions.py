from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    Custom permission class to check if the user is the owner of an object.

    Methods:
        has_object_permission: Checks if the user is the owner of the object.

    Example Usage:
        class MyView(APIView):
            permission_classes = [IsOwner]

            def get(self, request, pk):
                # Retrieve the object
                obj = MyModel.objects.get(pk=pk)
                # Check if the user is the owner of the object
                if not self.request.user.has_object_permission(self.request, self, obj):
                    return Response({'message': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
                # Perform further actions for the authorized user
                ...
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if the user is the owner of the object.

        Args:
            request (HttpRequest): The request object.
            view (APIView): The view object.
            obj: The object to check ownership against.

        Returns:
            bool: True if the user is the owner, False otherwise.
        """
        return obj == request.user
