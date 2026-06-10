Changelog
=========

2.1 (unreleased)
----------------

- Bug fix: "Exclude members folder" can now be turned off. The option is a
  ``:boolean`` checkbox (absent when unchecked), but ``change_owner()`` read it
  via the ``exclude_members_folder()`` method, which defaults to ``True`` --
  so unchecking it had no effect and the members folder was always excluded.
- Expanded the test suite to cover the option flags (dry-run,
  delete_old_creators, delete_old_owners, change_modification_date),
  the path filter, validation errors, string ``oldowners``, and the members
  folder exclusion (including a regression test for the fix above).
- Fixed an incorrect assertion in ``test_fake_oldusers`` (``assertTrue`` with a
  message argument never compared the value).
- Added a GitHub Actions workflow running the tests against Plone 6.2.


2.0 (2026-06-08)
----------------

- Plone 6 compatibility (Plone 6.0 / 6.1, Python 3.8 - 3.12)
- Replaced the ``@@pas_search`` lookup with ``acl_users.searchUsers()``
- Updated the control panel configlet to use a Plone 6 Bootstrap icon
- Modernized the change-owner form template for Plone 6 Classic UI
- Removed the legacy ``Extensions/install.py`` QuickInstaller hook
- Dropped Python 2 support and declared explicit dependencies


1.0 (2019-09-02)
----------------

- Plone 5 compatibility
  [tomgross]

- Python 3 compatibility
  [ajung]

- German translation
  [tomgross]


0.5 (2015-07-29)
----------------

- Fixed path filter
  [uschwarz]
- Minor changes to ownership form
  [keul]
- Support for Site Administrator role with a proper permissions
  [keul]
- Added uninstall profile
  [keul]
- Closed `#3`__:  Dexterity content doesn't have Creators method
  [keul]
- Added new check flag to chose if changing modification date or not
  [keul]

__ http://plone.org/products/plone.app.changeownership/issues/3

0.4 (2012-09-20)
----------------

- Fix permissions for Plone 4 [fdelia]

0.3 (2011-03-07)
----------------

- Added MANIFEST.in [WouterVH]
- Added Dutch-translation [WouterVH]
- Added z3c.autoinclude support [keul]
- Added italian translation [keul]

0.2 (2010-02-02)
----------------

- Added check to support instances without a membersfolder [jaroel]

0.1 (2008-02-01)
----------------

- Merged matth's branch that adds:

  - Filter by path
  - Dry run option
  - Sorting of usernames
  - Display userid as well as full name

- Initial release
