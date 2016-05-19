import os

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

css_n01_common_leapfrog_main_css = NEST_ROOT_DIR + '/css/n01_common/leapfrog_main.css'
jscript_n01_common_leapfrog_utils_js = NEST_ROOT_DIR + '/jscript/n01_common/leapfrog_utils.js'
#jscript_n01_common_history_js = NEST_ROOT_DIR + '/jscript/n01_common/history/scripts/bundled/html4+html5/jquery.history.js'
html_n11_loss_triangle_common_html = NEST_ROOT_DIR + '/html/n01_common/common.html'
html_n11_loss_triangle_top_box_html = NEST_ROOT_DIR + '/html/n11_loss_triangle/top_box.html'
html_n11_loss_triangle_hidden_inputs_spinner_html = NEST_ROOT_DIR + '/html/n11_loss_triangle/hidden_inputs_spinner.html'
html_n11_loss_triangle_filters_dialog_box_html = NEST_ROOT_DIR + '/html/n11_loss_triangle/filters_dialog_box.html'
jscript_n01_common_highcharts_js = NEST_ROOT_DIR + '/jscript/n01_common/highcharts/highcharts.js'
jscript_n01_common_highcharts_exporting_js = NEST_ROOT_DIR + '/jscript/n01_common/highcharts/exporting.js'
jscript_n01_common_jquery_js = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/jquery-1.9.1.js'
jscript_n01_common_jquery_ui_js = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/ui/jquery-ui.js'
jscript_n01_common_jquery_ui_css = NEST_ROOT_DIR + '/jscript/n01_common/jquery-ui-1.10.1/themes/base/jquery-ui.css'
image_n01_common_favicon_png = NEST_ROOT_DIR + '/image/n01_common/favicon.png'
jscript_n11_loss_triangle_loss_triangle_report_js = NEST_ROOT_DIR + '/jscript/n11_loss_triangle/main.js'
charts_n11_loss_triangle_loss_triangle_chart_js = NEST_ROOT_DIR + '/charts/n11_loss_triangle/chart.js'
image_n01_common_ajax_loader_gif = NEST_ROOT_DIR + '/image/n01_common/ajax_loader.gif'
image_n01_common_blank_png = NEST_ROOT_DIR + '/image/n01_common/blank.png'
image_n01_common_nest_header_png = NEST_ROOT_DIR + '/image/n01_common/nest_header.png'
#image_n01_common_del_red_png = NEST_ROOT_DIR + '/image/n01_common/del_red_bg.png'
image_n01_common_del_red_png = NEST_ROOT_DIR + '/image/n01_common/del_blue_bg.png'
#image_n01_common_del_gray_png = NEST_ROOT_DIR + '/image/n01_common/del_gray_bg.png'
image_n01_common_del_gray_png = NEST_ROOT_DIR + '/image/n01_common/blank_18px.png'

MAX_NUMBER_OF_VINTAGES = 10

#Add the filters on the loss triangle page here
LOSS_TRIANGLE_FILTERS_LIST = ['Vintage','BRM Bad','Chosen Funding Source','CRM Segment','Flows','Receiver Class','Receiver Region','Sender Region']

LOSS_TRIANGLE_REPORT_FILTERS = {
        'Vintage':[],
        'Flows':[],
        'Sender Region': ['All','NA','EMEA','APAC','LATAM'],
        'Receiver Region': ['All','NA','EMEA','APAC','LATAM'],
        'Receiver Class': ['All','CAT 99','USPS','OTHER'],
        'Txn Class':['VT','DCC','WAX','MEMBER','All'],
        'Chosen Funding Source': ['All','3PC','iBANK','BAL','eCHECK','OTHER'],
        'CRM Segment': ['All','Guest','Young','Casual','Top'],
        'BRM Bad':['All','ATO','CC','ACH','8 - OTH CHARGEBACK','No Tag'],
}

FILTERS_COLUMN_MAP = {
        'Sender Region': 'sndr_region',
        'Receiver Region': 'rcvr_region',
        'Receiver Class': 'rcvr_class',
        'Txn Class': 'txn_class',
        'Chosen Funding Source': 'chosen_funding_source',
        'CRM Segment': 'e2e_segment',
}

FLOW_FILTERS_COLUMN_MAP = {
        'Is Mobile': 'is_mobile_t_f',
        'Is SendMoney': 'is_send_money_t_f',
        'Is OnEbay': 'is_on_ebay_t_f',
        'Is FirstTxn': 'is_1st_pmt_sent_t_f',
        'Is XBDR': 'is_xbdr_t_f',
}

BRM_BAD_SUBTYPE_FILTERS_LIST = ['ACH','ATO','CC']

BRM_BAD_SUBTYPE_FILTERS = {
    'ACH': ['5 - ACH FRAUD','6 - ACH NSF','7 - ACH OTHER RETURN'],
    'ATO': ['1 - ATO CLAIM OR AFR','2 - ATO RESTRICTION'],
    'CC': ['3 - STOLEN CC CHARGEBACK','4 - UNAUTH RESTRICTION'],
    '8 - OTH CHARGEBACK':['8_OTH_CB'],
    'No Tag':['N/A'],
}

ACH_FILTERS = ['5 - ACH FRAUD','6 - ACH NSF','7 - ACH OTHER RETURN']

ATO_FILTERS = ['1 - ATO CLAIM OR AFR','2 - ATO RESTRICTION']

CC_FILTERS = ['3 - STOLEN CC CHARGEBACK','4 - UNAUTH RESTRICTION']

FLOWS_FILTERS_LIST = ['Is OnEbay','Is Mobile','Is SendMoney','Is FirstTxn','Is XBDR']

FLOWS_FILTERS = {
        'Is Mobile': ['Yes','No','Both'],
        'Is SendMoney': ['Yes','No','Both'],
        'Is OnEbay': ['Yes','No','Both'],
        'Is FirstTxn': ['Yes','No','Both'],
        'Is XBDR': ['Yes','No','Both'],
}

BRM_BAD_SUBTYPE_MAP = {
        '1 - ATO CLAIM OR AFR':'1_ATO_CLAIM_OR_AFR',
        '2 - ATO RESTRICTION':'2_ATO_RESTR',
        '3 - STOLEN CC CHARGEBACK':'3_STOLEN_CC_CB',
        '4 - UNAUTH RESTRICTION':'4_UNAUTH_RESTR',
        '5 - ACH FRAUD':'5_ACH_FRAUD',
        '6 - ACH NSF':'6_ACH_NSF',
        '7 - ACH OTHER RETURN':'7_ACH_OTH_RET',
        '8 - OTH CHARGEBACK':'8_OTH_CB',
        'No Tag':'N/A',
}

BRM_BAD_SUBTYPE_CHAR_MAP = {
        '1':'1_ATO_CLAIM_OR_AFR',
        '2':'2_ATO_RESTR',
        '3':'3_STOLEN_CC_CB',
        '4':'4_UNAUTH_RESTR',
        '5':'5_ACH_FRAUD',
        '6':'6_ACH_NSF',
        '7':'7_ACH_OTH_RET',
        '8 - OTH CHARGEBACK':'8_OTH_CB',
        'No Tag':'N/A',
}

FLOW_MAP = {
        'No':'0',
        'Yes':'1',
}

#Loss Triangle main query column names to row numbers mapping
SQL_COLUMN_NAME_NUMBER_MAP = {
        'txn_vintage_wk_end_dt':0,
        'bad_vintage_wk_num':1,
        'tot_ncg_txn_cnt':2,
        'tot_cg_3PC_txn_cnt':3,
        'tot_cg_ACH_txn_cnt':4,
        'tot_ncg_usd_amt':5,
        'tot_cg_3PC_usd_amt':6,
        'tot_cg_ACH_usd_amt':7,
        'gLOSS_ncg_txn_cnt_rate':8,
        'gLOSS_cg_3pc_txn_cnt_rate':9,
        'gLOSS_cg_ach_txn_cnt_rate':10,
        'gLOSS_ncg_usd_amt_rate':11,
        'gLOSS_cg_3pc_usd_amt_rate':12,
        'gLOSS_cg_ach_usd_amt_rate':13,
        'nLOSS_ncg_usd_amt_rate':14,
        'nLOSS_cg_3pc_usd_amt_rate':15,
        'nLOSS_cg_ach_usd_amt_rate':16,
}
