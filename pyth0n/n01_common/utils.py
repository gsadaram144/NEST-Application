import datetime,re,random,MySQLdb,os
from time import strftime

NEST_ROOT_DIR = os.path.abspath(__file__).partition('\\nest\\')[2].partition('\\')[0]

NEST_DATA_ROOT_FULL_PATH = os.path.abspath(__file__).partition('\\nest\\')[0] + '\\nest_data\\' + NEST_ROOT_DIR

import_nest_globals = __import__('%s.pyth0n.n01_common' % NEST_ROOT_DIR, globals(), locals(), ['globals'], 0).globals

def chunks(l, n):
    for i in xrange(0, len(l), n):
        yield l[i:i+n]

def allsundays(start_year, last_date=datetime.datetime.now().date()):
    d = datetime.date(start_year,1,7)
    #d += datetime.timedelta(days = last_date.weekday() - d.weekday())
    d += datetime.timedelta(days = 5 - d.weekday())
    while d.year >= start_year:
        if d > last_date:
            break
        yield d
        d += datetime.timedelta(days = 7)

def convert_date_format(d,strng=0,delim='-'):
    l = d.split(delim)
    if strng == 1:
        return ('-'.join([l[2],l[0],l[1]]))
    return datetime.datetime.strptime(('-'.join([l[2],l[0],l[1]])),'%Y-%m-%d')

def populate_header(request,kwargs):
    if 'HTTP_REFERER' in request.META:
        kwargs['back'] = request.META['HTTP_REFERER']
    else:
        kwargs['back'] = "/"
    return

def store_session_details(request,url='',error=False):
    ############### Temporarily writing into file#####################
    if request.META['REMOTE_ADDR'] not in import_nest_globals.IP_ADDRESSES_TO_IGNORE:
        if 'REMOTE_USER' in request.META:
            user = request.META['REMOTE_USER']
        elif 'USERNAME' in request.META:
            user = request.META['USERNAME']
        if 'Safari' in request.META['HTTP_USER_AGENT'] and 'Macintosh' in request.META['HTTP_USER_AGENT']:
            browser_name = 'Safari'
        elif 'Firefox' in request.META['HTTP_USER_AGENT']:
            browser_name = 'Firefox'
        elif 'MSIE' in request.META['HTTP_USER_AGENT']:
            browser_name = 'Internet Explorer'
        elif ('Chrome' in request.META['HTTP_USER_AGENT'] or 'OPR' in request.META['HTTP_USER_AGENT']):
            browser_name = 'Chrome/Opera'
        else:
            browser_name = 'Safari'
        if 'Windows' in request.META['HTTP_USER_AGENT']:
            operating_sys = 'Windows'
        elif 'Macintosh' in request.META['HTTP_USER_AGENT']:
            operating_sys = 'Mac'
        else:
            operating_sys = 'Linux'
        session_data = user+'~'
        if request.session._session_key:
            session_data += request.session._session_key+'~'
        else:
            session_data += '~'
        session_data += strftime("%Y-%m-%d %H:%M:%S")+'~'
        session_data += request.path+'~'
        session_data += browser_name+'~'
        session_data += operating_sys+'~'
        session_data += request.META['REMOTE_ADDR']+'~'
        if 'REMOTE_PORT' in request.META:
            session_data += request.META['REMOTE_PORT']+'~'
        else:
            session_data += '~'
        if 'HTTP_REFERER' in request.META:
            session_data += request.META['HTTP_REFERER']+'~'
        else:
            session_data += '~'
        session_data += url+'~'
        # if request.path == '/':
            # link_description = import_nest_globals.LINK_DESC['/']
            # session_data += link_description+'~'
        # elif not error:
            # link_description = [import_nest_globals.LINK_DESC[x] for x in import_nest_globals.LINK_DESC.keys() if x in request.path and x != '/']
            # session_data += link_description[0]+'~'
        # else:
            # link_description = 'Page not found'
            # session_data += link_description+'~'
        if error:
            with open(NEST_DATA_ROOT_FULL_PATH + '\\logs\\n01_common\\UserErrorLog.txt', 'a') as logfile:
                logfile.write(session_data+'\n')
        else:
            with open(NEST_DATA_ROOT_FULL_PATH + '\\logs\\n01_common\\UserSessionLog.txt', 'a') as logfile:
                logfile.write(session_data+'\n')
    return
