from datetime import datetime
from articles.models import ArticleStatus
from publish.filters import article_slugs, article_tags
from django.conf import settings
from django.contrib.auth.models import User


# Database to use
DB = getattr(settings, 'PUBLISH_DB', 'default')

# Some sane defaults
FIELD_DEFAULTS = {
    'use_addthis': False,
    'status': 'Finished',
    'addthis': 'nobody',
    'login_required': False
}

# Default filters / transformations for fields
FILTER_DEFAULTS = {
    'title': lambda title: title,
    'tags': article_tags,
    'keywords': lambda kw: kw,
    'description': lambda desc: desc.replace('\n', ' '),
    'follow-up': article_slugs,
    'related': article_slugs,
    'status': lambda status: ArticleStatus.objects.using(DB).get(name=status),
    'use_addthis': lambda a: bool(a),
    'addthis': lambda a: bool(a),
    'publish': lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M'),
    'expire': lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M'),
    'by': lambda a: a and User.objects.using(DB).get(username__iexact=a) or \
        User.objects.using(DB).get(username=getattr(
            settings, 'PUBLISH_FIELD_DEFAULTS', {}).get('by', 0)),
    'is_active': lambda a: a,
    'login_required': lambda a: a
}

# Many-to-Many fields require a saved object before they work
SAVE_NEEDED = ('follow-up', 'related', 'tags')

# `django-articles` needs these, at least
REQUIRED_FIELDS = ['title', 'by']

# Convert our tag names to field names
FIELD_TO_KWARG = {
    'use_addthis': 'use_addthis_button',
    'addthis': 'addthis_username',
    'by': 'author',
    'expire': 'expiration_date',
    'publish': 'publish_date',
    'follow-up': 'followup_for',
    'related': 'related_articles',
}

