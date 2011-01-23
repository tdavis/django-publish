#!/usr/bin/env python

import argparse
from django.template.defaultfilters import slugify
from articles.models import Article
from publish.utils import parse_meta_and_article, filter_field
from publish.utils import ConfigurationError
from publish.conf import FIELD_TO_KWARG, SAVE_NEEDED, REQUIRED_FIELDS, DB
from publish.conf import FIELD_DEFAULTS


def setfield(article, name, value, debug=False):
    """
    Simple function to keep things DRY
    """
    key = FIELD_TO_KWARG.get(name, name)
    try:
        setattr(article, key, value)
        if debug:
            print 'Set `%s` (as `%s`) -> %s' % (name, key, value)
    except ValueError:
        raise ValueError('Set primary key on Article to modify `%s`' % key)

def publish(f, draft, by=None, publish=None, is_active=True, login_required=False, debug=False):
    """
    Publishes an article.

    :param f: The file to parse
    :type f: file
    :param by: Author username
    :type by: str
    :param draft: Save as draft?
    :type draft: bool
    :param draft: Article active?
    :type draft: bool
    :param draft: Require login?
    :type draft: bool
    :param publish: When to publish
    :type publish: datetime fmt=YYYY-MM-DD HH:MM
    :param debug: Print debug data
    :type debug: bool

    :returns: Saved :class:`Article`
    """
    meta, content = parse_meta_and_article(f.read())
    meta.update({
        'is_active': is_active,
        'login_required': login_required,
    })
    if draft:
        meta['status'] = 'Draft'
    if publish:
        meta['publish'] = publish
    if by:
        meta['by'] = by
    slug = slugify(meta['title'])
    # New or updated?
    articles = Article.objects.using(DB).filter(slug=slug)
    if len(articles) > 1:
        if not publish:
            raise ConfigurationError('Title ambiguous; supply publish date')
        articles.filter(publish_date=meta['publish'])
        article = articles[0]
    elif len(articles) == 1:
        article = articles[0]
    else:
        article = Article()

    article.content = content
    article.markup = 'h'

    todo = []
    keys = list(meta.keys())
    for key in keys + [k for k in REQUIRED_FIELDS+FIELD_DEFAULTS.keys() if k not in keys]:
        value = filter_field(key, meta)
        if key not in SAVE_NEEDED:
            setfield(article, key, value, debug)
        else:
            todo.append((key, value))
    article.save(using=DB)

    for key, value in todo:
        setfield(article, key, value, debug)
    article.save(using=DB)

    return article

def main():
    """
    ``publish`` executable.
    """
    parser = argparse.ArgumentParser(description='Article Publisher')
    parser.add_argument('path', type=argparse.FileType('r'),
                        help='Relative or absolute path to article')
    parser.add_argument('--by -b', type=str, metavar='name',
                        help='Author (by name)', default='', dest='by')
    parser.add_argument('--draft -d', action='store_true', default=False,
                        help='Publish as a draft only', dest='draft')
    parser.add_argument('--noactive', action='store_false', default=True,
                        help='Make the article "inactive"', dest='is_active')
    parser.add_argument('--login', action='store_true', default=False,
                        help='Require a login to view the article',
                        dest='login_required')
    parser.add_argument('--publish -p', type=str, metavar='YYYY-MM-DD HH:MM',
                        help='When to publish the article (overrides in-file '
                        'value, if any)', default='', dest='publish')
    parser.add_argument('--debug', action='store_true', default=False,
                        help='Print debugging info', dest='debug')
    args = parser.parse_args()
    article = publish(args.path, args.draft, args.by, args.publish, args.is_active, args.login_required, args.debug)
    print '%s (pk=%d) saved as %s' % (article.title, article.pk, article.status.name)

