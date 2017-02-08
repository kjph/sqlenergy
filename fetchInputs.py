import json
import csv

def database_inputs(loc):
    """
    Loads database information from resources
    """

    if loc == None:
        info_to_req = ['host', 'user', 'passwd', 'db', 'port']
        dbi = {x: raw_input("%s>>\t\t" % x.upper()).strip() for x in info_to_req}

    elif loc.endswith('.json'):
        with open(loc, 'r') as fd:
            dbi = json.load(fd)

    elif loc.endswith('.csv'):
        with open(loc, 'r') as fd:
            reader = csv.reader(fd)
            dbi = {row[0].strip(): row[1].strip() for row in reader}
    else:
        reutrn -1

    return {str(k): str(v) for k,v in dbi.iteritems()}

def table_names(file):
    """
    Load all tables from a file
    """

    all_tables = []
    with open(file, 'r') as fd:
        for line in fd.readlines():
            all_tables.append(line.strip())

    return all_tables
