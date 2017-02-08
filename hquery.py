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
    return conn

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
    dbi = fetchInputs.database_inputs_json('res/cred.json')
    dbi = {k: str(v) for k,v in dbi.iteritems()}
    db = connect_mysql_converted(**dbi)
    cursor = db.cursor()

    #Specify which tables we want to run query over
    list_of_tables = fetchInputs.table_names('res/table_list.txt')

    allRenewables = RenewableTimeSeries(15)

    #Run the queries over all tables
    for table in list_of_tables:
        start_date = '2016-01-01'
        end_date = '2016-12-31'
        query = get_query_between_dates(table, start_date, end_date)
        cursor.execute(query)
        #print query

        allRenewables.stream_handler(cursor.fetchall())

    with open('test_output.csv', 'w') as fd:
        fd.write(str(allRenewables))

if __name__ == '__main__':
    main()
