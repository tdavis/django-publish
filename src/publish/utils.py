from docutils import io
from docutils.core import publish_doctree, Publisher
from docutils.readers.doctree import Reader
from docutils.writers import html4css1
from publish.conf import FIELD_DEFAULTS, FILTER_DEFAULTS
from django.conf import settings
# also bootstraps pygment's docutils support
from articles.models import Article


class ConfigurationError(Exception): pass


class Writer(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator


class HTMLTranslator(html4css1.HTMLTranslator):
    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1


def parts_from_doctree(document, destination_path=None,
                         writer=Writer(), writer_name='html4css2',
                         settings=None, settings_spec=None,
                         settings_overrides=None, config_section=None,
                         enable_exit_status=None):
    """
    A version of :func:`docutils.core.publish_from_doctree` that supplies
    the "parts" rather than a regular string representation.
    """
    reader = Reader(parser_name='null')
    pub = Publisher(reader, None, writer,
                    source=io.DocTreeInput(document),
                    destination_class=io.StringOutput, settings=settings)
    if not writer and writer_name:
        pub.set_writer(writer_name)
    pub.process_programmatic_settings(
        settings_spec, settings_overrides, config_section)
    pub.set_destination(None, destination_path)
    output = pub.publish()
    return pub.writer.parts

def parse_meta_and_article(content):
    """
    Parse out the meta declarations (tags, keywords, etc...) from the article
    and return both.

    :param content: Contents of the article file
    :type content: str
    :returns: dict(meta) and str(article)
    """
    meta_field_names = FILTER_DEFAULTS.keys()
    meta = {}
    article = publish_doctree(content)
    for where, node in enumerate(article.traverse()):
        if node.tagname == 'field':
            label = str(node.children[0].children[0])
            if label in meta_field_names:
                value = str(node.children[1].children[0].children[0])
                meta[label] = value
                node.parent.remove(node)
        elif node.tagname == 'title' and 'title' not in meta:
            value = str(node.children[0])
            meta['title'] = value
            node.parent.remove(node)
    
    raw = parts_from_doctree(article)
    return (meta, raw['fragment'])

def filter_field(key, fields, func=None):
    """
    Run a field through the given filter, or default if none is provided. If
    field doesn't exist, it will attempt to return the default value for that
    field.

    :param key: the field name to use
    :param fields: a dictionary of available fields in the form ``name: value``
    :returns: Filtered value
    :raises: KeyError in the event the field can't be found among the provided
        ones or the defaults
    """
    try:
        val = fields[key]
    except KeyError:
        default_fields = getattr(settings, 'PUBLISH_FIELD_DEFAULTS', {})
        FIELD_DEFAULTS.update(default_fields)
        try:
            val = FIELD_DEFAULTS[key]
        except KeyError:
            raise ConfigurationError('You must supply the `%s` field in the'
                            ' article, via settings.PUBLISH_FIELD_DEFAULTS, or'
                            ' via command line (where applicable)' % key)


    default_filters = getattr(settings, 'PUBLISH_FILTER_DEFAULTS', {})
    FILTER_DEFAULTS.update(default_filters)
    f = func or FILTER_DEFAULTS[key] 
    return f(val)

