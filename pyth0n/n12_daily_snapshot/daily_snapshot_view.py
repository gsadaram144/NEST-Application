from django.http import HttpResponse,HttpResponseRedirect, HttpRequest
from django.shortcuts import render_to_response
from django.template import RequestContext
import os, MySQLdb, json

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

import_nest_globals = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['globals'], 0).globals
import_nest_utils = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['utils'], 0).utils
import_daily_snapshot_sql = __import__('%s.sql.n12_daily_snapshot' % NEST_ROOT_DIR, globals(), locals(), ['daily_snapshot_query'], 0).daily_snapshot_query

def daily_snapshot_view(request):
    import_nest_utils.store_session_details(request)
    kwargs = {}
    import_nest_utils.populate_header(request,kwargs)
    kwargs['root'] = NEST_ROOT_DIR
    if 'REMOTE_USER' in request.META:
        user = request.META['REMOTE_USER']
        kwargs['user'] = user
    elif 'USERNAME' in request.META:
        user = request.META['USERNAME']
        kwargs['user'] = user
    #if NEST_ROOT_DIR != 'prod':
    #    if kwargs['user'] not in import_nest_globals.USERNAMES.keys():
    #        return HttpResponseRedirect('/')
    kwargs['css_n01_common_leapfrog_main_css'] = NEST_ROOT_DIR + '/css/n01_common/leapfrog_main.css'
    kwargs['jscript_n01_common_leapfrog_utils_js'] = NEST_ROOT_DIR + '/jscript/n01_common/leapfrog_utils.js'
    kwargs['image_n01_common_favicon_png'] = NEST_ROOT_DIR + '/image/n01_common/favicon.png'
    kwargs['jscript_n11_loss_triangle_loss_triangle_report_js'] = NEST_ROOT_DIR + '/jscript/n11_loss_triangle/loss_triangle_report.js'
    kwargs['image_n01_common_ajax_loader_gif'] = NEST_ROOT_DIR + '/image/n01_common/ajax_loader.gif'
    kwargs['image_n01_common_blank_png'] = NEST_ROOT_DIR + '/image/n01_common/blank.png'
    kwargs['image_n01_common_nest_header_png'] = NEST_ROOT_DIR + '/image/n01_common/nest_header.png'
    kwargs['root_url'] = import_nest_globals.NEST_ROOT_URL
    dt_pdmon = []
    total_attempts_amt_1 = []
    total_attempts_amt_2 = []
    total_attempts_amt_3 = []
    total_attempts_ct_1 = []
    total_attempts_ct_2 = []
    total_attempts_ct_3 = []
    risk_adj_attempts_amt_1 = []
    risk_adj_attempts_amt_2 = []
    risk_adj_attempts_amt_3 = []
    risk_adj_attempts_ct_1 = []
    risk_adj_attempts_ct_2 = []
    risk_adj_attempts_ct_3 = []
    risk_adj_auth_challenge_amt_1 = []
    risk_adj_auth_challenge_amt_2 = []
    risk_adj_auth_challenge_amt_3 = []
    risk_adj_auth_challenge_ct_1 = []
    risk_adj_auth_challenge_ct_2 = []
    risk_adj_auth_challenge_ct_3 = []
    risk_adj_decline_amt_1 = []
    risk_adj_decline_amt_2 = []
    risk_adj_decline_amt_3 = []
    risk_adj_decline_ct_1 = []
    risk_adj_decline_ct_2 = []
    risk_adj_decline_ct_3 = []
    risk_adj_processor_decline_amt_1 = []
    risk_adj_processor_decline_amt_2 = []
    risk_adj_processor_decline_amt_3 = []
    risk_adj_processor_decline_ct_1 = []
    risk_adj_processor_decline_ct_2 = []
    risk_adj_processor_decline_ct_3 = []
    risk_adj_policy_decline_amt_1 = []
    risk_adj_policy_decline_amt_2 = []
    risk_adj_policy_decline_amt_3 = []
    risk_adj_policy_decline_ct_1 = []
    risk_adj_policy_decline_ct_2 = []
    risk_adj_policy_decline_ct_3 = []
    risk_adj_card_decline_amt_1 = []
    risk_adj_card_decline_amt_2 = []
    risk_adj_card_decline_amt_3 = []
    risk_adj_card_decline_ct_1 = []
    risk_adj_card_decline_ct_2 = []
    risk_adj_card_decline_ct_3 = []
    risk_adj_bank_decline_amt_1 = []
    risk_adj_bank_decline_amt_2 = []
    risk_adj_bank_decline_amt_3 = []
    risk_adj_bank_decline_ct_1 = []
    risk_adj_bank_decline_ct_2 = []
    risk_adj_bank_decline_ct_3 = []
    risk_adj_ato_pld_amt_1 = []
    risk_adj_ato_pld_amt_2 = []
    risk_adj_ato_pld_amt_3 = []
    risk_adj_ato_pld_ct_1 = []
    risk_adj_ato_pld_ct_2 = []
    risk_adj_ato_pld_ct_3 = []
    
    conv=MySQLdb.converters.conversions.copy()
    conv[246]=float    # convert decimals to floats
    conv[10]=str    # convert date to str
    con = MySQLdb.connect(import_nest_globals.NEST_DATABASE_CONNECTION_SETTINGS['host'],import_nest_globals.NEST_DATABASE_CONNECTION_SETTINGS['username'],import_nest_globals.NEST_DATABASE_CONNECTION_SETTINGS['password'],import_nest_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name'], conv=conv)
    cursor = con.cursor()
    daily_snapshot_sql = import_daily_snapshot_sql.daily_snapshot_sql % {'db_name':import_nest_globals.NEST_DATABASE_CONNECTION_SETTINGS['db_name']}

    cursor.execute(daily_snapshot_sql)
    #print daily_snapshot_sql
    daily_snapshot_rows = cursor.fetchall()
    cursor.close()
    
    seen = set()
    nd_tpv_rows = [i for i in daily_snapshot_rows if i[0] not in seen and not seen.add(i[0])]
    for r in nd_tpv_rows:
        dt_pdmon.append(r[0])
        total_attempts_amt_1.append(r[1])
        total_attempts_amt_2.append(r[2])
        total_attempts_amt_3.append(r[3])
        total_attempts_ct_1.append(r[4])
        total_attempts_ct_2.append(r[5])
        total_attempts_ct_3.append(r[6])
        risk_adj_attempts_amt_1.append(r[7])
        risk_adj_attempts_amt_2.append(r[8])
        risk_adj_attempts_amt_3.append(r[9])
        risk_adj_attempts_ct_1.append(r[10])
        risk_adj_attempts_ct_2.append(r[11])
        risk_adj_attempts_ct_3.append(r[12])
        risk_adj_auth_challenge_amt_1.append(r[16])
        risk_adj_auth_challenge_amt_2.append(r[17])
        risk_adj_auth_challenge_amt_3.append(r[18])
        risk_adj_auth_challenge_ct_1.append(r[13])
        risk_adj_auth_challenge_ct_2.append(r[14])
        risk_adj_auth_challenge_ct_3.append(r[15])
        risk_adj_decline_amt_1.append(r[22])
        risk_adj_decline_amt_2.append(r[23])
        risk_adj_decline_amt_3.append(r[24])
        risk_adj_decline_ct_1.append(r[19])
        risk_adj_decline_ct_2.append(r[20])
        risk_adj_decline_ct_3.append(r[21])
        risk_adj_processor_decline_amt_1.append(r[28])
        risk_adj_processor_decline_amt_2.append(r[29])
        risk_adj_processor_decline_amt_3.append(r[30])
        risk_adj_processor_decline_ct_1.append(r[25])
        risk_adj_processor_decline_ct_2.append(r[26])
        risk_adj_processor_decline_ct_3.append(r[27])
        risk_adj_policy_decline_amt_1.append(r[34])
        risk_adj_policy_decline_amt_2.append(r[35])
        risk_adj_policy_decline_amt_3.append(r[36])
        risk_adj_policy_decline_ct_1.append(r[31])
        risk_adj_policy_decline_ct_2.append(r[32])
        risk_adj_policy_decline_ct_3.append(r[33])

        risk_adj_card_decline_amt_1.append(r[46])
        risk_adj_card_decline_amt_2.append(r[47])
        risk_adj_card_decline_amt_3.append(r[48])
        risk_adj_card_decline_ct_1.append(r[43])
        risk_adj_card_decline_ct_2.append(r[44])
        risk_adj_card_decline_ct_3.append(r[45])

        risk_adj_bank_decline_amt_1.append(r[52])
        risk_adj_bank_decline_amt_2.append(r[53])
        risk_adj_bank_decline_amt_3.append(r[54])
        risk_adj_bank_decline_ct_1.append(r[49])
        risk_adj_bank_decline_ct_2.append(r[50])
        risk_adj_bank_decline_ct_3.append(r[51])

        risk_adj_ato_pld_amt_1.append(r[40])
        risk_adj_ato_pld_amt_2.append(r[41])
        risk_adj_ato_pld_amt_3.append(r[42])
        risk_adj_ato_pld_ct_1.append(r[37])
        risk_adj_ato_pld_ct_2.append(r[38])
        risk_adj_ato_pld_ct_3.append(r[39])

    chart01_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart01_json_data = [{
                            "data": total_attempts_amt_1,
                        },{
                            "data": total_attempts_amt_2,
                        },{
                            "data": total_attempts_amt_3,
                        }
                        ]

    # print chart01_json_data

    kwargs['chart01_x'] = json.dumps(chart01_json_x)
    kwargs['chart01_data'] = json.dumps(chart01_json_data)

    chart02_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart02_json_data = [{
                            "data": total_attempts_ct_1,
                        },{
                            "data": total_attempts_ct_2,
                        },{
                            "data": total_attempts_ct_3,
                        }
                        ]

    # print chart02_json_data

    kwargs['chart02_x'] = json.dumps(chart02_json_x)
    kwargs['chart02_data'] = json.dumps(chart02_json_data)

    chart03_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart03_json_data = [{
                            "data": risk_adj_attempts_amt_1,
                        },{
                            "data": risk_adj_attempts_amt_2,
                        },{
                            "data": risk_adj_attempts_amt_3,
                        }
                        ]

    # print chart03_json_data

    kwargs['chart03_x'] = json.dumps(chart03_json_x)
    kwargs['chart03_data'] = json.dumps(chart03_json_data)

    chart04_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart04_json_data = [{
                            "data": risk_adj_attempts_ct_1,
                        },{
                            "data": risk_adj_attempts_ct_2,
                        },{
                            "data": risk_adj_attempts_ct_3,
                        }
                        ]

    # print chart04_json_data

    kwargs['chart04_x'] = json.dumps(chart04_json_x)
    kwargs['chart04_data'] = json.dumps(chart04_json_data)

    chart05_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart05_json_data = [{
                            "data": risk_adj_auth_challenge_amt_1,
                        },{
                            "data": risk_adj_auth_challenge_amt_2,
                        },{
                            "data": risk_adj_auth_challenge_amt_3,
                        }
                        ]

    # print chart05_json_data

    kwargs['chart05_x'] = json.dumps(chart05_json_x)
    kwargs['chart05_data'] = json.dumps(chart05_json_data)

    chart06_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart06_json_data = [{
                            "data": risk_adj_auth_challenge_ct_1,
                        },{
                            "data": risk_adj_auth_challenge_ct_2,
                        },{
                            "data": risk_adj_auth_challenge_ct_3,
                        }
                        ]

    # print chart06_json_data

    kwargs['chart06_x'] = json.dumps(chart06_json_x)
    kwargs['chart06_data'] = json.dumps(chart06_json_data)

    chart07_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart07_json_data = [{
                            "data": risk_adj_decline_amt_1,
                        },{
                            "data": risk_adj_decline_amt_2,
                        },{
                            "data": risk_adj_decline_amt_3,
                        }
                        ]

    # print chart07_json_data

    kwargs['chart07_x'] = json.dumps(chart07_json_x)
    kwargs['chart07_data'] = json.dumps(chart07_json_data)

    chart08_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart08_json_data = [{
                            "data": risk_adj_decline_ct_1,
                        },{
                            "data": risk_adj_decline_ct_2,
                        },{
                            "data": risk_adj_decline_ct_3,
                        }
                        ]

    # print chart08_json_data

    kwargs['chart08_x'] = json.dumps(chart08_json_x)
    kwargs['chart08_data'] = json.dumps(chart08_json_data)

    chart09_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart09_json_data = [{
                            "data": risk_adj_processor_decline_amt_1,
                        },{
                            "data": risk_adj_processor_decline_amt_2,
                        },{
                            "data": risk_adj_processor_decline_amt_3,
                        }
                        ]

    # print chart09_json_data

    kwargs['chart09_x'] = json.dumps(chart09_json_x)
    kwargs['chart09_data'] = json.dumps(chart09_json_data)

    chart10_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart10_json_data = [{
                            "data": risk_adj_processor_decline_ct_1,
                        },{
                            "data": risk_adj_processor_decline_ct_2,
                        },{
                            "data": risk_adj_processor_decline_ct_3,
                        }
                        ]

    # print chart10_json_data

    kwargs['chart10_x'] = json.dumps(chart10_json_x)
    kwargs['chart10_data'] = json.dumps(chart10_json_data)

    chart11_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart11_json_data = [{
                            "data": risk_adj_policy_decline_amt_1,
                        },{
                            "data": risk_adj_policy_decline_amt_2,
                        },{
                            "data": risk_adj_policy_decline_amt_3,
                        }
                        ]

    # print chart11_json_data

    kwargs['chart11_x'] = json.dumps(chart11_json_x)
    kwargs['chart11_data'] = json.dumps(chart11_json_data)

    chart12_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart12_json_data = [{
                            "data": risk_adj_policy_decline_ct_1,
                        },{
                            "data": risk_adj_policy_decline_ct_2,
                        },{
                            "data": risk_adj_policy_decline_ct_3,
                        }
                        ]

    # print chart12_json_data

    kwargs['chart12_x'] = json.dumps(chart12_json_x)
    kwargs['chart12_data'] = json.dumps(chart12_json_data)

    chart13_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart13_json_data = [{
                            "data": risk_adj_card_decline_amt_1,
                        },{
                            "data": risk_adj_card_decline_amt_2,
                        },{
                            "data": risk_adj_card_decline_amt_3,
                        }
                        ]

    kwargs['chart13_x'] = json.dumps(chart13_json_x)
    kwargs['chart13_data'] = json.dumps(chart13_json_data)

    chart14_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart14_json_data = [{
                            "data": risk_adj_card_decline_ct_1,
                        },{
                            "data": risk_adj_card_decline_ct_2,
                        },{
                            "data": risk_adj_card_decline_ct_3,
                        }
                        ]

    # print chart14_json_data

    kwargs['chart14_x'] = json.dumps(chart14_json_x)
    kwargs['chart14_data'] = json.dumps(chart14_json_data)

    chart15_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart15_json_data = [{
                            "data": risk_adj_bank_decline_amt_1,
                        },{
                            "data": risk_adj_bank_decline_amt_2,
                        },{
                            "data": risk_adj_bank_decline_amt_3,
                        }
                        ]

    # print chart15_json_data

    kwargs['chart15_x'] = json.dumps(chart15_json_x)
    kwargs['chart15_data'] = json.dumps(chart15_json_data)

    chart16_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart16_json_data = [{
                            "data": risk_adj_bank_decline_ct_1,
                        },{
                            "data": risk_adj_bank_decline_ct_2,
                        },{
                            "data": risk_adj_bank_decline_ct_3,
                        }
                        ]

    # print chart16_json_data

    kwargs['chart16_x'] = json.dumps(chart16_json_x)
    kwargs['chart16_data'] = json.dumps(chart16_json_data)

    chart17_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart17_json_data = [{
                            "data": risk_adj_ato_pld_amt_1,
                        },{
                            "data": risk_adj_ato_pld_amt_2,
                        },{
                            "data": risk_adj_ato_pld_amt_3,
                        }
                        ]

    # print chart17_json_data

    kwargs['chart17_x'] = json.dumps(chart17_json_x)
    kwargs['chart17_data'] = json.dumps(chart17_json_data)

    chart18_json_x = {
                        "name": "Day",
                        "data":dt_pdmon
                    }

    chart18_json_data = [{
                            "data": risk_adj_ato_pld_ct_1,
                        },{
                            "data": risk_adj_ato_pld_ct_2,
                        },{
                            "data": risk_adj_ato_pld_ct_3,
                        }
                        ]

    kwargs['chart18_x'] = json.dumps(chart18_json_x)
    kwargs['chart18_data'] = json.dumps(chart18_json_data)
    
    return render_to_response(NEST_ROOT_DIR + '/html/n12_daily_snapshot/daily_snapshot.html',{'kwargs':kwargs},RequestContext(request))
