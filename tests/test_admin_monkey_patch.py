from django.template.loader import render_to_string

from cms.test_utils.testcases import CMSTestCase

from djangocms_versioning import constants
from djangocms_versioning.helpers import version_list_url

from djangocms_version_locking.test_utils import factories
from djangocms_version_locking.test_utils.polls.cms_config import PollsCMSConfig


class VersionLockedIconTestCase(CMSTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.default_permissions = ["change_pollcontentversion"]

    def setUp(self):
        self.superuser = self.get_superuser()
        self.regular_staff_user = self._create_user(
            "regular",
            is_staff=True,
            permissions=["view_pollcontentversion"] + self.default_permissions,
        )

    def test_version_locked_icon_added(self):
        """
        With the admin monkeypatch, the locked icon template is override
        """
        poll_version = factories.PollVersionFactory(created_by=self.superuser)
        changelist_url = version_list_url(poll_version.content)

        with self.login_user_context(self.regular_staff_user):
            response = self.client.post(changelist_url)

        self.assertContains(response, '<a class="cms-version-locked-status-icon" title="Locked">')
        self.assertContains(response, '<img src="/static/djangocms_version_locking/svg/lock.svg">')

    def test_version_locked_icon_not_added(self):
        """
        With the admin monkeypatch, the locked icon template is override
        """
        poll_version = factories.PollVersionFactory(created_by=self.superuser)
        changelist_url = version_list_url(poll_version.content)

        with self.login_user_context(self.superuser):
            response = self.client.post(changelist_url)

        self.assertNotContains(response, '<a class="cms-version-locked-status-icon" title="Locked">')
        self.assertNotContains(response, '<img src="/static/djangocms_version_locking/svg/lock.svg">')


class VersionLockMediaMonkeyPatchTestCase(CMSTestCase):

    def setUp(self):
        self.superuser = self.get_superuser()

    def test_version_locking_css_media_loaded(self):
        """
        The verison locking css media is loaded on the page
        """
        poll_version = factories.PollVersionFactory(created_by=self.superuser)
        changelist_url = version_list_url(poll_version.content)
        css_file = "djangocms_version_locking/css/version-locking.css"

        with self.login_user_context(self.superuser):
            response = self.client.post(changelist_url)

        self.assertContains(response, css_file)
