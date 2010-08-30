from datetime import datetime
from articles.models import ArticleStatus
from publish.filters import article_slugs, tags
from django.conf import settings
from django.contrib.auth.models import User


FIELD_DEFAULTS = {
    'use_addthis': False,
    'status': 'Finished',
}

FILTER_DEFAULTS = {
    'title': lambda title: title,
    'tags': tags,
    'keywords': lambda kw: kw,
    'description': lambda desc: desc.replace('\n', ' '),
    'follow-up': article_slugs,
    'related': article_slugs,
    'status': lambda status: ArticleStatus.objects.get(name=status),
    'addthis': lambda a: bool(a),
    'publish': lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M'),
    'expire': lambda d: datetime.strptime(d, '%Y-%m-%d %H:%M'),
    'by': lambda a: a and User.objects.get(username__iexact=a) or \
        User.objects.get(username=getattr(settings, 'PUBLISH_FIELD_DEFAULTS', {}).get('by', 0)),
    'is_active': lambda a: a,
    'login_required': lambda a: a
}

SAVE_NEEDED = ('follow-up', 'related', 'tags')

REQUIRED_FIELDS = ('title', 'by')

FIELD_TO_KWARG = {
    'use_addthis': 'use_addthis_button',
    'addthis': 'addthis_username',
    'by': 'author',
    'expire': 'expiration_date',
    'publish': 'publish_date',
    'follow-up': 'followup_for',
    'related': 'related_articles',
}

