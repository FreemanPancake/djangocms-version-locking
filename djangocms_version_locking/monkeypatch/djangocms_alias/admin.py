from django.contrib import admin
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from djangocms_alias.admin import AliasAdmin as OriginalAliasAdmin
from djangocms_alias.models import Alias
from djangocms_versioning.helpers import (
    get_latest_admin_viewable_content,
    version_list_url,
)


class AliasAdmin(OriginalAliasAdmin):
    def get_actions_list(self) -> list:
        """Add alias manage version link"""
        original_list = super().get_actions_list()
        usage_link_index = original_list.index(self._get_alias_usage_link)
        original_list.insert(usage_link_index-1, self._get_manage_versions_link)
        return original_list

    def _get_content_obj(self, obj: Alias):
        if self._extra_grouping_fields is not None:  # Grouper Model
            content_obj = get_latest_admin_viewable_content(obj, include_unpublished_archived=True, **{
                field: getattr(self, field) for field in self._extra_grouping_fields
            })
        else:  # Content Model
            content_obj = obj
        return content_obj

    def _get_manage_versions_link(self, obj: Alias, request: HttpRequest, disabled: bool = False):
        url = version_list_url(self._get_content_obj(obj))
        return self.admin_action_button(
            url,
            icon="copy",
            title=_("Manage versions"),
            name="manage-versions",
            disabled=disabled,
        )


admin.site.unregister(Alias)
admin.site.register(Alias, AliasAdmin)
