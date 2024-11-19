from django.contrib import admin


def get_registered_admin(model, defaultAdmin):
    admin_instance = admin.site._registry.get(model)
    if admin_instance:
        return admin_instance.__class__
    else:
        return defaultAdmin
