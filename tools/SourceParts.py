#!/usr/bin/python
#! -*- coding: utf-8 -*-

import re

class SourceParts:
	"""Class for simply handling 'source-parts', like database and table."""

	def __init__(self, sourceString=None, dbSource=None, tableSource=None):
		"""Initializes the object with given parameters.

		Parameter:
		string sourceString See also 'SplitSourceString'
		string dbSource The database-part of the source, see also 'Set-/GetDatabase'.
		string tableSource The table-part of the source, see also 'Set-/GetDatabase'.
		"""

		self.__database, self.__table=dbSource, tableSource

		# Analyse/Split SourceString
		if sourceString!=None: self.SplitSourceString(sourceString)
	# End def

	def SetDatabase(self, database):
		"""Sets the database-part of the source.

		Parameter:
		string database The database to be set as a part.
		"""

		# Check
		if database and not isinstance(database, str): raise TypeError

		self.__database=database
	# End def

	def GetDatabase(self):
		"""Returns the database-part of the source."""

		return self.__database
	# End def

	def SetTable(self, table):
		"""Sets the table-part of the source.

		Parameter:
		string table The table to be set as a part.
		"""

		# Check
		if table and not isinstance(table, str): raise TypeError

		self.__table=table
	# End def

	def GetTable(self):
		"""Returns the table-part of the source."""

		return self.__table
	# End def

	def SplitSourceString(self, sourceString):
		"""Splits the given source-string into database and, if given, table.

		Parameter:
		string sourceString The source-string to be splitted, syntax: database[.table]

		Return:
		bool True if source-parts could be splitted, False if not.
		"""

		# Check
		if sourceString and not isinstance(sourceString, str): raise TypeError

		sourceParts=re.match(r"(?P<database>.*?)(?:\.|$)(?P<table>.*)$", sourceString)

		if sourceParts:
			# Database-Source
			self.SetDatabase(sourceParts.group("database"))
			# Table-Source
			self.SetTable(sourceParts.group("table"))
			return True
		else:
			return False
		# End if
	# End def

# End class


