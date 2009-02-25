# python
import re
from cgi import escape
from pprint import pprint

# django
from django.contrib.flatpages.models import FlatPage
from django import template

# app
from settings import DEBUG


register = template.Library()

@register.filter()
def clean_numbered_title(title):
    return _clean_numbered_title(title)

numbered_title_regex = re.compile('^\d+\.?\s*')
def _clean_numbered_title(title):
    return numbered_title_regex.sub('', title).strip()


class FlatpageToMenuNode(template.Node):
    def __init__(self, css_class=None):
        self.css_class = css_class
    def render(self, context):
        return flatpages_to_menu(css_class=self.css_class)

@register.tag(name='flatpages_to_menu')
def flatpages_to_menu_node(parser, token):
    _split = token.split_contents()
    tag_name = _split[0]
    options = _split[1:]
    css_class = None
    try:
        css_class = options[0]
        if not (css_class[0] == css_class[-1] and css_class[0] in ('"', "'")):
            raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
        css_class = css_class[1:-1]
    except IndexError:
        pass
    
    return FlatpageToMenuNode(css_class=css_class)
    


def flatpages_to_menu(css_class=None):
    html = []
    recursive_list = _flatpages()
    if DEBUG:
        #pprint(recursive_list)
        html = '\n'.join(_flatpages_html(recursive_list))
    else:
        html = ''.join(_flatpages_html(recursive_list))
    if css_class:
        html = html.replace('<ul>','<ul class="%s">' % css_class, 1)
    return html

def _flatpages_html(sub_pages):
    pages = ['<ul>']
    for each in sub_pages:
        pages.append('<li><a href="%s">%s</a>' % (each['url'], escape(each['title'])))

        if each.get('children'):
            pages.extend(_flatpages_html(each.get('children')))
        pages.append('</li>')
    
    pages.append('</ul>')
    return pages

anchors_regex = re.compile('<a\s+name="(?P<hash>[\w_]+)">(?P<title>.*?)</a>')
        
def _flatpages(inside='', depth=1):
    pages = []
    
    if inside:
        qs = FlatPage.objects.filter(url__startswith=inside)
    else:
        qs = FlatPage.objects.all()
        
        
    qs = qs.order_by('title')
    for flatpage in qs:
        this_url = flatpage.url#.replace(inside, '')
        this_depth = len([x for x in this_url.split('/') if x.strip()])
        
        # the OR part is for any flat page with url='/'
        if this_depth == depth or (this_depth == 0 and depth == 1):
            url = flatpage.url
            page = dict(url=flatpage.url, 
                        title=_clean_numbered_title(flatpage.title))
            sub_pages = []
            if depth >= 1 and this_depth != 0:
                sub_pages = _flatpages(inside=this_url, depth=depth+1)
                
            if not sub_pages:
                for anchor in anchors_regex.findall(flatpage.content):
                    #print anchor
                    #print dir(anchor), type(anchor)
                    sub_pages.append(dict(url=flatpage.url+'#'+anchor[0],
                                        title=anchor[1]))
        
            if sub_pages:
                page['children'] = sub_pages
            pages.append(page)
        
        
    return pages
