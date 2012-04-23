import re
import couchdb
from ConnectionBase import *

class CouchConnection(ConnectionBase):
	"""Class which implements methods to connect to a couch-db, retrieve some
	data, aso."""

	CREATION_TYPE_DB="db"
	CREATION_TYPE_TBL="tbl"
	CREATION_TYPE_DB_TBL="db_tbl"

	def __init__(self, connectionString=None, username=None, password=None, host="localhost", port=5984):
		"""Initializes the object with given parameters, like username, password, aso. Will not open
		the connection to the sql database. Use method 'Connect' instead.
		
		Parameter:
		See also ConnectionBase.__init__(...)
		"""

		super(self.__class__, self).__init__(connectionString=connectionString, username=username, password=password, host=host, port=port)
	# End def

	def Connect(self):
		"""Connects to the currently defined couch-db-host via currently defined authorization."""

		# Not actually a connect, but rather check if Couch is online.
		connectURL="%s%s%s%s" % (
			self.GetProtocol() if self.GetProtocol() else "http://",
			("%s:%s@" % (self.GetUsername(), self.GetPassword())) if self.GetUsername() and self.GetPassword() else "",
			"%s" % self.GetHost() if self.GetHost() else "",
			":%i" % self.GetPort() if self.GetPort() else ""
		)
		self.__dbConnection=couchdb.client.Server(connectURL)
	# End def

	def IsDatabase(self, database):
		"""Checks if given database is available.
		
		Parameter:
		string database The database to checked if it' available.

		Return:
		bool True if database is available, false, if not.
		"""

		# Check
		if not database or not isinstance(database, str): raise TypeError

		# Return if database is available
		return database in self.__dbConnection
	# End def

	def GetValidDatabaseName(self, database):
		"""Returns a valid name for a couch-db database.

		References:
		Information about a valid database name taken from ...
		http://wiki.apache.org/couchdb/HTTP_database_API#PUT_.28Create_New_Database.29

		"...A database must be named with all lowercase letters (a-z), digits (0-9), or any of
		the _$()+-/ characters and must end with a slash in the URL. The name has to start with
		a lowercase letter (a-z)..."

		Return:
		string Valid database name.
		"""
		# Check
		if not database or not isinstance(database, str): raise TypeError

		return re.sub(r"(^[^a-z]|[^a-z0-9_\$\(\)\+\-]+)", "_", database)
	# End def

	def CreateDatabase(self, database):
		"""Creates a new database.

		Parameter:
		string database The name of the database to be created.
		"""

		# Check
		if not database or not isinstance(database, str): raise TypeError
		
		# Create database
		try:
			self.__dbConnection.create(database)
		except:
			raise CouchCreateDatabase
		# End try/except
	# End def

	def WriteDoc(self, database, docObject):
		"""Writes given object to the database.

		Parameter:
		dict docObject Dictionary-Object which should be written to couch-db.
		"""

		# Check
		if not database or not isinstance(database, str): raise TypeError
		if not docObject or not isinstance(docObject, dict): raise TypeError

		# Check if database is available
		# Database available
		if self.IsDatabase(database):
			try:
				docId, docRev=self.__dbConnection[database].save(docObject)
				return {"docId": docId, "docRev": docRev}
			except:
				raise CouchWriteDocument
			# End try/except
		# Database not available
		else:
			raise NoDatabaseFound(database)
		# End if
	# End def

	def Disconnect(self): super(self.__class__, self).Disconnect()
	
	def ExecuteSQL(self, sql): super(self.__class__, self).ExecuteSQL(sql)

	def GetDatabases(self, databases=[""]): super(self.__class__, self).GetDatabases(databases)

	def GetTablesFromDatabase(self, database, table=None): super(self.__class__, self).GetTablesFromDatabase(database, table)

	def YieldRowsFromSQL(self, sql): super(self.__class__, self).YieldRowsFromSQL(sql)

	def YieldRowsFromTable(self, database, table, limit=None): super(self.__class__, self).YieldRowsFromTable(database, table, limit)
# End class



