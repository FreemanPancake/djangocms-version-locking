from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from djangocms_versioning.admin import ExtendedVersionAdminMixin, StateIndicatorMixin
from djangocms_versioning.constants import INDICATOR_DESCRIPTIONS
from djangocms_versioning.helpers import get_latest_admin_viewable_content
from djangocms_versioning.indicators import content_indicator


def _get_indicator_column(func):
    '''
    Change the State Indicator to readonly, publish process will be take over by djangocms-moderation.
    '''
    def inner(self, request):
        def indicator(obj):
            if self._extra_grouping_fields is not None:  # Grouper Model
                content_obj = get_latest_admin_viewable_content(obj, include_unpublished_archived=True, **{
                    field: getattr(self, field) for field in self._extra_grouping_fields
                })
            else:  # Content Model
                content_obj = obj
            status = content_indicator(content_obj)
            return render_to_string(
                "admin/djangocms_versioning/indicator.html",
                {
                    "state": status or "empty",
                    "description": INDICATOR_DESCRIPTIONS.get(status, _("Empty")),
                    "menu_template": "admin/cms/page/tree/indicator_menu.html",
                }
            )
        indicator.short_description = self.indicator_column_label
        return indicator
    return inner

def _get_actions_list(func):
    '''
    Add `Manage versions` action to versioned admin's action list, State Indicator is ready only.
    '''
    def inner(self):
        actions = func(self)
        actions.append(self._get_manage_versions_link)
        return actions
    return inner


ExtendedVersionAdminMixin.get_actions_list = _get_actions_list(ExtendedVersionAdminMixin.get_actions_list)
StateIndicatorMixin.get_indicator_column = _get_indicator_column(StateIndicatorMixin.get_indicator_column)
