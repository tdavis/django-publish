Installation
============

Ready to install django-publish? Sweet!


Requirements
------------

Because django-publish is meant to be used in conjunction with django-articles,
it doesn't make Django or anything related to django-articles a requirement for
installation. However, django-publish expects to be used from a valid Django
environment, meaning ``DJANGO_SETTINGS_MODULE`` must be set, etc. Additionally,
**Django 1.2+ is required** due to our support of multiple databases.


Choose Your Adventure
---------------------

You can install the application directly via ``pip``::

    pip install django-publish

Or checkout the source directly from GitHub and install it manually::

    git clone git@github.com:tdavis/django-publish.git
    cd django-publish
    python setup.py install


.. _configuration:

Configuration
-------------

A few  configuration options exist for django-publish; they should be placed in
``settings.py`` for your blog.

.. topic:: PUBLISH_DB

   Defines the database name to use for publishing. Default: ``default``.

.. topic:: PUBLISH_FIELD_DEFAULTS

   Allows you to define default values for arbitrary fields. This should be a
   dictionary of the form ``{ tag: value, ... }``.  See :ref:`available-tags`
   for what can be defined. 

