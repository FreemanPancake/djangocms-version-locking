from django.template.loader import render_to_string
from django.utils.html import format_html

from cms.app_base import CMSAppConfig, CMSAppExtension

from djangocms_alias.models import AliasContent
from djangocms_versioning.constants import DRAFT
from djangocms_versioning.helpers import version_is_locked


def add_alias_version_lock(obj, field):
    version = obj.versions.all()[0]
    lock_icon = ""
    if version.state == DRAFT and version_is_locked(version):
        lock_icon = render_to_string("djangocms_version_locking/admin/locked_mixin_icon.html")
    return format_html(
        "{is_locked}{field_value}",
        is_locked=lock_icon,
        field_value=getattr(obj, field),
    )


class VersionLockingCMSExtension(CMSAppExtension):

    def configure_app(self, cms_config):
        pass


class VersionLockingCMSAppConfig(CMSAppConfig):
    djangocms_versioning_enabled = True
    versioning = []
    extended_admin_field_modifiers = [{AliasContent: {"name": add_alias_version_lock}}, ]
