#!/usr/bin/python

from optparse import OptionParser
import urllib

results = {
    'ConnsAsyncClosing': 0,
    'Uptime': 0,
    'IdleWorkers': 0,
    'ConnsAsyncWriting': 0,
    'Total Accesses': 0,
    'Total kBytes': 0,
    'BytesPerReq': 0,
    'CPULoad': 0,
    'BytesPerSec': 0,
    'ReqPerSec': 0,
    'ConnsTotal': 0,
    'ConnsAsyncKeepAlive': 0,
    'BusyWorkers': 0
}

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

    (opts, args) = parser.parse_args()
    opts.url = "http://%s:%s/server-status?auto" % (opts.host, opts.port)
    print "%s\t\t\t%s" % (opts, args)

    data = fetchURL(opts.url)

    key = data.splitlines()
    for item in key:
        try:
            results[item.split(': ')[0]] = float(item.split(': ')[1]) if '.' in item.split(': ')[1] else int(item.split(': ')[1])
        except:
            pass
    try:
        del results['Scoreboard']
    except KeyError:
        pass
    print '----------------------------------------------------------------------'
    print results
