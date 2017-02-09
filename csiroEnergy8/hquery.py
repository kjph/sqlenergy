import MySQLdb
import logging
import logging.config
from datetime import datetime, timedelta
from TimeSeries import TimeSeries
import fetchInputs

try:
    import MySQLdb.converters
except ImportError:
    _connarg('conv')

def connect_mysql_converted(**dbi):
    """Specify converters for MYSQL connections.

    Parameters
    ---------------
    dbi:    dict-type, key=field, value=value
            container for database specification

    Return
    ---------------
    success     returns a MySQLdb connection.
                Must be closed outside of function
    fail        returns tuple
                (error_code, error_msg)
    """

    try:
        orig_conv = MySQLdb.converters.conversions
        conv_iter = iter(orig_conv)
        convert = dict(zip(conv_iter, [str,] * len(orig_conv.keys())))
        logging.info("hquery:Connecting host=%s user=%s db=%s port=%d" % (dbi['host'],
                                                            dbi['user'],
                                                            dbi['db'],
                                                            int(dbi['port'])))
        conn = MySQLdb.connect(dbi['host'],
                               dbi['user'],
                               dbi['passwd'],
                               dbi['db'],
                               int(dbi['port']),
                               conv=convert)
    except MySQLdb.Error, e:
        logging.error("hquery:ERR:connecting %d: %s" % (e.args[0], e.args[1]))
        return (e.args[0], e.args[1])

    return conn

def ping_database(**dbi):
    """Ping database for successful connection.

    Parameters
    ---------------
    dbi:    dict-type, key=field, value=value
            container for database specification

    Return
    ---------------
    bool_success
    """

    logging.info("Ping test")
    db = connect_mysql_converted(**dbi)
    if isinstance(db, tuple):
        logging.info("Ping test FAILED")
        return 0

    db.close()
    logging.info("Ping test SUCCESS")
    return 1

def get_all_tables(ending='realenergy', **dbi):

    db = connect_mysql_converted(**dbi)
    if isinstance(db, tuple):
        logging.info("hquery:get_all_tables:FAILED")
        return 0

    cur = db.cursor()
    cur.execute("show tables;")

    all_tables = [x[0].strip() for x in cur.fetchall() if x[0].strip().endswith(ending)]

    db.close()
    logging.debug("hquery:get_all_tables %s" % all_tables)
    logging.info("hquery:get_all_tables:SUCCESS")
    return all_tables

def get_query_between_dates(table_name, start_date, end_date):
    """Generate SQL query string.

    Parameters
    ---------------
    table_name:     str, name of table to query from database
    start_date:     str, 'YYYY-MM-DD', date to being query
    end_date:       str, 'YYYY-MM-DD', date to end query

    Return
    ---------------
    str
    """

    query = "select FROM_UNIXTIME(TIMESTAMP/1000) as timestamp, VALUE as kwh"
    query += " from %s" % table_name.strip()
    query += " where ((TIMESTAMP/1000) > UNIX_TIMESTAMP('%s'))" % start_date
    query += " AND ((TIMESTAMP/1000) < UNIX_TIMESTAMP('%s'))" % end_date

    logging.debug("hquery:get_query_between_dates(%s, %s, %s): %s" % (table_name, start_date, end_date, query))

    return query

def get_time_series(start_date, end_date, min_res, table_file='res/table_list.txt', cred_file='res/cred.json'):

    #Connect to database and get cursor
    dbi = fetchInputs.database_inputs(cred_file)
    db = connect_mysql_converted(**dbi)
    cursor = db.cursor()

    #Specify which tables we want to run query over
    tab_stat = fetchInputs.table_stat(table_file)

    #Get unique keys
    all_types = list(set([tab_stat[k]['stype'] for k in tab_stat]))

    #Init TimeSeries object for all source types
    Series = TimeSeries(all_types, min_res)

    #Run over all series types
    for tab, stat in tab_stat.iteritems():

        query = get_query_between_dates(tab, start_date, end_date)
        cursor.execute(query)

        Series.stream_handler(stat['stype'], cursor.fetchall(),
                              stat['thr_min'], stat['thr_max'],
                              stat['time_format'])

    return Series

    db.close()


def main():

    logging.basicConfig(filename='hquery.log',level=logging.DEBUG)

    #Settings (temporary)
    min_res = 15
    start_date = '2016-01-01'
    end_date = '2017-01-01'
    output_file = 'rawdata.csv'

    Series = get_time_series(start_date, end_date, min_res)

    #Write output
    with open(output_file, 'w') as fd:
        fd.write(str(Series))

if __name__ == '__main__':
    main()
