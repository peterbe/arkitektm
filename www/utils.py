# python
import re
import unicodedata

# django
from django.utils.safestring import mark_safe

def slugify(value):
    """
    Normalizes string, removes non-alpha characters,
    and converts spaces to hyphens.
    
    Peter: Copied this from django/template/defaultfilters.py but removed
    the lowercasing thing
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip())
    return mark_safe(re.sub('[\s]+', '_', value))

