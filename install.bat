git pull
python -m pip install -r requirements.txt
python -c "import MySQLdb"
if %ERRORLEVEL% GEQ 1 .\win\MySQL-python-1.2.5.win32-py2.7.exe
