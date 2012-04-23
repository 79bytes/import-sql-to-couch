#!/usr/bin/python
#! -*- coding: utf-8 -*-

class NoDatabaseFound(Exception):
	"""Exception for if one explicit database cannot be found."""
	pass

class NoDatabasesFound(Exception):
	"""Exception for if no databases where found."""
	pass

class NoTableFound(Exception):
	"""Exception for if one explicit table cannot be found."""
	pass

class NoTablesFound(Exception):
	"""Exception for if no tables where found in database."""
	pass

class SQLExecutionFailed(Exception):
	"""Exception for if a sql-execution failed."""
	pass

class CouchCreateDatabase(Exception):
	"""Exception for if a database cannot be created."""
	pass

class CouchWriteDocument(Exception): 
	"""Exception for if a doc cannot be written to couch."""
	pass
