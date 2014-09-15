#!/usr/bin/python

from optparse import OptionParser
import pymysql

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
    conn = pymysql.connect(host=opts.host, passwd=opts.passwd, user=opts.user, port=opts.port)
    cur = conn.cursor()
    cur.execute("SHOW GLOBAL STATUS")
    data = cur.fetchall()
    print data
    conn.close
