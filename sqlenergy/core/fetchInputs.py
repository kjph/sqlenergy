import logging
import json
import csv
import collections
from datetime import datetime

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
        logging.warning('fetchInputs:database_inputs:failed to detect file type')
        return -1

    logging.debug('fetchInputs:database_inputs:%s' % dbi)
    return {str(k): str(v) for k,v in dbi.iteritems()}


def table_stat(loc):
    """Get table information in dictionary.

    Parameters
    ---------------
    loc:    str, path to CSV file

    Return
    ---------------
    Dictionary key=tab, val={'stype':
                             'thr_min':
                             'thr_max':
                             'time_format':}

    """

    r = collections.defaultdict(dict)

    if not(loc.endswith('.csv') or loc.endswith('.txt')):
        logging.error("fetchInputs:table_stat:Incorrect file format for file %s" % loc)
        return -1

    with open(loc, 'r') as fd:
        reader = csv.reader(fd)

        for row in reader:

            #Incorrect format
            if len(row) < 2:
                logging.warning("Incorrect format raised for table_stat in %s in %s" % (loc, row))
                continue

            #Get table ID and type
            table = row[0].strip()
            r[table]['stype'] = row[1].strip()

            #Robust CSV
            if len(row) == 5:
                r[table]['thr_min'] = float(row[2])
                r[table]['thr_max'] = float(row[3])
                r[table]['time_format'] = row[4].strip()
            elif len(row) == 4:
                r[table]['thr_min'] = float(row[2])
                r[table]['thr_max'] = float(row[3])
                r[table]['time_format'] = '%Y-%m-%d %H:%M:%S.%f'
            else:#Default values
                r[table]['thr_min'] = 0.0
                r[table]['thr_max'] = 100.0
                r[table]['time_format'] = '%Y-%m-%d %H:%M:%S.%f'

    return r

def get_datetime_from_str(in_str, time_format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(in_str, time_format)
