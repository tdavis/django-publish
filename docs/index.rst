.. django-publish documentation master file, created by
   sphinx-quickstart on Thu Aug 19 13:57:06 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Say Hello to django-publish!
============================

When used in conjunction with django-articles_, django-publish lets you
publish your blog from the command line. I created this application because I
was tired of using anything but Vim_ and RestructuredText_ to compose my
articles. Thankfully django-articles gave me an easy way to use the latter, but
using the former still required copying and pasting. django-publish rectifies
this and streamlines the whole process of writing, publishing, and updating an
article. It also allows you to keep all your posts under source control, or
indeed do whatever else you want with them.

Through a series of simple tags, django-publish allows you to configure a post.
Via a single command, you can then publish it. Here's an example post:

.. literalinclude:: /../src/publish/tests/sample.rst
   :language: rst

As you can see, a series of tags defines various attributes of the post (a list
of :ref:`available-tags` is elsewhere). The first major title (`===`) is used as
the title of the post to reduce repetition. Other than that, everything works as
it does in any other ``reST`` document. When you're ready to publish or update a
post, it's just a command away (see: :ref:`publishing`).

Still interested? Then read on!

.. toctree::
   :maxdepth: 2

   install
   usage


.. _django-articles: http://bitbucket.org/codekoala/django-articles/
.. _Vim: http://vim.org
.. _RestructuredText: http://docutils.sourceforge.net/rst.html


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

