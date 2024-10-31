from django.contrib import admin
from django.http import HttpRequest
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from djangocms_alias.admin import AliasAdmin as OriginalAliasAdmin
from djangocms_alias.models import Alias
from djangocms_versioning.constants import DRAFT, PUBLISHED
from djangocms_versioning.helpers import (
    get_latest_admin_viewable_content,
    proxy_model,
    version_list_url,
)


class AliasAdmin(OriginalAliasAdmin):

    change_list_template = "monkeypatch/cms/admin/cms/grouper/change_list.html"

    def get_actions_list(self) -> list:
        """Add alias manage version link"""
        original_list = super().get_actions_list()
        settings_link_index = original_list.index(self._get_settings_action)
        preview_link_index = original_list.index(self._get_view_action)
        original_list.insert(settings_link_index, self._get_manage_versions_link)
        original_list.insert(preview_link_index+1, self._get_edit_link)
        return original_list

    def _get_content_obj(self, obj: Alias):
        if self._extra_grouping_fields is not None:  # Grouper Model
            content_obj = get_latest_admin_viewable_content(obj, include_unpublished_archived=True, **{
                field: getattr(self, field) for field in self._extra_grouping_fields
            })
        else:  # Content Model
            content_obj = obj
        return content_obj

    def _get_edit_link(self, obj: Alias, request: HttpRequest, disabled: bool = False):
        version = proxy_model(self._get_content_obj(obj).versions.all()[0], self._get_content_obj(obj))

        if version.state not in (DRAFT, PUBLISHED):
            # Don't display the link if it can't be edited
            return ""
        if not version.check_edit_redirect.as_bool(request.user):
            disabled = True

        if version.state == PUBLISHED:
            icon = "edit-new"
            title = "New Draft"
        else:
            icon = "pencil"
            title = "Edit"

        url = reverse(
            "admin:{app}_{model}_edit_redirect".format(
                app=version._meta.app_label, model=version._meta.model_name
            ),
            args=(version.pk,),
        )

        # close sideframe as edit will always be on page and not in sideframe
        return self.admin_action_button(
            url=url,
            icon=icon,
            title=_(title),
            name="edit",
            disabled=disabled,
            action="post",
            keepsideframe=False,
        )

    def _get_manage_versions_link(self, obj: Alias, request: HttpRequest, disabled: bool = False):
        url = version_list_url(self._get_content_obj(obj))
        return self.admin_action_button(
            url,
            icon="copy",
            title=_("Manage versions"),
            name="manage-versions",
            disabled=disabled,
        )

    def has_delete_permission(self, request: HttpRequest, obj=None):
        return False


admin.site.unregister(Alias)
admin.site.register(Alias, AliasAdmin)
