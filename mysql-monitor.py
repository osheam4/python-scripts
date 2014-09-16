#!/usr/bin/python

from optparse import OptionParser
import pymysql



def getstats(opts):
    results = {}
    conn = pymysql.connect(host=opts.host, passwd=opts.passwd, user=opts.user, port=opts.port)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SHOW GLOBAL STATUS")
    data = cur.fetchall()
    for item in data:
        results[item['Variable_name']] = item['Value']
    cur.execute("SHOW VARIABLES")
    for item in data:
        results[item['Variable_name']] = item['Value']
    # TODO: get results of the following queries
    #cur.execute("SHOW PROCESSLIST")
    #cur.execute("SHOW MASTER LOGS")
    #cur.execute("SHOW SLAVE STATUS")
    #cur.execute("SHOW /*!50000 ENGINE*/ INNODB STATUS")
    conn.close()
    return results


if __name__ == "__main__":
    parser = OptionParser(
        usage = "%prog [-o <Apache hostname or IP>]",
        version = "%prog $Revision: 1 $",
        prog = "MySqlMonitor",
        description = """This program gathers data from MySql.
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
        "-s",
        "--port",
        action = "store",
        type = "int",
        dest = "port",
        default = 3306,
        help = "Port to connect on. [default: %default]",
        )
    parser.add_option(
        "-u",
        "--user",
        action = "store",
        type = "string",
        dest = "user",
        default = "root",
        help = "User to connect as. [default: %default]",
        )
    parser.add_option(
        "-p",
        "--pass",
        action = "store",
        type = "string",
        dest = "passwd",
        default = "",
        help = "Password to connect. [default: %default]",
        )


    (opts, args) = parser.parse_args()
    print "%s\t\t\t" % (opts)
    results = getstats(opts)
    print results.keys()[0]
    print len(results)
    for key, value in results.items():
        if 'Threads_cached' in key:
            print '%s\t\t%s' % (key, value)
