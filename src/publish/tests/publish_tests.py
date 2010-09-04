import os
from StringIO import StringIO
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from docutils.core import publish_doctree
from publish import publish
from publish.utils import parts_from_doctree, parse_meta_and_article, filter_field
from publish.utils import ConfigurationError
from articles.models import Article, ArticleStatus, Tag


# This shouldn't be necessary but I can't figure out why normal fixture loading
# doesn't seem to work for this particular app.
from django.conf import settings
here = os.path.abspath(os.path.split(__file__)[0])
setattr(settings, 'FIXTURE_DIRS', [os.path.join(here, '../fixtures')])


class PublishTests(TestCase):
    fixtures = ['test_articles.json']

    def setUp(self):
        self.raw_sample = open(os.path.join(here, 'sample.rst'), 'r').read()
        self.article = Article.objects.get(pk=1)
        self.meta, self.html = parse_meta_and_article(self.raw_sample)

    def test_parts_from_doctree(self):
        """
        Test parsing parts from a doctree
        """
        article = publish_doctree(self.raw_sample)
        parts = parts_from_doctree(article)
        self.assertTrue('fragment' in parts)
        frag = parts['fragment']
        self.assertTrue('Some content' in frag)
        self.assertTrue('Post description...' not in frag)

    def test_simple_meta(self):
        """
        Test simple meta-data conversions
        """
        keywords = filter_field('keywords', self.meta)
        description = filter_field('description', self.meta)
        title = filter_field('title', self.meta)
        self.assertEqual(keywords, self.article.keywords)
        self.assertEqual(description, self.article.description)
        self.assertEqual(title, self.article.title)

    def test_article_slugs(self):
        """
        Test ``article_slugs`` filter
        """
        self.assertEqual(filter_field('related', self.meta)[0], self.article)

    def test_status_default(self):
        """
        Test ``status`` filter and use of conf defaults
        """
        status = ArticleStatus.objects.get(name='Finished')
        self.assertEqual(filter_field('status', self.meta), status)

    def test_author(self):
        """
        Test ``author`` filter which results in a ConfigurationError by default
        """
        self.assertRaises(ConfigurationError, filter_field, 'author', self.meta)

    def test_tags(self):
        """
        Test ``tags`` filter
        """
        tagqs = Tag.objects.all()
        self.assertEqual(list(tagqs), filter_field('tags', self.meta))

    def test_publish_update(self):
        """
        Publish an article update
        """
        f = open(os.path.join(here, 'sample.rst'))

        publish(f, draft=True, login_required=True)
        updated_article = Article.objects.get(pk=1)
        self.assertFalse(self.article.login_required)
        self.assertTrue(updated_article.login_required)

    def test_publish_new(self):
        """
        Publish a new article
        """
        # Make a different title
        title = 'Here is another article'
        pubstr = '2020-09-01 12:00'
        pubdate = filter_field('publish', { 'publish': pubstr })
        contents = open(os.path.join(here, 'sample.rst')).read().replace(
            'This is my title', title)
        f = StringIO(contents)

        a = publish(f, draft=True, publish=pubstr, debug=True)
        self.assertNotEqual(a.pk, self.article.pk)
        self.assertEqual(a.title, title)
        self.assertEqual(a.publish_date, pubdate)
        self.assertTrue('Some content' in a.content)
        followups = a.followup_for.all()
        self.assertTrue(self.article.pk in [a.pk for a in followups], followups)
        related = a.related_articles.all()
        # We have to use titles due to ambiguous slug
        self.assertTrue(self.article.title in [b.title for b in related], related)

