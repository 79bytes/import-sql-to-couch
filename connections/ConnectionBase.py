from abc import *
import re
from ImportExceptions import *

class ConnectionBase(object):
	"""Connection-baseclass which implements common methods like  Username, Password, Host, aso. """
	__metaclass__=ABCMeta

	def __init__(self, connectionString=None, username=None, password=None, host=None, port=None):
		"""Initializes the object with given parameters, like username, password, aso. Will not open
		the connection to the sql database. Use method 'Connect' instead.
		
		Should be extended and placeholder-methods should be overwritten.
		
		Parameter:
		string connectionString URL-like connection-string, Syntax: see also method 'SetConnectionString'
		string username Username used for the connection.
		string password Password used for the connection.
		string host Host to connect to.
		int port Port-number to connect to.
		"""

		# Initialize username, password, host, port
		self.__protocol, self.__username, self.__password, self.__host, self.__port=None, username, password, host, port

		# Analyse/Split, if connectionString is given and analyse
		if connectionString!=None: self.SetConnectionString(connectionString)
	# End def

	@abstractmethod
	def Connect(self):
		"""Placeholder-method for extending classes. Does not do anything, but calling 'pass'."""

		pass
	#  End def

	@abstractmethod
	def Disconnect(self):
		"""Placeholder-method for extending classes. Does not do anything, but calling 'pass'."""

		pass
	#  End def

	def SetProtocol(self, protocol):
		"""Sets the used protocol.

		Parameter:
		string protocol Used protocol, e.g. http or https
		"""

		# Check
		if protocol and not isinstance(protocol, str): raise TypeError
		# Update protocol
		self.__protocol=protocol
	# End def

	def GetProtocol(self):
		"""Returns the currently set protocol."""

		return self.__protocol
	# End def

	def SetUsername(self, username):
		"""Sets the used username used for authorization.

		Parameter:
		string username The username.
		"""

		# Check
		if username and not isinstance(username, str): raise TypeError
		# Update Username
		self.__username=username
	# End def

	def GetUsername(self):
		"""Returns the currently set username."""
		return self.__username
	# End def

	def SetPassword(self, password):
		"""Sets the password used for authorization.

		Parameter:
		string password The Password.
		"""

		# Check
		if password and not isinstance(password, str): raise TypeError
		# Update password
		self.__password=password
	# End def

	def GetPassword(self):
		"""Returns the currently set password."""

		return self.__password
	# End def

	def SetHost(self, host):
		"""Sets the host to connect to.

		Parameter:
		string host The host.
		"""

		# Check
		if host and not isinstance(host, str): raise TypeError
		# Update host
		self.__host=host
	# End def

	def GetHost(self):
		"""Returns the currently set host."""

		return self.__host
	# End def

	def SetPort(self, port):
		"""Sets the number of the port to connect to.

		Parameter:
		int port The port.
		"""
		
		# Check
		if port and not isinstance(port, int): raise TypeError
		# Update host
		self.__port=port
	# End def

	def GetPort(self):
		"""Returns the currently set number of the port."""

		return self.__port
	# End def

	def SetConnectionString(self, connectionString):
		"""Splits the given connection-string into different used parts, like username, password, aso.

		Example:
		http://root:my_admin_password@localhost:3306
		http://john:Test1234@sqldata.myexample.com:1234
		...

		Parameter:
		string connectionString URL-like connection-string, Syntax: [http or https://][username:password@]host[:port]
		"""

		# Check
		if not connectionString or not isinstance(connectionString, str): raise TypeError

		# Analyse
		connectionParts=re.search(r"^(?P<protocol>https?:\/\/)?(?:(?P<username>.*?):(?P<password>.*?)@)?(?P<host>.*?)(?::(?P<port>\d*?))?$", connectionString)

		if connectionParts:
			# Protocol
			if connectionParts.group("protocol")!=None: self.SetProtocol(connectionParts.group("protocol"))
			# Username 
			if connectionParts.group("username")!=None: self.SetUsername(connectionParts.group("username"))
			# Password 
			if connectionParts.group("password")!=None: self.SetPassword(connectionParts.group("password"))
			# Host 
			if connectionParts.group("host")!=None: self.SetHost(connectionParts.group("host"))
			# Port
			if connectionParts.group("port")!=None: self.SetPort(int(connectionParts.group("port")))
			return True
		else:
			return False
		# End if
	# End def

	@abstractmethod
	def ExecuteSQL(self, sql):
		"""Placeholder-methos for executing a given sql-query.

		Parameter:
		string sql SQL to be executed.
		"""

		pass
	# End def

	@abstractmethod
	def GetDatabases(self, databases=[""]):
		"""Placeholder-methos for returning (the given) databases after checked if valid.

		Parameter:
		list databases Databases which should be checked if they available.

		Return:
		list List of databases, if parameter 'databases' is empy, actually "", then
		all databases are returned.
		"""

		pass
	#  End def

	@abstractmethod
	def GetTablesFromDatabase(self, database, table=None):
		"""Placeholder-methos for returning defined table(s) from given database.

		Parameter:
		string database Database which should be used.
		string table Explicit table which should be checked if it's available.

		Return:
		list List of checked tables, if parameter 'table' is None, all table from
		the given database are returned.
		"""

		pass
	# End def

	@abstractmethod
	def YieldRowsFromTable(self, database, table, limit=None):
		"""Placeholder-methos for a yield-generator over the rows of the table. Yields a dictionary.

		Mostly should call method 'YieldRowsFromSQL'.

		Parameter:
		string database Database which should be used.
		string table Table which should be used.
		int limit SQL-Limit appended to the executed sql, like "... LIMIT 50"
		"""

		raise StopIteration
	# End def

	@abstractmethod
	def YieldRowsFromSQL(self, sql):
		"""Placeholder-methos for a yield-generator over the rows of the result of the sql. Yields a dictionary.

		Parameter:
		string sql SQL which should be executed and yielded.
		"""

		raise StopIteration
	# End ef

# End class
