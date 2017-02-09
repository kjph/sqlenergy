# csiroEnergy8
MySQL Handler for Energy Usage

# Command-Line Useage

Directly calling the `hquery.py` script will query the database specified in `res/cred.[csv/json]`

```bash
~$ python hquery.py
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
