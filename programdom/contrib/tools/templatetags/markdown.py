from django import template
from django.template.defaultfilters import stringfilter

import markdown as md
from django.utils.safestring import mark_safe
from markupsafe import escape

register = template.Library()
extensions=[
    'markdown.extensions.fenced_code',
    'markdown.extensions.abbr',
    'markdown.extensions.def_list',
    'markdown.extensions.footnotes',
]

@register.filter()
@stringfilter
def unsafe_markdown(value):
    return md.markdown(value, extensions=extensions)


@register.filter()
@stringfilter
def markdown(value):
    return mark_safe(md.markdown(escape(value), extensions=extensions))
