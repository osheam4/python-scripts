#!/usr/bin/python

from optparse import OptionParser
import pymysql

key_index = [
    'Key_read_requests',
    'Key_reads',
    'Key_write_requests',
    'Key_writes',
    'history_list',
    'innodb_transactions',
    'read_views',
    'current_transactions',
    'locked_transactions',
    'active_transactions',
    'pool_size',
    'free_pages',
    'database_pages',
    'modified_pages',
    'pages_read',
    'pages_created',
    'pages_written',
    'file_fsyncs',
    'file_reads',
    'file_writes',
    'log_writes',
    'pending_aio_log_ios',
    'pending_aio_sync_ios',
    'pending_buf_pool_flushes',
    'pending_chkp_writes',
    'pending_ibuf_aio_reads',
    'pending_log_flushes',
    'pending_log_writes',
    'pending_normal_aio_reads',
    'pending_normal_aio_writes',
    'ibuf_inserts',
    'ibuf_merged',
    'ibuf_merges',
    'spin_waits',
    'spin_rounds',
    'os_waits',
    'rows_inserted',
    'rows_updated',
    'rows_deleted',
    'rows_read',
    'Table_locks_waited',
    'Table_locks_immediate',
    'Slow_queries',
    'Open_files',
    'Open_tables',
    'Opened_tables',
    'innodb_open_files',
    'open_files_limit',
    'table_cache',
    'Aborted_clients',
    'Aborted_connects',
    'Max_used_connections',
    'Slow_launch_threads',
    'Threads_cached',
    'Threads_connected',
    'Threads_created',
    'Threads_running',
    'max_connections',
    'thread_cache_size',
    'Connections',
    'slave_running',
    'slave_stopped',
    'Slave_retried_transactions',
    'slave_lag',
    'Slave_open_temp_tables',
    'Qcache_free_blocks',
    'Qcache_free_memory',
    'Qcache_hits',
    'Qcache_inserts',
    'Qcache_lowmem_prunes',
    'Qcache_not_cached',
    'Qcache_lowmem_prunes',
    'Qcache_not_cached',
    'Qcache_queries_in_cache',
    'Qcache_total_blocks',
    'query_cache_size',
    'Questions',
    'Com_update',
    'Com_insert',
    'Com_select',
    'Com_delete',
    'Com_replace',
    'Com_load',
    'Com_update_multi',
    'Com_insert_select',
    'Com_delete_multi',
    'Com_replace_select',
    'Select_full_join',
    'Select_full_range_join',
    'Select_range',
    'Select_range_check',
    'Select_scan',
    'Sort_merge_passes',
    'Sort_range',
    'Sort_rows',
    'Sort_scan',
    'Created_tmp_tables',
    'Created_tmp_disk_tables',
    'Created_tmp_files',
    'Bytes_sent',
    'Bytes_received',
    'innodb_log_buffer_size',
    'unflushed_log',
    'log_bytes_flushed',
    'log_bytes_written',
    'relay_log_space',
    'binlog_cache_size',
    'Binlog_cache_disk_use',
    'Binlog_cache_use',
    'binary_log_space',
    'innodb_locked_tables',
    'innodb_lock_structs',
    'State_closing_tables',
    'State_copying_to_tmp_table',
    'State_end',
    'State_freeing_items',
    'State_init',
    'State_locked',
    'State_login',
    'State_preparing',
    'State_reading_from_net',
    'State_sending_data',
    'State_sorting_result',
    'State_statistics',
    'State_updating',
    ]


def getstats(opts):
    results = {}
    conn = pymysql.connect(host=opts.host, passwd=opts.passwd, user=opts.user, port=opts.port)
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SHOW GLOBAL STATUS")
    data = cur.fetchall()
    for item in data:
        if item['Variable_name'] in key_index:
            results[item['Variable_name']] = item['Value']
    cur.execute("SHOW VARIABLES")
    # TODO: get results of the following queries
    #cur.execute("SHOW PROCESSLIST")
    #cur.execute("SHOW MASTER LOGS")
    #cur.execute("SHOW SLAVE STATUS")
    cur.execute("SHOW /*!50000 ENGINE*/ INNODB STATUS")
    data = cur.fetchall()
    print data
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
    print results
    print len(results)
    for key, value in results.items():
        if 'Threads_cached' in key:
            print '%s\t\t%s' % (key, value)
