import codecs
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='decode_unicode')
def decode_unicode(value):
    """
    Decode Unicode escape sequences in strings
    """
    if not value:
        return value
    
    try:
        # Try to decode Unicode escape sequences
        decoded = codecs.decode(value, 'unicode_escape')
        return mark_safe(decoded)
    except (UnicodeDecodeError, UnicodeEncodeError):
        # If decoding fails, return the original value
        return mark_safe(value)
