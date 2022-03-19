from server.utils.base import base_utils
from django.conf import settings


def post_image_path(instance, filename):
    unique_name = base_utils.generate_unique_name(filename)
    file = base_utils.change_suffix(unique_name, 'png')
    return 'post/img/' + str(instance.id) + "/" + file


def post_default_image():
    post_default_image = getattr(settings, 'POST_DEFAULT_IMAGE', None)
    if not post_default_image:
        raise KeyError("POST_DEFAULT_IMAGE is not defined in settings")
    return post_default_image
