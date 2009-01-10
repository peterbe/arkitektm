# python
import os
import datetime
from pprint import pprint

# djano
from django.http import HttpResponse, HttpResponseRedirect,  Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test

# project
from models import ProjectCategory, Project, ProjectPhoto


################################################################################
def _render(template, data, request):
    return render_to_response(template, data,
                                  context_instance=RequestContext(request))


# Create your views here.

def home_page(request):
    return _render('home.html', locals(), request)

def projects_page(request):
    projects = Project.objects.all().order_by('add_date')
    return _render('projects.html', locals(), request)