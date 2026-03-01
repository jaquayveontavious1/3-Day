# templatetags/session_tags.py
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def clear_session_key(context, key_name):
    try:
        del context['request'].session[key_name]
    except KeyError:
        pass
    return ''
