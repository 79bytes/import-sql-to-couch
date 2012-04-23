import MySQLdb
from ConnectionBase import *

class MySQLConnection(ConnectionBase):
	"""Class which implements methods to connect to a sql-database, like MySQL, aso, 
	retrieve data, aso."""

	def __init__(self, connectionString=None, username="", password="", host="localhost", port=3306, databaseType="mysql"):
		"""Initializes the object with given parameters, like username, password, aso. Will not open
		the connection to the sql database. Use method 'Connect' instead.
		
		Parameter:
		See also 'ConnectionBase.__init__'
		"""

		# Call super-init
		super(self.__class__, self).__init__(connectionString=connectionString, username=username, password=password, host=host, port=port)
	# End def

	def Connect(self):
		"""Connects to the currently defined sql-host via currently defined authorization."""

		self.__dbConnection=MySQLdb.connect(user=self.GetUsername(), passwd=self.GetPassword(), host=self.GetHost(), port=self.GetPort())
	# End def

	def Disconnect(self):
		"""Disconnect/closes the connectionn which was opened via 'Connect' method."""

		# Close SQL
		self.__dbConnection.close()
	# End def

	def ExecuteSQL(self, sql):
		"""Executes a given sql-query.

		Parameter:
		string sql SQL to be executed.
		"""

		# Check
		if not sql or not isinstance(sql, str): raise TypeError

		cursor=self.__dbConnection.cursor()
		cursor.execute(sql)
		cursor.close()
	# End def

	def GetDatabases(self, databases=[""]):
		"""Returns the given databases after checked if valid.

		Parameter:
		list databases Databases which should be checked if they available.

		Return:
		list List of databases, if parameter 'databases' is empy, actually "", then
		all databases are returned.
		"""

		# Check
		if databases and not isinstance(databases, list): raise TypeError

		# Create return array
		rtn=[]

		# Create cursor
		cursor=self.__dbConnection.cursor()

		# Retrieve all databases
		for db in databases:
			query="SHOW DATABASES%s" % (" LIKE '%s'" % db)
			cursor.execute(query)

			# Gather rows of databases
			if cursor.rowcount==0:
				if len(databases) and databases[0]!="":
					raise NoDatabaseFound(db)
				else:
					raise NoDatabasesFound
				# End if
			else:
				[ rtn.append(row[0]) for row in cursor.fetchall() ]
			# End if
		# End for

		# Close cursor
		cursor.close()

		# Return databases-array
		return rtn
	# End def

	def GetTablesFromDatabase(self, database, table=None):
		"""Returns defined table(s) from given database.

		Parameter:
		string database Database which should be used.
		string table Explicit table which should be checked if it's available.

		Return:
		list List of checked tables, if parameter 'table' is None, all table from
		the given database are returned.
		"""

		# Check
		if not database or not isinstance(database, str): raise TypeError

		# Create return array
		tables=[]

		# Create cursor
		cursor=self.__dbConnection.cursor()

		# Retrieve all tables from database
		query="SHOW TABLES FROM %s%s" % (database, (" LIKE '%s'" % table) if table else "")
		cursor.execute(query)

		# Gather rows of tables
		if cursor.rowcount==0: 
			if table:
				raise NoTableFound("%s => %s" % (database, table))
			else:
				raise NoTablesFound(database)
			# End if
		else:
			[ tables.append(row[0]) for row in cursor.fetchall() ]
		# End if

		# Close cursor
		cursor.close()

		# Return tables-array
		return tables
	# End def

	def YieldRowsFromTable(self, database, table, limit=None):
		"""Yield-Generator over the rows of the table. Yields a dictionary.

		Parameter:
		string database Database which should be used.
		string table Table which should be used.
		int limit SQL-Limit appended to the executed sql, like "... LIMIT 50"
		"""

		# Check
		if not database or not isinstance(database, str): raise TypeError
		if not table or not isinstance(table, str): raise TypeError
		if limit and not isinstance(limit, int): raise TypeError

		query="SELECT * FROM %s.%s%s" % (database, table, " LIMIT %i" % limit if limit else "")
		for row in self.YieldRowsFromSQL(query): yield row
	# End def

	def YieldRowsFromSQL(self, sql):
		"""Yield-Generator over the rows of the result of the sql. Yields a dictionary.

		Parameter:
		string sql SQL which should be executed and yielded.
		"""

		# Create cursor
		cursor=self.__dbConnection.cursor(MySQLdb.cursors.DictCursor)

		# Yield rows from table
		cursor.execute(sql)

		if cursor.rowcount>0:
			while (1):
				row=cursor.fetchone()
				if not row: break;

				yield row
			# End while

			raise StopIteration
		else:
			raise StopIteration
		# End if
	# End def
# End class

