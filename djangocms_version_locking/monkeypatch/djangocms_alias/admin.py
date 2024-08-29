from django.contrib import admin
from django.urls import reverse
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from djangocms_alias.admin import AliasAdmin as OriginalAliasAdmin
from djangocms_alias.models import Alias
from djangocms_versioning.helpers import get_latest_admin_viewable_content, proxy_model, version_list_url


class AliasAdmin(OriginalAliasAdmin):
    def get_actions_list(self) -> list:
        """Add alias edit link, manage version link"""
        original_list = super().get_actions_list()
        usage_link_index = original_list.index(self._get_alias_usage_link)
        original_list.insert(usage_link_index-1, self._get_edit_link)
        original_list.insert(usage_link_index-1, self._get_manage_versions_link)


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

def _get_edit_link(self, obj: Alias, request: HttpRequest, disabled: bool = False):
    version = proxy_model(obj, self._get_content_obj(obj))
    # if not version.check_edit_redirect.as_bool(request.user):
    #     # Don't display the link if it can't be edited
    #     return ""
    if not version.check_edit_redirect.as_bool(request.user):
        disabled = True

    url = reverse(
        "admin:{app}_{model}_edit_redirect".format(
            app=version._meta.app_label, model=version._meta.model_name
        ),
        args=(version.pk,),
    )

    # close sideframe as edit will always be on page and not in sideframe
    return self.admin_action_button(
        url=url,
        icon="pencil",
        title=_("Edit"),
        name="edit",
        disabled=disabled,
        action="post",
        keepsideframe=False,
    )


admin.site.unregister(Alias)
admin.site.register(Alias, AliasAdmin)
