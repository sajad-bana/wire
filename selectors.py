from django.contrib.contenttypes.models import ContentType
from .models import WireProcessRequest

class WireProcessRequestSelector:
    def __init__(self, user):
        """
        Initializes the selector with the request user.
        """
        self.user = user

    def get_request_by_object(self, content_type_name: str, object_id: int):
        """
        Retrieves a workflow request based on the object it's linked to.
        """
        try:
            content_type = ContentType.objects.get(model=content_type_name.lower())
            return WireProcessRequest.objects.filter(
                content_type=content_type,
                object_id=object_id
            )
        except ContentType.DoesNotExist:
            return WireProcessRequest.objects.none()

