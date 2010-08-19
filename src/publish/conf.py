from datetime import datetime
from articles.models import ArticleStatus
from publish.filters import article_slugs, tags
from django.conf import settings
from django.contrib.auth.models import User


FIELD_DEFAULTS = {
    'addthis': False,
    'status': 'Draft',
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
    'publish': lambda d: datetime.strptime(d, '%Y-%m-%d %H%M'),
    'expire': lambda d: datetime.strptime(d, '%Y-%m-%d %H%M'),
    'author': lambda a: a and User.objects.get(username=a) or \
        User.objects.get(username=getattr(settings, 'PUBLISH_FIELD_DEFAULTS', {}).get('by', 0))
}

FIELD_TO_KWARG = {
    'addthis': 'use_addthis_button',
    'by': 'username',
    'expire': 'expiration_date',
    'publish': 'publish_date',
    'followup': 'followup_for',
    'related': 'related_articles',
}
    

