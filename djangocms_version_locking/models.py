# NOTE: 'version lock' has been migrated to djangocms_versioning.Version table 'locked_by' field.
# so this table is not needed anymore after data migration.

# from django.conf import settings
# from django.db import models
# from django.utils.translation import gettext_lazy as _

# from djangocms_versioning.models import Version


# class VersionLock(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.PROTECT,
#         verbose_name=_('locked by')
#     )
#     version = models.OneToOneField(
#         Version,
#         on_delete=models.CASCADE,
#         verbose_name=_('version')
#     )
