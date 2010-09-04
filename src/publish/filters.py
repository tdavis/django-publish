from articles.models import Article, Tag


def article_slugs(text):
    """
    Retrieve a list of :class:`Article` objects based on field text
    (a return-delimeted list of slugs).

    :param text: The text, such as:
            
            my-best-post
            my-second-best-post

    :returns: ``QuerySet`` of :class:`Articles`
    """
    from publish.conf import DB

    slugs = text.split('\n')
    return Article.objects.using(DB).filter(slug__in=slugs)

def tags(tagstr):
    """
    Convert a space-delimited list of tags to their :class:`Tag` equivalients.
    
    TODO:   Improve tags to support multiple words (make ``django-articles`` use
            ``django-tagging``!)
    
    :param tagstr: Tags in the form, ``one two three``.
    """
    from publish.conf import DB

    tag = lambda n: Tag.objects.using(DB).get_or_create(name=Tag.clean_tag(n))[0]
    return [tag(t) for t in tagstr.split()]

