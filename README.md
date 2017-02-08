# csiroEnergy8
MySQL Handler for Energy Usage

# Credentials (Temporary)

a `json` file must be saved in `res/cred.json` in the format:

```json
    {
        "host": "1xx.xxx.xxx.xxx",
        "user": "uuuuuuu",
        "passwd": "pppppp",
        "db": "dddd",
        "port": "3306"
    }
```

Alternatively, credentials can be manually inputted by changing the line in `hquery.py` at the `main()` method:

```python
    #Connect to database and get cursor
    dbi = fetchInputs.database_inputs_user()
```
