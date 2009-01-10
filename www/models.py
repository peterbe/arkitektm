# python
from cgi import escape
import os
import datetime

# django
from django.db import models
from django.template.defaultfilters import filesizeformat
#from django.template.defaultfilters import slugify as django_slugify

# app
from utils import slugify
from settings import MEDIA_ROOT

################################################################################

def _show_description(text):
    return escape(text).replace('\n','<br/>\n')

################################################################################

class ProjectCategory(models.Model):
    """
    A category for the projects. Very simple:
    
        >>> c = ProjectCategory.objects.create(name=u'Apa')
        >>> c.name
        u'Apa'
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField('Slug', blank=True)

    class Meta:
        verbose_name_plural = u'Kategorier'
        verbose_name = u'Kategori'
        db_table = u'project_categories'

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs and 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs['name'])
        super(ProjectCategory, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.name


class Project(models.Model):
    """
    A project holds information and photos. Basically a project
    is a name, description, date, current and category. Simple test:
    
        >>> p = Project.objects.create(name=u'G\xf6tt')
        >>> p.current
        True
        >>> p.get_absolute_url()
        u'/projekt/Gott/'
        >>> import datetime
        >>> today = datetime.datetime.now()
        >>> p.add_date.year == today.year
        True
        >>> p.add_date.month == today.month
        True
        >>> p.add_date.day == today.day
        True
        >>> p.description
        u''
        
    If you first add a category you can set that on a project:
    
        >>> c = ProjectCategory.objects.create(name=u'Ost')
        >>> p = Project.objects.create(name=u'France', category=c)
        >>> p.category.name
        u'Ost'
        
    If the description contains newlines and HTML you can use show_description():
    
        >>> p.description = u'<script>'
        >>> p.save()
        >>> p.show_description()
        u'&lt;script&gt;'
    
        

    """
    
    name = models.CharField(max_length=100)
    slug = models.SlugField('Slug', blank=True)
    
    category = models.ForeignKey(ProjectCategory, blank=True, null=True)
    
    description = models.TextField(default=u'')
    
    current = models.BooleanField(default=True)
    
    add_date = models.DateTimeField('date added', default=datetime.datetime.now)
    modify_date = models.DateTimeField('date modified', auto_now=True)
    

    class Meta:
        verbose_name_plural = u'Projekt'
        verbose_name = u'Projekt'
        db_table = u'projects'

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs and 'slug' not in kwargs:
            kwargs['slug'] = slugify(kwargs['name'])
        super(Project, self).__init__(*args, **kwargs)
        
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        if self.slug:
            return '/projekt/%s/' % self.slug
        else:
            return '/projekt/%s/' % self.id
        
    def get_photos(self):
        return ProjectPhoto.objects.filter(project=self).order_by('order')

    def show_description(self):
        return self.description and _show_description(self.description) or u''

        
        
def _upload_to(instance, filename):
    from string import zfill
    next_id = ProjectPhoto.objects.all().count()
    home = os.path.join(ProjectPhoto.UPLOAD_PATH, zfill(next_id, 4))
    filename = base_filename = os.path.join(MEDIA_ROOT, home, filename)
    c = 0
    while os.path.isfile(filename):
        c += 1
        pre, post = os.path.splitext(base_filename)
        pre += '-%s' % c
        filename = pre + post
        
    return filename.replace(MEDIA_ROOT+'/', '')
    
class ProjectPhoto(models.Model):
    """
    A project can contain multiple photos. First create a project:
    
        >>> p = Project.objects.create(name=u'Hus')

    Before we can create a photo we have to create an actual image:
    
        >>> import PIL
        >>> from PIL import Image
        >>> img = Image.new('RGB', (100, 200), 0xffffff)
        >>> from cStringIO import StringIO
        >>> img.save('/tmp/projectphoto.png', 'png')    
        
    Then create a photo inside it:
    
        >>> b = ProjectPhoto.objects.create(project=p, title=u'Bild f\xf6rst')
        >>> b.get_absolute_url()
        u'/projekt/Hus/bild/1/'
        
    If you add multiple photos you can control the order:
    
        >>> b2 = ProjectPhoto.objects.create(project=p, title=u'Tva')
        >>> b3 = ProjectPhoto.objects.create(project=p, title=u'Tre')
        >>> b3.move_up()
        >>> b3.move_up()
        >>> b2.move_down()
        >>> b2.move_down()
        >>> photos = [x.title for x in p.get_photos()]
        >>> photos[0]
        u'Tre'
        >>> photos[-1]
        u'Tva'
        
    """

    UPLOAD_PATH = 'project_photos'
    
    project = models.ForeignKey(Project)
    photo = models.ImageField(upload_to=_upload_to)
    title = models.CharField(max_length=200)
    description = models.TextField(default=u'')
    
    # Order so you can rearrange the order of photos for a particular frock
    order = models.PositiveIntegerField(default=1, blank=True)
    
    add_date = models.DateTimeField('date added', default=datetime.datetime.now)
    modify_date = models.DateTimeField('date modified', auto_now=True)
    

    class Meta:
        verbose_name_plural = u'Bilder'
        verbose_name = u'Bild'
        db_table = u'project_photos'

    def __repr__(self):
        return '<%s: %s %r>' % (self.__class__.__name__, self.photo.name, self.title)
    
    def __unicode__(self):
        return u'%s (%s)' % (self.title, filesizeformat(self.photo.size))
    
    def move_up(self):
        """ change the order of this FrockPhoto to be one notch higher """
        photos = ProjectPhoto.objects.filter(project=self.project).order_by('order')
        new_order = []
        position = 0
        for photo in photos:
            if photo.id == self.id:
                new_order.insert(position - 1, photo)
            else:
                new_order.insert(position, photo)
            position += 1
        for i, photo in enumerate(new_order):
            if photo.order != i:
                photo.order = i
                photo.save()
            
    def move_down(self):
        """ change the order of this FrockPhoto to be one notch higher """
        new_order = list(ProjectPhoto.objects.filter(project=self.project).order_by('order'))
        new_index = new_order.index(self) + 1
        new_order.remove(self)
        new_order.insert(new_index, self)
        
        for i, photo in enumerate(new_order):
            if photo.order != i:
                photo.order = i
                photo.save()

    def get_absolute_url(self):
        return self.project.get_absolute_url() + 'bild/%s/' % self.id
    
    def show_description(self):
        return self.description and _show_description(self.description) or u''
