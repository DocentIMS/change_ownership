# -*- coding: utf-8 -*-

import unittest
from zope.component import getMultiAdapter
from DateTime import DateTime
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.changeownership.testing import OWNERSHIP_INTEGRATION_TESTING


class ChangeOwnershipTestCase(unittest.TestCase):

    layer = OWNERSHIP_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, TEST_USER_NAME)
        self._createContent()

    def _createContent(self):
        self.portal.invokeFactory(
            type_name="Document", id='page', title="New document")

    # -- helpers ----------------------------------------------------------

    def _view(self, context=None):
        ctx = context if context is not None else self.portal.page
        return getMultiAdapter((ctx, self.request), name=u"change-owner")

    def _change(self, context=None, **form):
        """Populate request.form, run change_owner(), return the view.

        Pass checkbox options as real booleans to mimic the Zope ``:boolean``
        converter (an unchecked box is simply *absent*, so omit the key).
        """
        self.request.form.clear()
        form.setdefault('submit', '1')
        self.request.form.update(form)
        view = self._view(context)
        view.change_owner()
        return view

    # -- existing behaviour (with the assertTrue bug fixed) ---------------

    def test_fake_oldusers(self):
        # No object has creator 'foo', so nothing changes.
        self._change(oldowners=['foo'], newowner='user')
        # Was: assertTrue(Creator(), TEST_USER_ID) -- 2nd arg is the *message*,
        # so it never actually compared. Use assertEqual.
        self.assertEqual(self.portal.page.Creator(), TEST_USER_ID)

    def test_fake_new_user(self):
        self.request.form.clear()
        self.request.form.update(
            {'oldowners': [TEST_USER_ID], 'newowner': 'imnothere',
             'submit': '1'})
        view = self._view()
        self.assertRaises(KeyError, view.change_owner)

    def test_change_Creator(self):
        self._change(oldowners=[TEST_USER_ID], newowner='user')
        self.assertEqual(self.portal.page.Creator(), 'user')

    def test_do_not_change_modification_time(self):
        self.portal.page.setModificationDate(DateTime() - 1)
        old = self.portal.page.ModificationDate()
        self._change(oldowners=[TEST_USER_ID], newowner='user',
                     change_modification_date=False)
        self.assertEqual(self.portal.page.ModificationDate(), old)

    # -- newly covered branches -------------------------------------------

    def test_change_modification_time(self):
        """change_modification_date=True -> modified date bumps to now."""
        self.portal.page.setModificationDate(DateTime() - 1)
        old = self.portal.page.ModificationDate()
        self._change(oldowners=[TEST_USER_ID], newowner='user',
                     change_modification_date=True)
        self.assertNotEqual(self.portal.page.ModificationDate(), old)

    def test_dry_run_changes_nothing(self):
        """dry_run=True lists the object but must not change ownership."""
        view = self._change(oldowners=[TEST_USER_ID], newowner='user',
                            dry_run=True)
        self.assertEqual(self.portal.page.Creator(), TEST_USER_ID)
        # The path of the would-be-changed object is reported in the status.
        joined = " ".join(str(m) for m in view.status)
        self.assertIn('page', joined)

    def test_keep_old_creators_by_default(self):
        """Default: new owner is prepended, old creator is kept."""
        self._change(oldowners=[TEST_USER_ID], newowner='user')
        creators = self.portal.page.Creators()
        self.assertEqual(creators[0], 'user')
        self.assertIn(TEST_USER_ID, creators)

    def test_delete_old_creators(self):
        """delete_old_creators=True removes the old creator entirely."""
        self._change(oldowners=[TEST_USER_ID], newowner='user',
                     delete_old_creators=True)
        creators = self.portal.page.Creators()
        self.assertEqual(tuple(creators), ('user',))
        self.assertNotIn(TEST_USER_ID, creators)

    def test_keep_old_owner_role_by_default(self):
        """Default: old owner keeps the Owner local role; new owner gains it."""
        self.portal.page.manage_setLocalRoles(TEST_USER_ID, ['Owner'])
        self._change(oldowners=[TEST_USER_ID], newowner='user')
        self.assertIn(
            'Owner', self.portal.page.get_local_roles_for_userid('user'))
        self.assertIn(
            'Owner', self.portal.page.get_local_roles_for_userid(TEST_USER_ID))

    def test_delete_old_owners(self):
        """delete_old_owners=True strips the Owner local role from old owner."""
        self.portal.page.manage_setLocalRoles(TEST_USER_ID, ['Owner'])
        self._change(oldowners=[TEST_USER_ID], newowner='user',
                     delete_old_owners=True)
        self.assertIn(
            'Owner', self.portal.page.get_local_roles_for_userid('user'))
        self.assertNotIn(
            'Owner', self.portal.page.get_local_roles_for_userid(TEST_USER_ID))

    def test_validation_requires_newowner(self):
        view = self._change(oldowners=[TEST_USER_ID], newowner='')
        self.assertIn(view.need_newowner_message, view.status)
        self.assertEqual(self.portal.page.Creator(), TEST_USER_ID)

    def test_validation_requires_oldowners(self):
        view = self._change(oldowners=[], newowner='user')
        self.assertIn(view.need_oldowners_message, view.status)
        self.assertEqual(self.portal.page.Creator(), TEST_USER_ID)

    def test_oldowners_accepts_a_string(self):
        """A single old owner may arrive as a string, not a list."""
        view = self._change(oldowners=TEST_USER_ID, newowner='user',
                            dry_run=True)
        # No crash, and the page is reported (dry run -> unchanged).
        self.assertEqual(self.portal.page.Creator(), TEST_USER_ID)
        self.assertIn('page', " ".join(str(m) for m in view.status))

    def test_path_filter_limits_scope(self):
        """Only content under the given path is touched."""
        self.portal.invokeFactory(type_name="Folder", id='sub', title="Sub")
        self.portal.sub.invokeFactory(
            type_name="Document", id='inside', title="Inside")
        self._change(oldowners=[TEST_USER_ID], newowner='user', path='/sub')
        self.assertEqual(self.portal.sub.inside.Creator(), 'user')
        # The root page is outside '/sub' and must be untouched.
        self.assertEqual(self.portal.page.Creator(), TEST_USER_ID)

    def test_members_folder_excluded_when_checked(self):
        members = self._make_members_doc()
        self._change(oldowners=[TEST_USER_ID], newowner='user',
                     exclude_members_folder=True)
        self.assertEqual(members.Creator(), TEST_USER_ID)   # excluded
        self.assertEqual(self.portal.page.Creator(), 'user')  # outside Members

    def test_members_folder_included_when_unchecked(self):
        """Regression: unchecking the box (key absent) must INCLUDE members.

        Before the fix, change_owner() read exclude_members_folder() which
        defaults True, so an absent (unchecked) field still excluded -- the
        toggle was stuck on. This asserts the toggle now works.
        """
        members = self._make_members_doc()
        # Note: no exclude_members_folder key -> simulates an unchecked box.
        self._change(oldowners=[TEST_USER_ID], newowner='user')
        self.assertEqual(members.Creator(), 'user')

    def test_list_authors_and_members(self):
        view = self._view()
        author_ids = [a['id'] for a in view.list_authors()]
        member_ids = [m['id'] for m in view.list_members()]
        self.assertIn(TEST_USER_ID, author_ids)
        self.assertIn('user', member_ids)

    # -- helpers for the members-folder tests -----------------------------

    def _make_members_doc(self):
        """Create a 'Members' folder with a doc, owned by the test user."""
        if 'Members' not in self.portal.objectIds():
            self.portal.invokeFactory(
                type_name="Folder", id='Members', title="Members")
        self.portal.Members.invokeFactory(
            type_name="Document", id='mdoc', title="Member doc")
        return self.portal.Members.mdoc
