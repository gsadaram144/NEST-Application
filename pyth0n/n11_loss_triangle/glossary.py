from django.http import HttpResponse,HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core import serializers
from django.db.models.loading import get_model
from django.utils.safestring import SafeString
import re, itertools, urllib2, base64, json, random, os, datetime, collections, pytz, MySQLdb

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import_common_globals = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['globals'], 0).globals
import_loss_triangle_globals = __import__('%s.pyth0n.n11_loss_triangle' % NEST_ROOT_DIR, globals(), locals(), ['globals'], 0).globals
import_nest_utils = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['utils'], 0).utils


def glossary_view(request):
    import_nest_utils.store_session_details(request)
    kwargs = {}
    import_nest_utils.populate_header(request,kwargs)
    kwargs['root'] = NEST_ROOT_DIR
    kwargs['title'] = 'Glossary'
    kwargs['css_n01_common_leapfrog_main_css'] = import_loss_triangle_globals.css_n01_common_leapfrog_main_css
    kwargs['jscript_n01_common_leapfrog_utils_js'] = import_loss_triangle_globals.jscript_n01_common_leapfrog_utils_js
    kwargs['image_n01_common_favicon_png'] = import_loss_triangle_globals.image_n01_common_favicon_png
    kwargs['image_n01_common_blank_png'] = import_loss_triangle_globals.image_n01_common_blank_png
    kwargs['image_n01_common_nest_header_png'] = import_loss_triangle_globals.image_n01_common_nest_header_png
    kwargs['root_url'] = import_common_globals.NEST_ROOT_URL
    return render_to_response(NEST_ROOT_DIR + '/html/n11_loss_triangle/glossary.html',{'kwargs':kwargs},RequestContext(request))