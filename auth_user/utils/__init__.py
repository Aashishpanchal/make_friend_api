from utility.base import base_utils
from django.conf import settings


def user_image_path(instance, filename):
    unique_name = base_utils.generate_unique_name(filename)
    file = base_utils.change_suffix(unique_name, 'png')
    return 'user/profile/img/' + instance.username + str(
        instance.id) + "/" + file


def user_default_image():
    user_default_profile_image = getattr(settings,
                                         'USER_DEFAULT_PROFILE_IMAGE', None)
    if not user_default_profile_image:
        raise KeyError("USER_DEFAULT_PROFILE_IMAGE is not defined in settings")
    return user_default_profile_image


def user_back_cover_image_path(instance, filename):
    unique_name = base_utils.generate_unique_name(filename)
    file = base_utils.change_suffix(unique_name, 'png')
    return 'user/backCover/img/' + instance.username + str(
        instance.id) + "/" + file


def user_default_back_cover_image():
    user_default_back_cover_image = getattr(settings,
                                            'USER_DEFAULT_BACK_COVER_IMAGE', None)
    if not user_default_back_cover_image:
        raise KeyError(
            "USER_DEFAULT_BACK_COVER_IMAGE is not defined in settings")
    return user_default_back_cover_image
