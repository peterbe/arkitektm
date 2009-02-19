# django
from django.contrib import admin

# app
from models import ProjectCategory, Project, ProjectPhoto

class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
      'slug': ('name',),
    }
    
    ordering = ('name',)
    list_display = ('name', 'slug')
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.slug = get_slugify(obj.name, instance=obj)
        obj.save()

        
admin.site.register(ProjectCategory, ProjectCategoryAdmin)

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {
      'slug': ('name',),
    }
    ordering = ('name','current', 'add_date')
    list_filter = ['category','current']
    list_display = ('name', 'slug', 'category', 'current', 'add_date')
    
    
    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.slug = get_slugify(obj.name, instance=obj)
        obj.save()


admin.site.register(Project, ProjectAdmin)

class ProjectPhotoAdmin(admin.ModelAdmin):
    ordering = ('title','add_date')
    list_display = ('title', 'project', 'add_date')
    list_filter = ['project']
    
    def save_model(self, request, obj, form, change):
        if obj.order == 1:
            other_orders = [x.order for x in ProjectPhoto.objects.filter(project=obj.project)]
            if other_orders:
                obj.order = max(other_orders) + 1
            else:
                obj.order = 1
        obj.save()
    
admin.site.register(ProjectPhoto, ProjectPhotoAdmin)
