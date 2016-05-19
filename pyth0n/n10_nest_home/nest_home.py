from django.http import HttpResponse,HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.mail import send_mail,EmailMessage
from django.db.models import Max
from django import forms
from django.core import serializers
from django.db.models.loading import get_model
from django.utils.safestring import SafeString

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

import re, itertools, urllib2, base64, json, random, os, datetime, collections, pytz, MySQLdb

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import_common_globals = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['globals'], 0).globals
import_nest_globals = __import__('%s.pyth0n.n10_nest_home' % NEST_ROOT_DIR, globals(), locals(), ['nest_globals'], 0).nest_globals
import_nest_utils = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['utils'], 0).utils
import_loss_triangle_main_view = __import__('%s.pyth0n.n11_loss_triangle' % NEST_ROOT_DIR, globals(), locals(), ['main'], 0).main
import_loss_triangle_glossary_view = __import__('%s.pyth0n.n11_loss_triangle' % NEST_ROOT_DIR, globals(), locals(), ['glossary'], 0).glossary
import_daily_snapshot_view = __import__('%s.pyth0n.n12_daily_snapshot' % NEST_ROOT_DIR, globals(), locals(), ['daily_snapshot_view'], 0).daily_snapshot_view
import_pos_dashboard_view = __import__('%s.pyth0n.n14_pos_dashboard' % NEST_ROOT_DIR, globals(), locals(), ['pos_dashboard_view'], 0).pos_dashboard_view
import_useful_link_view = __import__('%s.pyth0n.n13_useful_link' % NEST_ROOT_DIR, globals(), locals(), ['useful_link_view'], 0).useful_link_view
import_nest_survey_view = __import__('%s.pyth0n.n15_nest_survey' % NEST_ROOT_DIR, globals(), locals(), ['main'], 0).main
import_project_tracker_main_view = __import__('%s.pyth0n.project_tracker' % NEST_ROOT_DIR, globals(), locals(), ['main'], 0).main
import_home_page_sql = __import__('%s.sql.n10_nest_home' % NEST_ROOT_DIR, globals(), locals(), ['home_page_query'], 0).home_page_query

def home_page_view(request):
    #import_nest_utils.store_session_details(request)
    kwargs = {}
    import_nest_utils.populate_header(request,kwargs)
    kwargs['root'] = NEST_ROOT_DIR

    kwargs['css_n01_common_leapfrog_main_css'                                      ] = NEST_ROOT_DIR + '/css/n01_common/leapfrog_main.css'
    kwargs['css_n01_common_jquery_ui_themes_1_10_1_themes_smoothness_jquery_ui_css'] = NEST_ROOT_DIR + '/css/n01_common/jquery-ui-themes-1.10.1/themes/smoothness/jquery-ui.css'

    kwargs['jscript_n01_common_leapfrog_utils_js'               ] = NEST_ROOT_DIR + '/jscript/n01_common/leapfrog_utils.js'

    kwargs['jscript_n01_common_highcharts_highcharts_js'        ] = NEST_ROOT_DIR + '/jscript/n01_common/highcharts/highcharts.js'
    kwargs['jscript_n01_common_highcharts_modules_exporting_js' ] = NEST_ROOT_DIR + '/jscript/n01_common/highcharts/modules/exporting.js'

    kwargs['jscript_n01_common_jquery_ui_1_10_1_jquery_1_9_1_js'] = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/jquery-1.9.1.js'
    kwargs['jscript_n01_common_jquery_ui_1_10_1_ui_jquery_ui_js'] = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/ui/jquery-ui.js'

    kwargs['image_n01_common_favicon_png'] = NEST_ROOT_DIR + '/image/n01_common/favicon.png'
    kwargs['image_n01_common_paypal_png'] = NEST_ROOT_DIR + '/image/n01_common/paypal.png'
    kwargs['image_n01_common_nest_png'] = NEST_ROOT_DIR + '/image/n01_common/nest.png'

    kwargs['title'] = "Nest"
    kwargs['root_url'] = import_common_globals.NEST_ROOT_URL
    #print 'root url is '+kwargs['root_url']
    if 'REMOTE_USER' in request.META:
        user = request.META['REMOTE_USER']
        kwargs['user'] = user
    elif 'USERNAME' in request.META:
        user = request.META['USERNAME']
        kwargs['user'] = user
    #if NEST_ROOT_DIR != 'prod':
    #    if kwargs['user'] not in import_common_globals.USERNAMES.keys():
    #        return HttpResponseRedirect('/')
    kwargs['leapfrog_list'] = import_nest_globals.LEAPFROG_LIST[:]
    kwargs['leapfrog_links_list'] = []
    for key in import_nest_globals.LEAPFROG_LIST:
        kwargs['leapfrog_links_list'].append((key,import_nest_globals.LEAPFROG_LINKS_DICT[key][0]))
    kwargs['crm_mgmt_list'] = []
    for key in import_nest_globals.CRM_MGMT_LIST:
        kwargs['crm_mgmt_list'].append((key,import_nest_globals.CRM_MGMT[key][0]))
    kwargs['useful_links_list'] = []
    for key in import_nest_globals.USEFUL_LINKS.keys():
        kwargs['useful_links_list'].append((key,'useful_link/'+key))
    dt_tpv = []
    dt_units = []
    tpv_a = []
    tpv_d = []
    tpv_f = []
    tpv_units_a = []
    tpv_units_d = []
    tpv_units_f = []
    conv=MySQLdb.converters.conversions.copy()
    conv[246]=float    # convert decimals to floats
    conv[10]=str    # convert date to str
    con = MySQLdb.connect(import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['host'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['username'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['password'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name'], conv=conv)
    attempt_status_sql = import_home_page_sql.home_page_sql
    cursor = con.cursor()
    cursor.execute(attempt_status_sql)
    attempt_status_rows = cursor.fetchall()
    cursor.close()
    seen = set()
    nd_tpv_rows = [i for i in attempt_status_rows if i[0] not in seen and not seen.add(i[0])]
    for r in nd_tpv_rows:
        dt_tpv.append(r[0])
        dt_units.append(r[0])
        tpv_a.append(r[4])
        tpv_d.append(r[5])
        tpv_f.append(r[6])
        tpv_units_a.append(r[1])
        tpv_units_d.append(r[2])
        tpv_units_f.append(r[3])
    chart1_json_x = {
                        "name": "Month",
                        "data":dt_tpv
                    }
    chart1_json_data = [{
                            "data": tpv_a,
                        },{
                            "data": tpv_d,
                        },{
                            "data": tpv_f,
                        }
                        ]
    chart2_json_x = {
                        "name": "Month",
                        "data":dt_units
                    }
    chart2_json_data = [{
                            "name": "Approved",
                            "type": "column", # "type": "column" for a multiple axes
                            "data": tpv_units_a,
                            #"tooltip": {"valuePrefix":'$'}
                        },{
                            "name": "Decline",
                            "type": "column",
                            "color": '#FF8040',
                            "data": tpv_units_d,
                            #"tooltip": {"valuePrefix":'$'}
                        },{
                            "name": "Drop-off",
                            "type": "column",
                            "color": '#FF8040',
                            "data": tpv_units_f,
                            #"tooltip": {"valuePrefix":'$'}
                        }
                        ]
    kwargs['chart1_data'] = json.dumps(chart1_json_data)
    kwargs['chart1_x'] = json.dumps(chart1_json_x)
    kwargs['chart2_data'] = json.dumps(chart2_json_data)
    kwargs['chart2_x'] = json.dumps(chart2_json_x)
    return render_to_response(NEST_ROOT_DIR + '/html/n10_nest_home/home_page.html',{'kwargs':kwargs}, RequestContext(request))


def loss_triangle_report_view(request,filters=""):
    return import_loss_triangle_main_view.view(request,filters)


def update_loss_triangle_report_ajax(request):
    return import_loss_triangle_main_view.ajax(request)


def loss_triangle_glossary_view(request):
    return import_loss_triangle_glossary_view.glossary_view(request)


def loss_triangle_alternate_view_view(request):
    return import_loss_triangle_main_view.view(request)


def update_loss_triangle_report_alternate_view_ajax(request):
    return import_loss_triangle_main_view.alternate_view_ajax(request)


def daily_snapshot_view(request):
    return import_daily_snapshot_view.daily_snapshot_view(request)


def pos_dashboard_view(request):
    return import_pos_dashboard_view.pos_dashboard_view(request)


def useful_link_view(request, link=""):
    return import_useful_link_view.useful_link_view(request,link)


def nest_survey_view(request):
    return import_nest_survey_view.view(request)


def nest_survey_submitted_view(request):
    return import_nest_survey_view.nest_survey_submitted_view(request)

def project_tracker_view(request,filters=""):
    return import_project_tracker_main_view.view(request)

def project_tracker_initiatives_view(request,filters=""):
    return import_project_tracker_main_view.initiatives_view(request)

def project_tracker_tickets_list(request,filters=""):
    return import_project_tracker_main_view.TicketList(request)
	
def project_tracker_initiatives_list(request,filters=""):
    return import_project_tracker_main_view.InitiativeList(request)
	
def project_tracker_milestones_list(request,InitiativeID=""):
    return import_project_tracker_main_view.MilestoneList(request)	

def page_not_found_view(request,trashyurl=""):
    #import_nest_utils.store_session_details(request,trashyurl)
    kwargs = {}
    import_nest_utils.populate_header(request,kwargs)
    kwargs['title'] = '404'
    kwargs['root'] = NEST_ROOT_DIR
    kwargs['css_n01_common_leapfrog_main_css'] = NEST_ROOT_DIR + '/css/n01_common/leapfrog_main.css'
    kwargs['image_n01_common_favicon_png'] = NEST_ROOT_DIR + '/image/n01_common/favicon.png'
    kwargs['image_n01_common_blank_png'] = NEST_ROOT_DIR + '/image/n01_common/blank.png'
    kwargs['image_n01_common_nest_header_png'] = NEST_ROOT_DIR + '/image/n01_common/nest_header.png'
    kwargs['root_url'] = import_common_globals.NEST_ROOT_URL
    kwargs['trash'] = trashyurl
    return render_to_response(NEST_ROOT_DIR + '/html/n01_common/error_page_404.html',{'kwargs':kwargs},RequestContext(request))

