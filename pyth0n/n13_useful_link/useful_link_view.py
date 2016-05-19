from django.http import HttpResponse,HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
import os

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import_nest_globals = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['globals'], 0).globals
import_useful_link_globals = __import__('%s.pyth0n.n13_useful_link' % NEST_ROOT_DIR, globals(), locals(), ['useful_link_globals'], 0).useful_link_globals
import_nest_utils = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['utils'], 0).utils

def useful_link_view(request,link=""):
    import_nest_utils.store_session_details(request)
    kwargs = {}
    import_nest_utils.populate_header(request,kwargs)
    kwargs['root'] = NEST_ROOT_DIR
    kwargs['css_n01_common_leapfrog_main_css'] = NEST_ROOT_DIR + '/css/n01_common/leapfrog_main.css'
    kwargs['image_n01_common_favicon_png'] = NEST_ROOT_DIR + '/image/n01_common/favicon.png'
    kwargs['image_n01_common_blank_png'] = NEST_ROOT_DIR + '/image/n01_common/blank.png'
    kwargs['image_n01_common_nest_header_png'] = NEST_ROOT_DIR + '/image/n01_common/nest_header.png'
    kwargs['title'] = link
    kwargs['link_name'] = link
    kwargs['url'] = import_useful_link_globals.USEFUL_LINKS[link][0]
    kwargs['root_url'] = import_nest_globals.NEST_ROOT_URL
    return render_to_response(NEST_ROOT_DIR + '/html/n13_useful_link/useful_link.html',{'kwargs':kwargs},RequestContext(request))
