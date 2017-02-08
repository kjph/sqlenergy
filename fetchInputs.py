import json

def database_inputs_user():
    """
    Get database information from user
    """

    info_to_req = ['host', 'user', 'passwd', 'db', 'port']
    dbinfo = {x: raw_input("%s>>\t\t" % x.upper()).strip() for x in info_to_req}

    return dbinfo

def database_inputs_json(json_file):
    """
    Loads database information from resources
    """

    with open(json_file, 'r') as fd:
        dbinfo = json.load(fd)

    return dbinfo

def table_names(file):
    """
    Load all tables from a file
    """

    all_tables = []
    with open(file, 'r') as fd:
        for line in fd.readlines():
            all_tables.append(line.strip())

    return all_tables
