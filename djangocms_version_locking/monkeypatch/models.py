from django.utils.translation import gettext_lazy as _

from djangocms_moderation import models as moderation_model
from djangocms_moderation.models import version_is_unlocked_for_moderation
from djangocms_moderation.helpers import (
    get_moderated_children_from_placeholder,
)
from djangocms_versioning import constants, models
from djangocms_versioning.helpers import get_latest_draft_version, version_is_locked
from djangocms_versioning.exceptions import ConditionFailed


def _is_version_locked(message):
    def inner(version, user):
        locked_user = version_is_locked(version)
        if locked_user and locked_user != user:
            raise ConditionFailed(message.format(user=locked_user))
    return inner


def _is_draft_version_locked(message):
    def inner(version, user):
        draft_version = get_latest_draft_version(version)
        locked_user = version_is_locked(draft_version)
        if locked_user and locked_user != user:
            raise ConditionFailed(message.format(user=locked_user))
    return inner


error_message = _('Action Denied. The latest version is locked with {user}')
draft_error_message = _('Action Denied. The draft version is locked with {user}')


models.Version.check_archive += [_is_version_locked(error_message)]
models.Version.check_discard += [_is_version_locked(error_message)]
models.Version.check_revert += [_is_draft_version_locked(draft_error_message)]
models.Version.check_unpublish += [_is_draft_version_locked(draft_error_message)]
models.Version.check_edit_redirect += [_is_draft_version_locked(draft_error_message)]
