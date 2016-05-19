import os

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import socket

if socket.gethostname().lower().startswith('sjd-finrs-001'):
    NEST_PROD_HOST = True
else:
    NEST_PROD_HOST = False

EMAIL_SENT = 0

NEST_DATABASE_NAME_MAP = {
    'prod'          :'nest_prod',
    'stage'         :'nest_prod',
    'dev'           :'nest_dev',
    'u_akaushik'    :'nest_u_akaushik',
    'u_gsadaram'    :'nest_u_gsadaram',
    'u_vinarne'     :'nest_u_vinarne',
    'u_virajan'     :'nest_u_virajan',
}

DB_HOST = '127.0.0.1'

NEST_DATABASE_CONNECTION_SETTINGS = {
    'host':DB_HOST,
    'username':"root",
    'password':"root1234",
    'db_name':NEST_DATABASE_NAME_MAP[NEST_ROOT_DIR]
}

if NEST_PROD_HOST:
    NEST_ROOT_URL_MAP = {
        'prod'          :'',
        'stage'         :'stage/',
        'dev'           :'dev/',
        'u_akaushik'    :'u_akaushik/',
        'u_gsadaram'    :'u_gsadaram/',
        'u_vinarne'     :'u_vinarne/',
        'u_virajan'     :'u_virajan/',
    }

else:
    NEST_ROOT_URL_MAP = {
        'prod'          :'prod/',
        'stage'         :'stage/',
        'dev'           :'',
        'u_akaushik'    :'u_akaushik/',
        'u_gsadaram'    :'u_gsadaram/',
        'u_vinarne'     :'u_vinarne/',
        'u_virajan'     :'u_virajan/',
    }

NEST_ROOT_URL = NEST_ROOT_URL_MAP[NEST_ROOT_DIR]

IP_ADDRESSES_TO_IGNORE = []
#IP_ADDRESSES_TO_IGNORE = ['127.0.0.1']

USERNAMES = {
    'akaushik':'Atulesh Kaushik',
    'gsadaram':'Gangadhar Sadaram',
    'virajan':'Vikas Rajan',
    'vinarne':'Vidya Narne',
}

css_n01_common_leapfrog_main_css = NEST_ROOT_DIR + '/css/n01_common/leapfrog_main.css'
css_n01_common_jquery_ui_themes_1_10_1_themes_smoothness_jquery_ui_css = NEST_ROOT_DIR + '/css/n01_common/jquery-ui-themes-1.10.1/themes/smoothness/jquery-ui.css'
jscript_n01_common_leapfrog_utils_js = NEST_ROOT_DIR + '/jscript/n01_common/leapfrog_utils.js'
#jscript_n01_common_history_js = NEST_ROOT_DIR + '/jscript/n01_common/history/scripts/bundled/html4+html5/jquery.history.js'
html_n01_common_common_html = NEST_ROOT_DIR + '/html/n01_common/common.html'
jscript_n01_common_highcharts_highcharts_js = NEST_ROOT_DIR + '/jscript/n01_common/highcharts/highcharts.js'
jscript_n01_common_highcharts_modules_exporting_js = NEST_ROOT_DIR + '/jscript/n01_common/highcharts/modules/exporting.js'
jscript_n01_common_jquery_ui_1_10_1_jquery_1_9_1_js = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/jquery-1.9.1.js'
jscript_n01_common_jquery_ui_1_10_1_ui_jquery_ui_js = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/ui/jquery-ui.js'
jscript_n01_common_jquery_ui_css = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/themes/base/jquery-ui.css'
image_n01_common_favicon_png = NEST_ROOT_DIR + '/image/n01_common/favicon.png'
image_n01_common_ajax_loader_gif = NEST_ROOT_DIR + '/image/n01_common/ajax_loader.gif'
image_n01_common_blank_png = NEST_ROOT_DIR + '/image/n01_common/blank.png'
image_n01_common_nest_header_png = NEST_ROOT_DIR + '/image/n01_common/nest_header.png'
#image_n01_common_del_red_png = NEST_ROOT_DIR + '/image/n01_common/del_red_bg.png'
image_n01_common_del_red_png = NEST_ROOT_DIR + '/image/n01_common/del_blue_bg.png'
#image_n01_common_del_gray_png = NEST_ROOT_DIR + '/image/n01_common/del_gray_bg.png'
image_n01_common_del_gray_png = NEST_ROOT_DIR + '/image/n01_common/blank_18px.png'