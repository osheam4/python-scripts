#!/usr/bin/python

import os
from optparse import OptionParser
import urllib

zabbix_log = '/dev/null';

results = {}

def fetchURL(url, user = None, passwd = None):
    """ Return the data from a URL """
    if user and passwd:
        parts = url.split('://')
        url = parts[0] + "://" + user + ":" + passwd + "@" + parts[1]
    conn = urllib.urlopen(url)
    try:
        data = conn.read()
    finally:
        conn.close()
    return data

def send_to_zabbix(results):
    for key, value in results.iteritems():
        os.system("%s -c %s -k %s -i %s" % (opts.zabbix_sender, opts.zabbix_conf, key, value))

if __name__ == "__main__":
    parser = OptionParser(
        usage = "%prog [-o <Apache hostname or IP>]",
        version = "%prog $Revision: 1 $",
        prog = "ApacheMonitor",
        description = """This program gathers data from Apache's built-in status page.
        """,
        )
    parser.add_option(
        "-o",
        "--host",
        action = "store",
        type = "string",
        dest = "host",
        default = "localhost",
        help = "Host to connect to. [default: %default]",
        )
    parser.add_option(
        "-p",
        "--port",
        action = "store",
        type = "int",
        dest = "port",
        default = 80,
        help = "Port to connect on. [default: %default]",
        )
    parser.add_option(
        "-l",
        "--log",
        action = "store_false",
        dest = "log",
        default = "False",
        help = "Only log output, dont send to zabbix server"
        )
    parser.add_option(
        "-z",
        "--zabbix_sender",
        action = "store",
        type = "string",
        dest = "zabbix_sender",
        default = "/usr/bin/zabbix_sender",
        help = "Zabbix Sender binary. [default: %default]",
        )
    parser.add_option(
        "-c",
        "--zabbix_conf",
        action = "store",
        type = "string",
        dest = "zabbix_conf",
        default = "/etc/zabbix/zabbix_agentd.conf",
        help = "Zabbix Configuration file. [default: %default]",
        )



    (opts, args) = parser.parse_args()
    opts.url = "http://%s:%s/server-status?auto" % (opts.host, opts.port)
    data = fetchURL(opts.url)
    key = data.splitlines()
    for item in key:
        try:
            resultitem = item.split(': ')[1]
            results[item.split(': ')[0].replace(" ", "_").lower()] = float(resultitem) if '.' in resultitem else int(resultitem)
        except:
            if item.split(': ')[0] == "Scoreboard":
                results['workers.open_slot'] = item.split(': ')[1].count('.')
                results['workers.waiting'] = item.split(': ')[1].count('_')
                results['workers.starting'] = item.split(': ')[1].count('S')
                results['workers.reading'] = item.split(': ')[1].count('R')
                results['workers.sending'] = item.split(': ')[1].count('W')
                results['workers.keepalive'] = item.split(': ')[1].count('K')
                results['workers.dns_lookup'] = item.split(': ')[1].count('D')
                results['workers.closing'] = item.split(': ')[1].count('C')
                results['workers.logging'] = item.split(': ')[1].count('L')
                results['workers.gracefully_finishing'] = item.split(': ')[1].count('G')
                results['workers.idle_cleanup'] = item.split(': ')[1].count('I')
    try:
        del results['Scoreboard']
    except KeyError:
        pass
    for key, value in results.iteritems():
        key = key.replace(" ", "_").lower()
    if opts.log == 'False':
        send_to_zabbix(results)
    else:
        print results
