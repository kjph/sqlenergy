import MySQLdb
import datetime

try:
    import MySQLdb.converters
except ImportError:
    _connarg('conv')

def connect_with_convert(user, passwd, host='150.229.111.139', db='ems', port=3306):
    """
    Specify converters for MYSQL connections
    """

    try:
        orig_conv = MySQLdb.converters.conversions
        conv_iter = iter(orig_conv)
        convert = dict(zip(conv_iter, [str,] * len(orig_conv.keys())))
        print "Connecting host=%s user=%s db=%s port=%d" % (host, user, db, port)
        conn = MySQLdb.connect(host, user, passwd, db, port, conv=convert)
    except MySQLdb.Error, e:
        print "Error connecting %d: %s" % (e.args[0], e.args[1])
    return conn

def load_table_list(file):
    """
    Load all tables from a file
    """

    all_tables = []
    with open(file, 'r') as fd:
        for line in fd.readlines():
            all_tables.append(line.strip())

        return all_tables

def get_query_between_dates(table_name, start_date, end_date):
    """
    Function to generate SQL query string
    """

    query = "select VALUE as KWH, FROM_UNIXTIME(TIMESTAMP/1000) AS timestamp_good from %s" % table_name
    query += " where ((TIMESTAMP/1000) > UNIX_TIMESTAMP('%s'))" % start_date
    query += " AND ((TIMESTAMP/1000) < UNIX_TIMESTAMP('%s'))" % end_date

    return query

def main():

    #Ask user for user/password
    user = raw_input("Username>>\t")
    passwd = raw_input("Password>>\t")

    #Make a connection
    db = connect_with_convert(user, passwd)

    #Get a cursor object
    cursor = db.cursor()

    #Specify which tables we want to run query over
    list_of_tables = load_table_list('res/test.txt')

    #Data structure to hold our results
    all_vals = []#Empty list that we will fill up

    #Run the queries over all tables
    for table in list_of_tables:
        start_date = '2016-01-16'
        end_date = '2016-12-16'
        query = get_query_between_dates(table, start_date, end_date)
        cursor.execute(query)
        #print query

        for row in cursor.fetchall():
            #Append means to ADD to a list (at the end)
           print row

    #     #Go through all values in our LIST (all_vals)
    # for result in all_vals:
    #     print result

if __name__ == '__main__':
    main()
