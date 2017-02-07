import MySQLdb

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

    query = "select VALUE as KWH, FROM_UNIXTIME(TIMESTAMP/1000) AS timestamp_good FROM %s" % table_name
    query += " where ((TIMESTAMP/1000) > UNIX_TIMESTAMP('%s'))" % start_date
    query += " AND ((TIMESTAMP/1000) < UNIX_TIMESTAMP('%s'))" % end_date

    return query

def main():

    #Ask user for user/password
    user = raw_input("Username>>\t")
    passwd = raw_input("Password>>\t")

    #Make a connection
    db = MySQLdb.connect(host="150.229.111.139",
                         user=user,
                         passwd=passwd,
                         db='ems')

    #Get a cursor object
    cursor = db.cursor()

    #Specify which tables we want to run query over
    list_of_tables = load_table_list('res/table_list.txt')

    #Data structure to hold our results
    all_vals = []#Empty list that we will fill up

    #Run the queries over all tables
    for table in list_of_tables:
        start_date = '2016-01-16'
        end_date = '2016-12-16'
        query = get_query_between_dates(table, start_date, end_date)
        cursor.execute(query)

        for value in cursor:
            #Append means to ADD to a list (at the end)
            all_vals.append((table, value))

        #Go through all values in our LIST (all_vals)
    for result in all_vals:
        print result
#             table = result[0]#Extract the table name from the TUPLE
#             value = result[1:]#Extract the value from the TUPLE
#             string_to_write = "%s, %s\n" % (table, value)
#             fd.write(string_to_write)

if __name__ == '__main__':
    main()
