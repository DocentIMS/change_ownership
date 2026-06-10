Introduction
============

plone.app.changeownership as it sounds is a Plone package to change objects
ownership.

Problem
=======

While for a single content you can call the ``/change-owner`` view,
there is no way in Plone to transfer **ownership of all objects** owned by an user
to a new user. To delete a Plone member in such case is not an option. 

Solution
========

plone.app.changeownership makes easy to transfer ownership from one ore more 
members to a new member. It also can change content metadata, like *Creators*
field.

Compatibility
=============

Version 2.0 and later target **Plone 6** (6.0 / 6.1) on Python 3.8 - 3.12.
For Plone 5.x use the 1.0 release.

Install
=======

The addon can be installed with ``pip`` or via a Plone buildout.

* With pip, add ``plone.app.changeownership`` to your project requirements
  (or constraints) and install it alongside Plone, e.g.: ::

    $ pip install plone.app.changeownership

* With buildout, add ``plone.app.changeownership`` to the list of eggs: ::

    [buildout]
    ...
    eggs =
        ...
        plone.app.changeownership

  and re-run buildout: ::

    $ ./bin/buildout

After restarting Plone, activate the add-on from the *Add-ons* control panel
(Site Setup → Add-ons). You will then get a configlet in the Plone control
panel named "Change Ownership".

