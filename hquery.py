import MySQLdb
import logging
from datetime import datetime, timedelta
from TimeSeries import TimeSeries
import fetchInputs

try:
    import MySQLdb.converters
except ImportError:
    _connarg('conv')

def connect_mysql_converted(**dbi):
    """
    Specify converters for MYSQL connections

    Arguments:
        dbi:    key-value dictionary specifying all credentials
                All values must be of string type
    """

    try:
        orig_conv = MySQLdb.converters.conversions
        conv_iter = iter(orig_conv)
        convert = dict(zip(conv_iter, [str,] * len(orig_conv.keys())))
        print "Connecting host=%s user=%s db=%s port=%d" % (dbi['host'],
                                                            dbi['user'],
                                                            dbi['db'],
                                                            int(dbi['port']))
        conn = MySQLdb.connect(dbi['host'],
                               dbi['user'],
                               dbi['passwd'],
                               dbi['db'],
                               int(dbi['port']),
                               conv=convert)
    except MySQLdb.Error, e:
        print "Error connecting %d: %s" % (e.args[0], e.args[1])
        return (e.args[0], e.args[1])

    return conn

def ping_database(**dbi):
    """
    Ping database for successful connection
    """

    db = connect_mysql_converted(**dbi)
    if isinstance(db, tuple):
        return -1

def get_query_between_dates(table_name, start_date, end_date):
    """
    Function to generate SQL query string
    """

    query = "select FROM_UNIXTIME(TIMESTAMP/1000) as timestamp, VALUE as kwh"
    query += " from %s" % table_name
    query += " where ((TIMESTAMP/1000) > UNIX_TIMESTAMP('%s'))" % start_date
    query += " AND ((TIMESTAMP/1000) < UNIX_TIMESTAMP('%s'))" % end_date

    return query

def main():

    #Connect to database and get cursor
    dbi = fetchInputs.database_inputs('res/cred.json')
    db = connect_mysql_converted(**dbi)
    cursor = db.cursor()

    #Specify which tables we want to run query over
    type_table_map = fetchInputs.type_table_map('res/table_list.txt')

    #Settings
    min_res = 15
    allSeries = []
    start_date = '2016-01-01'
    end_date = '2016-12-31'
    base_output = 'test_output'

    all_types = list(set([k for k in type_table_map]))

    Series = TimeSeries(all_types, min_res)

    #Run over all
    for series_type, list_of_tables in type_table_map.iteritems():
        print series_type

        #Run the queries over all tables
        for table in list_of_tables:

            query = get_query_between_dates(table, start_date, end_date)
            cursor.execute(query)

            Series.stream_handler(series_type, cursor.fetchall())

    series_output = '%s.csv' % (base_output)
    with open(series_output, 'w') as fd:
        fd.write(str(Series))

if __name__ == '__main__':
    main()
