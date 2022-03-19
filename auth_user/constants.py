from django.utils.translation import gettext as _


class Messages(object):
    PASSWORD_MISMATCH_ERROR = _("The two password fields didn't match.")
    CANNOT_CREATE_USER = _("This user already exists.")
    NO_ACTIVE_ACCOUNT: str = _(
        'No active account found with the given credentials.')
    NO_USER_FOUND: str = _('No User found with the given credentials.')
    INCORRECT_PASSWORD: str = _(
        'Incorrect password please give correct password')
    BAD_TOKEN: str = _('Token is expired or Invalid')
