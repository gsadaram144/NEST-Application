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
import_main_query = __import__('%s.sql.n11_loss_triangle' % NEST_ROOT_DIR, globals(), locals(), ['main_query'], 0).main_query
import_dates_query = __import__('%s.sql.n11_loss_triangle' % NEST_ROOT_DIR, globals(), locals(), ['dates_query'], 0).dates_query

#Function to render the html
def view(request,filters=''):
    #Log Session details
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = 'URL from browser'
    import_nest_utils.store_session_details(request,url)

    kwargs = {}
    import_nest_utils.populate_header(request,kwargs)

    kwargs['root'] = NEST_ROOT_DIR
    kwargs['root_url'] = import_common_globals.NEST_ROOT_URL
    if 'REMOTE_USER' in request.META:
        kwargs['user'] = request.META['REMOTE_USER']
    elif 'USERNAME' in request.META:
        kwargs['user'] = request.META['USERNAME']

    #Initialize variables with static files to be imported in html
    kwargs['css_n01_common_leapfrog_main_css'] = import_loss_triangle_globals.css_n01_common_leapfrog_main_css
    kwargs['jscript_n01_common_leapfrog_utils_js'] = import_loss_triangle_globals.jscript_n01_common_leapfrog_utils_js
    #kwargs['jscript_n01_common_history_js'] = import_loss_triangle_globals.jscript_n01_common_history_js
    kwargs['html_n11_loss_triangle_common_html'] = import_loss_triangle_globals.html_n11_loss_triangle_common_html
    kwargs['html_n11_loss_triangle_top_box_html'] = import_loss_triangle_globals.html_n11_loss_triangle_top_box_html
    kwargs['html_n11_loss_triangle_hidden_inputs_spinner_html'] = import_loss_triangle_globals.html_n11_loss_triangle_hidden_inputs_spinner_html
    kwargs['html_n11_loss_triangle_filters_dialog_box_html'] = import_loss_triangle_globals.html_n11_loss_triangle_filters_dialog_box_html
    kwargs['jscript_n01_common_highcharts_js'] = import_loss_triangle_globals.jscript_n01_common_highcharts_js
    kwargs['jscript_n01_common_highcharts_exporting_js'] = import_loss_triangle_globals.jscript_n01_common_highcharts_exporting_js
    kwargs['jscript_n01_common_jquery_js'] = import_loss_triangle_globals.jscript_n01_common_jquery_js
    kwargs['jscript_n01_common_jquery_ui_js'] = import_loss_triangle_globals.jscript_n01_common_jquery_ui_js
    kwargs['jscript_n01_common_jquery_ui_css'] = import_loss_triangle_globals.jscript_n01_common_jquery_ui_css
    kwargs['image_n01_common_favicon_png'] = import_loss_triangle_globals.image_n01_common_favicon_png
    kwargs['jscript_n11_loss_triangle_loss_triangle_report_js'] = import_loss_triangle_globals.jscript_n11_loss_triangle_loss_triangle_report_js
    kwargs['charts_n11_loss_triangle_loss_triangle_chart_js'] = import_loss_triangle_globals.charts_n11_loss_triangle_loss_triangle_chart_js
    kwargs['image_n01_common_ajax_loader_gif'] = import_loss_triangle_globals.image_n01_common_ajax_loader_gif
    kwargs['image_n01_common_blank_png'] = import_loss_triangle_globals.image_n01_common_blank_png
    kwargs['image_n01_common_nest_header_png'] = import_loss_triangle_globals.image_n01_common_nest_header_png
    kwargs['image_n01_common_del_red_png'] = import_loss_triangle_globals.image_n01_common_del_red_png
    kwargs['image_n01_common_del_gray_png'] = import_loss_triangle_globals.image_n01_common_del_gray_png

    #Initialize variables with filters to be displayed in the html
    kwargs['shared_filters'] = filters
    kwargs['report_filters'] = []
    kwargs['brm_subtype_filters'] = []
    kwargs['flow_filters'] = []
    kwargs['brm_bad_subtype_map'] = []
    for key in import_loss_triangle_globals.LOSS_TRIANGLE_FILTERS_LIST:
        kwargs['report_filters'].append((key,import_loss_triangle_globals.LOSS_TRIANGLE_REPORT_FILTERS[key]))
    for key in import_loss_triangle_globals.FLOWS_FILTERS_LIST:
        kwargs['flow_filters'].append((key,import_loss_triangle_globals.FLOWS_FILTERS[key]))
    for key in import_loss_triangle_globals.BRM_BAD_SUBTYPE_FILTERS_LIST:
        kwargs['brm_subtype_filters'].append((key,import_loss_triangle_globals.BRM_BAD_SUBTYPE_FILTERS[key]))
    for key in sorted(import_loss_triangle_globals.BRM_BAD_SUBTYPE_MAP.keys()):
        kwargs['brm_bad_subtype_map'].append(key)
    kwargs['ach_filters'] = import_loss_triangle_globals.ACH_FILTERS[:]
    kwargs['ato_filters'] = import_loss_triangle_globals.ATO_FILTERS[:]
    kwargs['cc_filters'] = import_loss_triangle_globals.CC_FILTERS[:]
    kwargs['txn_class_values'] = import_loss_triangle_globals.LOSS_TRIANGLE_REPORT_FILTERS['Txn Class'][:]

    #Get all the Week Ending Dates
    conv=MySQLdb.converters.conversions.copy()
    conv[246]=float    # convert decimals to floats
    conv[10]=str    # convert date to str
    con = MySQLdb.connect(import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['host'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['username'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['password'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name'], conv=conv)
    cursor = con.cursor()
    dates_query = import_dates_query.dates_query % {'db_name':import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name']}
    cursor.execute(dates_query)
    week_ending_date_rows = cursor.fetchall()
    week_ending_date_rows = [i[0] for i in week_ending_date_rows if i[0] != ""]
    kwargs['week_ending_date_rows'] = week_ending_date_rows[:]
    kwargs['first_uds_date'] = week_ending_date_rows[0]
    week_ending_date_rows = week_ending_date_rows[-13:]
    kwargs['start_date'] = week_ending_date_rows[0]
    kwargs['current_date'] = week_ending_date_rows[-1]
    kwargs['current_date_day'] = (datetime.datetime.strptime(week_ending_date_rows[-1],'%Y-%m-%d').weekday() + 1) % 7
    kwargs['max_vintages'] = import_loss_triangle_globals.MAX_NUMBER_OF_VINTAGES
    kwargs['vintage_selection_list'] = range(7,27)

    if 'alternate_view' in request.path:
        kwargs['title'] = 'Loss Triangle Alternate View'
        kwargs['ajax_url'] = "update_loss_triangle_report_alternate_view_ajax/"
    else:
        kwargs['title'] = 'Loss Triangle'
        kwargs['ajax_url'] = "update_loss_triangle_report_ajax/"
    return render_to_response(NEST_ROOT_DIR + '/html/n11_loss_triangle/main.html',{'kwargs':kwargs},RequestContext(request))


#Function to send the data for the charts
def ajax(request):
    
    response_from_query = getQueryResult(request)
    populated_tpv_values = populateTpvValues(response_from_query)

    #Parse result of query and create a JSON object with chart data
    loss_ncg_dict = {}
    units_ncg_dict = {}
    net_loss_ncg_dict = {}
    loss_cg_dict = {}
    units_cg_dict = {}
    net_loss_cg_dict = {}
    if request.GET['Number of bad weeks']:
        num_of_bad_weeks = int(request.GET['Number of bad weeks'])
    else:
        num_of_bad_weeks = 13
    for date in response_from_query['vintage_date_rows']:
        if response_from_query['ach_flag_funding_src'] == 1 or response_from_query['ach_flag_brm_bad'] == 1:
            loss_cg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_ach_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
            units_cg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_ach_txn_cnt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
            net_loss_cg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['nLOSS_cg_ach_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
        else:
            loss_cg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_3pc_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
            units_cg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_3pc_txn_cnt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
            net_loss_cg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['nLOSS_cg_3pc_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
        loss_ncg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_ncg_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
        units_ncg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_ncg_txn_cnt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
        net_loss_ncg_dict[date] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['nLOSS_ncg_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']] == date and 0<=l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]<=(num_of_bad_weeks-1)]
        
    chart_json_data = [ {
                            'type':'tpv',
                            'series':[{
                                        "name": 'NCG',
                                        "data": populated_tpv_values['tpv_ncg']
                                    },{
                                        "name": 'CG',
                                        "data": populated_tpv_values['tpv_cg']
                                    }],
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'$TPV (millions)',
                            'x_text':'Week Ending Date',
                            'y_text':'TPV',
                            'tooltip_unit':'$',
                        },{
                            'type':'vintage',
                            'series':createChartJsonData(loss_ncg_dict,hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':range(1,num_of_bad_weeks+1),
                            'title':'NCG: $gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text':'gLoss Rate',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'vintage',
                            'series':createChartJsonData(loss_cg_dict,hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':range(1,num_of_bad_weeks+1),
                            'title':'CG: $gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text':'gLoss Rate',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'vintage',
                            'series':createChartJsonData(net_loss_ncg_dict,hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':range(1,num_of_bad_weeks+1),
                            'title':'NCG: $nLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text':'nLoss Rate',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'vintage',
                            'series':createChartJsonData(net_loss_cg_dict,hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':range(1,num_of_bad_weeks+1),
                            'title':'CG: $nLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text':'nLoss Rate',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'tpv',
                            'series':[{
                                        "name": 'NCG',
                                        "data": populated_tpv_values['tpv_units_ncg']
                                    },{
                                        "name": 'CG',
                                        "data": populated_tpv_values['tpv_units_cg']
                                    }],
                            'categories':populated_tpv_values['dt_units'],
                            'title':'# of Txn (units, millions)',
                            'x_text':'Week Ending Date',
                            'y_text':'Units',
                            'tooltip_unit':'',
                        },{
                            'type':'vintage',
                            'series':createChartJsonData(units_ncg_dict,hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':range(1,num_of_bad_weeks+1),
                            'title':'NCG: Unit gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text':'gLoss Rate',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'vintage',
                            'series':createChartJsonData(units_cg_dict,hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':range(1,num_of_bad_weeks+1),
                            'title':'CG: Unit gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text':'gLoss Rate',
                            'tooltip_series_name':'Week Ending Vintage',
                        }]
    return HttpResponse(json.dumps(chart_json_data))
    
    
def alternate_view_ajax(request):
    
    response_from_query = getQueryResult(request)
    populated_tpv_values = populateTpvValues(response_from_query)

    #Parse result of query and create a JSON object with chart data
    loss_ncg_dict = {}
    units_ncg_dict = {}
    net_loss_ncg_dict = {}
    loss_cg_dict = {}
    units_cg_dict = {}
    net_loss_cg_dict = {}

    loss_ncg_dict[-1] = populated_tpv_values['tpv_ncg']
    units_ncg_dict[-1] = populated_tpv_values['tpv_units_ncg']
    net_loss_ncg_dict[-1] = populated_tpv_values['tpv_ncg']
    loss_cg_dict[-1] = populated_tpv_values['tpv_cg']
    units_cg_dict[-1] = populated_tpv_values['tpv_units_cg']
    net_loss_cg_dict[-1] = populated_tpv_values['tpv_cg']

    for bad_week in xrange(1,14):
        if response_from_query['ach_flag_funding_src'] == 1 or response_from_query['ach_flag_brm_bad'] == 1:
            loss_cg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_ach_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
            units_cg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_ach_txn_cnt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
            net_loss_cg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['nLOSS_cg_ach_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
        else:
            loss_cg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_3pc_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
            units_cg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_cg_3pc_txn_cnt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
            net_loss_cg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['nLOSS_cg_3pc_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
        loss_ncg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_ncg_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
        units_ncg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['gLOSS_ncg_txn_cnt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]
        net_loss_ncg_dict[bad_week] = [l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['nLOSS_ncg_usd_amt_rate']] for l in response_from_query['loss_triangle_rows'] if (l[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['bad_vintage_wk_num']]+1) == bad_week]

    chart_json_data = [ {
                            'type':'multipleAxes',
                            'series':createChartJsonData(loss_ncg_dict,"TPV","Loss rate week ",hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'NCG: $gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text1':'gLoss Rate',
                            'y_text2':'TPV',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'multipleAxes',
                            'series':createChartJsonData(loss_cg_dict,"TPV","Loss rate week ",hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'CG: $gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text1':'gLoss Rate',
                            'y_text2':'TPV',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'multipleAxes',
                            'series':createChartJsonData(net_loss_ncg_dict,"TPV","Loss rate week ",hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'NCG: $nLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text1':'nLoss Rate',
                            'y_text2':'TPV',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'multipleAxes',
                            'series':createChartJsonData(net_loss_cg_dict,"TPV","Loss rate week ",hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'CG: $nLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text1':'nLoss Rate',
                            'y_text2':'TPV',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'multipleAxes',
                            'series':createChartJsonData(units_ncg_dict,'# of Txns',"Loss rate week ",hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'NCG: Unit gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text1':'gLoss Rate',
                            'y_text2':'Units',
                            'tooltip_series_name':'Week Ending Vintage',
                        },{
                            'type':'multipleAxes',
                            'series':createChartJsonData(units_cg_dict,'# of Txns',"Loss rate week ",hidden_vintages=request.GET['Hidden Vintages']),
                            'categories':populated_tpv_values['dt_tpv'],
                            'title':'CG: Unit gLoss Rate (bps)',
                            'x_text':'Weeks Since Txn',
                            'y_text1':'gLoss Rate',
                            'y_text2':'Units',
                            'tooltip_series_name':'Week Ending Vintage',
                        }]
    return HttpResponse(json.dumps(chart_json_data))
    
    
#Function to populate data for vintages charts
def createChartJsonData(data_dict,metric="",name_prefix="",hidden_vintages=""):
    chart_json_data = []
    for k,v in sorted(data_dict.items()):
        series_visible = True
        hidden_vintages_split = hidden_vintages.split(',')
        if k in hidden_vintages_split:
            series_visible = False
        elif 'Loss rate week '+str(k) in hidden_vintages_split:
            series_visible = False
        if k == -1:
            nd = {
                  'type': "column",
                  #'lineWidth': 300,
                  'yAxis': 1,
                  'name': metric,
                  "color": '#BABABA',
                  'data': v,
                  'tooltip': {
                            'valueSuffix':'$'
                            }
                 }
            chart_json_data.append(nd)
        else:
            nd = {
                  'type': "line",
                  'lineWidth': 2,
                  'marker': {
                    'symbol': 'circle',
                    'lineColor': "null",
                    'radius': 3,
                    'lineWidth': 1
                  },
                  'visible': series_visible,
                  'name': name_prefix + str(k),
                  'data': v,
                  'tooltip': {
                    'valueSuffix':'bps'
                  }
                  }
            chart_json_data.append(nd)

    return chart_json_data
    
    
def getQueryResult(request):
    where_list1 = ''
    where_list2 = ''
    ach_flag_funding_src = 0
    ach_flag_brm_bad = 0
    selected_date = ''
    brm_bad_type_list = ''
    brm_bad_subtype_list = ''

    #Populate filters for the query
    for key in request.GET.keys():
        if request.GET[key].strip() != 'All':
            request_current_filter = request.GET[key].replace(', ', ',')

            if key in import_loss_triangle_globals.FILTERS_COLUMN_MAP.keys():
                if request_current_filter.strip() == 'iBANK':
                    ach_flag_funding_src = 1
                where_list1 += import_loss_triangle_globals.FILTERS_COLUMN_MAP[key]+' IN (\''+request_current_filter.replace(',', '\', \'')+'\') AND '
                where_list2 += import_loss_triangle_globals.FILTERS_COLUMN_MAP[key]+' IN (\''+request_current_filter.replace(',', '\', \'')+'\') AND '

            if 'BRM Bad' == key:
                if request_current_filter.strip() == 'ACH':
                    ach_flag_brm_bad = 1

                for brm_bad_type_item in request_current_filter.split(','):
                    if brm_bad_type_item in import_loss_triangle_globals.BRM_BAD_SUBTYPE_MAP.keys():
                        brm_bad_type_list += ', \''+import_loss_triangle_globals.BRM_BAD_SUBTYPE_MAP[brm_bad_type_item]+'\''
                        brm_bad_subtype_list += ', \''+import_loss_triangle_globals.BRM_BAD_SUBTYPE_MAP[brm_bad_type_item]+'\''
                    else:
                        brm_bad_type_list += ', \''+brm_bad_type_item+'\''

            if 'BRM Bad Subtype' == key:
                for brm_bad_subtype_item_array in request_current_filter.split(','):
                    for brm_bad_subtype_item in brm_bad_subtype_item_array.split('|'):
                        if brm_bad_subtype_item in import_loss_triangle_globals.BRM_BAD_SUBTYPE_CHAR_MAP.keys():
                            brm_bad_subtype_list += ', \''+import_loss_triangle_globals.BRM_BAD_SUBTYPE_CHAR_MAP[brm_bad_subtype_item]+'\''

            if key in import_loss_triangle_globals.FLOW_FILTERS_COLUMN_MAP.keys():
                where_list1 +=  import_loss_triangle_globals.FLOW_FILTERS_COLUMN_MAP[key] + '=' + import_loss_triangle_globals.FLOW_MAP[request_current_filter] + ' AND '
                where_list2 +=  import_loss_triangle_globals.FLOW_FILTERS_COLUMN_MAP[key] + '=' + import_loss_triangle_globals.FLOW_MAP[request_current_filter] + ' AND '

    if brm_bad_type_list != "":
        where_list1 += 'brm_bad_tag_type IN ('+brm_bad_type_list[2:]+') AND '

    if brm_bad_subtype_list != "":
        where_list1 += 'brm_bad_tag_subtype IN ('+brm_bad_subtype_list[2:]+') AND '

    if where_list1 != "":
        where_list1 = where_list1[:-5]
    else:
        where_list1 = "1=1"

    if where_list2 != "":
        where_list2 = where_list2[:-5]
    else:
        where_list2 = "2=2"

    vintages_list = request.GET['Vintage Dates'].split(' | ')

    #Get the list of dates between first and last date selected by user
    conv=MySQLdb.converters.conversions.copy()
    conv[246]=float    # convert decimals to floats
    conv[10]=str    # convert date to str
    con = MySQLdb.connect(import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['host'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['username'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['password'],import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name'], conv=conv)
    cursor = con.cursor()
    dates_query = import_dates_query.dates_query % {'db_name':import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name']}
    cursor.execute(dates_query)
    week_ending_date_rows = cursor.fetchall()
    cursor.close()
    week_ending_date_rows = [i[0] for i in week_ending_date_rows if i[0] != ""]
    vintage_date_rows = []
    for vintage in vintages_list:
        index_first_date = week_ending_date_rows.index(vintage.split('~')[0])
        index_last_date = week_ending_date_rows.index(vintage.split('~')[1])
        vintage_date_rows += week_ending_date_rows[index_first_date:index_last_date+1]
    vintage_date_rows = sorted(set(vintage_date_rows))
    vintages_str = ''
    for i in vintage_date_rows:
        vintages_str += '\''+i+'\','
    vintages_str = vintages_str[:-1]
    dates_where_list = 'txn_wk_end_dt IN ('+vintages_str+')'
    
    #Get the data for those dates and other filters
    try :
        main_query = import_main_query.main_query % {'db_name':import_common_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name'],'dates_where_list':dates_where_list, 'wherelist1':where_list1, 'wherelist2':where_list2}
        cursor = con.cursor()
        cursor.execute(main_query)
        loss_triangle_rows = cursor.fetchall()
        cursor.close()
    except:
        print "SQL error"
        
    response_from_query = {}
    response_from_query['loss_triangle_rows'] = loss_triangle_rows
    response_from_query['vintage_date_rows'] = vintage_date_rows
    response_from_query['ach_flag_funding_src'] = ach_flag_funding_src
    response_from_query['ach_flag_brm_bad'] = ach_flag_brm_bad
        
    return response_from_query
    
    
def populateTpvValues(response_from_query):
    dt_tpv = []
    dt_units = []
    tpv_ncg = []
    tpv_cg = []
    tpv_units_ncg = []
    tpv_units_cg = []
    
    loss_triangle_rows = response_from_query['loss_triangle_rows']
    ach_flag_funding_src = response_from_query['ach_flag_funding_src']
    ach_flag_brm_bad = response_from_query['ach_flag_brm_bad']
    
    seen = set()
    nd_tpv_rows = [i for i in loss_triangle_rows if i[0] not in seen and not seen.add(i[0])]
    prev_date = nd_tpv_rows[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']][0]
    for r in nd_tpv_rows:
        if (datetime.datetime.strptime(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']],'%Y-%m-%d') - datetime.datetime.strptime(prev_date,'%Y-%m-%d')).days > 7:
            dt_tpv.append('')
            dt_units.append('')
            tpv_ncg.append(None)
            tpv_cg.append(None)
            tpv_units_ncg.append(None)
            tpv_units_cg.append(None)
        dt_tpv.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']])
        dt_units.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']])
        tpv_ncg.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['tot_ncg_usd_amt']])
        if ach_flag_funding_src == 1 or ach_flag_brm_bad == 1:
            tpv_cg.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['tot_cg_ACH_usd_amt']])
            tpv_units_cg.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['tot_cg_ACH_txn_cnt']])
        else:
            tpv_cg.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['tot_cg_3PC_usd_amt']])
            tpv_units_cg.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['tot_cg_3PC_txn_cnt']])
        tpv_units_ncg.append(r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['tot_ncg_txn_cnt']])
        prev_date = r[import_loss_triangle_globals.SQL_COLUMN_NAME_NUMBER_MAP['txn_vintage_wk_end_dt']]
        
    populated_tpv_values = {}
    populated_tpv_values['dt_tpv'] = dt_tpv
    populated_tpv_values['dt_units'] = dt_units
    populated_tpv_values['tpv_ncg'] = tpv_ncg
    populated_tpv_values['tpv_cg'] = tpv_cg
    populated_tpv_values['tpv_units_ncg'] = tpv_units_ncg
    populated_tpv_values['tpv_units_cg'] = tpv_units_cg
    return populated_tpv_values