# CSIRO SQL Energy Usage Analyser
Python wrapper to query MySQL database and retrieve energy time series data from multiple sources.
The script calculates the usage of energy for various groups of sources in a time-series format for further analysis

# Command-Line Usage

Directly calling the `hquery.py` script will query the database specified in `res/cred.[csv/json]` (see Database Credentials).

```bash
~$ python hquery.py
```

An alternative location for the database and table list can be specified in the `get_time_series` 5th and 6th positional arguments

```python
    get_time_series(start_date, end_date, min_res, table_file='res/table_list.txt', cred_file='res/cred.json')
```

Settings must currently be directly modified in the `main()` method of `hquery.py`

```python
    #Settings (temporary)
    min_res = 15
    start_date = '2016-01-01'
    end_date = '2016-12-31'
    base_output = 'test_output'
```

# Database Credentials

Database credentials must specify the host, user, password, database name, and port.

This information may be specified in `json` or `csv` format. Alternatively, manually entering this data is supported. `csv` files must be header-less, with the first column being the field and the second the value.

Strictly, the fields must be either `host`, `user`, `passwd`, `db`, or `port`

`json` Files must be in the format:

```json
    {
        "host": "1xx.xxx.xxx.xxx",
        "user": "uuuuuuu",
        "passwd": "pppppp",
        "db": "dddd",
        "port": "3306"
    }
```

# Table List
The table list is the list of tables that the sript will query from the specified database.

Currently, the table list must be a plain text file, with `csv` rows of length 2. The first column is the table name, and
the second column is the source type
