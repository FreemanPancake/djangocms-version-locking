from django.contrib import messages
from django.contrib.admin.utils import unquote
from django.http import Http404, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import re_path, reverse
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

from djangocms_versioning import admin, constants
from djangocms_versioning.helpers import version_is_locked


def _locked(self, version):
    """
    Generate an locked field for Versioning Admin, to override the default locked icon from djangocms-versioning.
    """
    if version.state == constants.DRAFT and version_is_locked(version):
        return render_to_string('djangocms_version_locking/admin/locked_icon.html')
    return ""

admin.VersionAdmin.locked = _locked


# Add Version Locking css media to the Versioning Admin instance
additional_css = ('djangocms_version_locking/css/version-locking.css',)
admin.VersionAdmin.Media.css['all'] = admin.VersionAdmin.Media.css['all'] + additional_css
