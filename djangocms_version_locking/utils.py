from django import forms


class AdminActionListMixin(metaclass=forms.MediaDefiningClass):
    """AdminActionListMixin is a mixin for the Versioned Model class. It adds the ability to have
    action buttons and a burger menu in the admin's change list view.
    """

    class Media:
        js = (
            "admin/js/jquery.init.js",
            "djangocms_version_locking/js/actions.js",
        )
        css = {"all": ("djangocms_version_locking/css/actions.css",)}
