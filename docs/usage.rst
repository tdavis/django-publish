Usage
=====

Read below for more about the specifics of django-publish usage.

.. _available-tags:

Available Tags
--------------

The following tags are available and should be placed somewhere in articles (
the exact location of tags doesn't matter). Tags defined in-file will override
those defined in ``settings.py`` (see: :ref:`configuration`) and will themselves
be overridden by any command-line arguments (see: :ref:`publishing`).

.. topic:: use_addthis

   Defines whether or not to use the *AddThis* button. Default: ``False``.

.. topic:: addthis

   The *AddThis* username. Default: posting user (a django-articles default).

.. topic:: by

   The author of the post, by name.

.. topic:: description

   Meta Description. Default: the "teaser", as defined by
   django-articles.

.. topic:: expire

   Date the post should expire, in the form YYYY-MM-DD HH:MM. Default:
   never.

.. topic:: follow-up

   Any posts this is a follow-up to, as a ``\n``-delimited list of slugs.
   Default: none.

   .. warning::

      There is currently no way to differentiate between identical slugs. This
      issue will be rectified in a later version.

.. topic:: keywords

   Meta Keywords. Default: your tags

.. topic:: publish

   When to publish, in the form YYYY-MM-DD HH:MM. Default: now

.. topic:: related

   Any posts related to this one, as a ``\n``-delimited list of slugs.

   .. warning::

      There is currently no way to differentiate between identical slugs. This
      issue will be rectified in a later version.

.. topic:: tags

   Post tags as a comma-delimited list of strings. Yes, this is inconsistent
   with the ``related`` and ``follow-up`` tags.

Note that not all of these are required in-document and only ``by`` is strictly
required at all. See the next section for fields which may be defined on the
command line (for instance, if you don't want to couple your publish date with
your article source).


.. _publishing:

Publishing
----------

So your post is done and you're ready to publish. What now? Well, you use
``publish`` of course! ``publish`` is the command-line tool that django-publish
provides to hammer your beautiful new post into your blagh's database. The
easiest way to learn ``publish`` is by running ``publish --help``.

