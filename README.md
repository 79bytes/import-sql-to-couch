# Import SQL To Couch

A simple, comfortable way to transfer a SQL-database, or parts of it, to your CouchDB. Transfer whole databases or just some different tables. Currently supported SQL-databases, take a look at sql-type: mysql


## Installation/Test environment

* Ubuntu 11.10
* python -> python2.7 from repositories -> Python 2.7.2+
* MySQL -> mysql-server from repositories -> mysql-server-core-5.1
* CouchDB -> couchdb-bin from repositories -> couchdb - Apache CouchDB 1.0.1
	* CouchDB -> hosted on Iris Couch -> Apache CouchDB


## Python requirements

Following python-libs are required, used and imported:

* getpass (python installation)
* argparse (python installation)
* abc (python installation)
* re (python installation)
* couchdb (python-couchdb)
* MySQLdb (python-mysqldb)


## Usage

Use ...

```
$ python import_sql_2_couch.py --help
```

... for parameters definition and -spezifications.


### Mostly used parameters explained

sql-/couch-connection:
```
[(http|https)://][username:password@]sql-host[:port]
```

A "connection string" is a combination of authentication-, host to connect- and, if needed, port-information,
actually a normally used URL, like ...

```
http://john_smith:secret@myhost.com:1234
```

So, if you don't want to give your authentication-data on the line, you can set "username" and/or password to
the ? (question mark)-character. You will be asked about the data.


### sql-sources

```
db.[table]
```

One or more definable SQL-sources, given as a "database dot table" combination.

e.g.
mydb
Imports the whole database "mydb"

mydb, myotherdb.mytable
Imports the whole database "mydb" and the table "mytable" from database "myotherdb".


### sql-type

Defines which type of sql-database-connection is used.

mysql
A MySQL-database is used, connected via python-mysqldb-lib.


### sql-connect-sql

Adds one or more sqls which are executed directly after connecting to the sql-host, useful to set charset-settings.

e.g.
```
$ python import_sql_2_couch.py ... -scsql "SET names 'utf8'" ...
```
... Executes "SET names 'utf8'" after connection to the sql-connection.


### couch-creation-type

Defines how the import creates databases within the couch, given via 'sql-sources'.

db_tbl -> database_table, default
db -> database
tbl -> table

e.g.
SQL-Sources -ss mydb -cct db_tbl will be imported to CouchDB-database "mydb_[tablename]".

SQL-Sources -ss myotherdb.mytable -cct tbl will be imported to CouchDB-database "mytable".


## Example

```
$ python import_sql_2_couch.py -s sqlserver -c localhost -ss mydb -st mysql
```

Will import all tables from "mydb" from sql-server "sqlserver" using the default port 3306 to couch-server
"localhost" using the default port 5984 and the default couch-creation-type "db_tbl" for creating the couch
database.

... now, a more complex one ...

```
$ python import_sql_2_couch.py -s http://john:my_blue_elephant@sqldataserver:1234 -c https://admin:my_secret_password@my_online_domain.net -ss mydb -st mysql -ss myotherdb.mytable -scsql "SET name 'utf8'" -cct tbl -v
```

Will import all tables from "mydb" and the table "mytable" from "myotherdb" from "sqldataserver" using special
port 1234 authenticated with username "john" and password "my_blue_elephant" securely (https, if implemented
into he couch-server) to couch-server "my_online_domain.net" using the default port 5984 authenticated with
username "admin" and password "my_secret_password" using the couch-creation-type "tbl". If the connection is
established to "sqldataserver" the given -scsql-queries are executed, actually in this case "SET names 'utf8'".
The parameter -v shows you all the stuff going on, set verbosity.

... no need for more examples, i think you got the clue.

