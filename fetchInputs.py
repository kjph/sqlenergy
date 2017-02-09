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


def type_table_map(loc):

    ret = collections.defaultdict(list)

    with open(loc, 'r') as fd:
        reader = csv.reader(fd)

        for row in reader:
            ret[row[1].strip()].append(row[0].strip())

    logging.debug("fetchInputs:type_table_map:%s" % ret)
    return ret

def get_datetime_from_str(in_str, time_format='%Y-%m-%d %H:%M:%S'):
    return datetime.strptime(in_str, time_format)
