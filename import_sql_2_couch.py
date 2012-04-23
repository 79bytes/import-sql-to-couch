#!/usr/bin/python
#! -*- coding: utf-8 -*-

# ---- Import required libraries

# System/standard packages
import getpass

# deb-package: python-argparse
from argparse import ArgumentParser

from connections import *
from tools import *

# ----- Main import part

if __name__=="__main__":
	# Name
	PROG_NAME=__file__
	# Version
	PROG_VERSION="$Id$, $Rev$, $Date$"
	# Code Pages URL
	PROG_CODE_PAGES="http://code.google.com/p/import-sql-2-couch/"
	# Description
	PROG_SUMMARY="Simple SQL to CouchDb importer. Define a source, get it in a couch."
	# Epilog
	PROG_EPILOG="For more descriptive information, newer versions and tracking issues/bugs take a look on the code-pages (%s)." % (PROG_CODE_PAGES)

	# Defines sql-database-type
	SQL_TYPE_MYSQL="mysql"
	sqlTypeChoices=[SQL_TYPE_MYSQL]

	# Initialize/Create arguments-parser-object
	argParser=ArgumentParser(description=PROG_SUMMARY, epilog=PROG_EPILOG, add_help=False, prog=PROG_NAME)

	# Adding arguments
	argParser.add_argument("-s", "--sql-connection", help="Defines the SQL-connection, e.g. [http|https://][username:password@]sql-host[:port]", required=True, type=str)
	argParser.add_argument("-ss", "--sql-sources", help="Adds one or more sql db[.table]-sources to the import list, e.g. -ss my_db.my_table -ss second_db", action="append", type=str)
	argParser.add_argument("-st", "--sql-type", help="Defines which type of database 'sql' is, e.g. MySQL, ...", required=True, choices=sqlTypeChoices)
	argParser.add_argument("-sl", "--sql-limit", help="Limits the sql-query to select rows from a db[.table]-source.", default=None, type=int)
	argParser.add_argument("-scsql", "--sql-connect-sql", help="Adds one or more sqls which are executed directly after connecting to the sql-host, useful to set charset-settings.", action="append", type=str)
	argParser.add_argument("-c", "--couch-connection", help="Defines the Couch-connection, e.g. [http|https://][username:password@]couch-host[:port]", required=True, type=str)
	argParser.add_argument("-cct", "--couch-creation-type", help="Defines how the import creates databases within the couch, from db[.table]-source.", choices=[CouchConnection.CREATION_TYPE_DB_TBL, CouchConnection.CREATION_TYPE_DB, CouchConnection.CREATION_TYPE_TBL], default=CouchConnection.CREATION_TYPE_DB_TBL)
	argParser.add_argument("-v", "--verbose", help="Sets verbosity of the import's debug-/information-output.", action="store_const", const=True, default=False)
	argParser.add_argument("-d", "--debug", help="Sets debug-level, actually not executing any changes-operations.", action="store_const", const=True, default=False)
	argParser.add_argument("-h", "--help", help="Prints out this help.", action="help")
	argParser.add_argument("--version", help="Prints out the current version.", action="version", version="%s, %s" % (PROG_NAME, PROG_VERSION) )

	# Parse arguments
	params=argParser.parse_args()

	# Verbosity
	verbosity=Verbosity(params.verbose)

	# SQL Connection
	verbosity.Say("Connect to SQL, %s ..." % params.sql_connection)
	# SQL-Type: MySQL
	if params.sql_type==SQL_TYPE_MYSQL:	sqlConnection=MySQLConnection(connectionString=params.sql_connection)

	# Read username from stdinput
	# Enter username/password via std input
	if sqlConnection.GetUsername()=="?" or sqlConnection.GetPassword()=="?":
		if not params.verbose: print "Connection to sql ..."
		if sqlConnection.GetUsername()=="?": sqlConnection.SetUsername(raw_input("Username: "))
		if sqlConnection.GetPassword()=="?": sqlConnection.SetPassword(getpass.getpass("Password: "))
	# End if

	sqlConnection.Connect()

	# Executing separated sql settings sql-database-settings
	if params.sql_connect_sql:
		for sqlQuery in params.sql_connect_sql:
			verbosity.Say("Executing sql: %s" % sqlQuery)
			if not params.debug: sqlConnection.ExecuteSQL(sqlQuery)
		# End for
	# End if

	verbosity.Say("... connected.")

	# Couch Connection
	verbosity.Say("Connect to Couch, %s ..." % params.couch_connection)
	couchConnection=CouchConnection(connectionString=params.couch_connection)
	# Enter username/password via std input
	if couchConnection.GetUsername()=="?" or couchConnection.GetPassword()=="?":
		if not params.verbose: print "Connection to couch ..."
		if couchConnection.GetUsername()=="?": couchConnection.SetUsername(raw_input("Username: "))
		if couchConnection.GetPassword()=="?": couchConnection.SetPassword(getpass.getpass("Password: "))
	# End if
	couchConnection.Connect()
	verbosity.Say("... connected.")

	# Extend/Validate SQL-Sources
	verbosity.Say("Extend/Validate SQL-Sources ... ")
	if params.sql_sources:
		for source in params.sql_sources:
			# Split source-parts
			sourceParts=SourceParts(source)

			# Check if database is valid
			try:
				sqlConnection.GetDatabases([sourceParts.GetDatabase()])
			except NoDatabaseFound:
				sys.exit("Error: SQL database '%s' not found." % sourceParts.GetDatabase())
			# End try/except

			# Check if table is available and valid
			if sourceParts.GetTable():
				try:
					sqlConnection.GetTablesFromDatabase(sourceParts.GetDatabase(), sourceParts.GetTable())
				except NoTableFound:
					sys.exit("Error: SQL table '%s' in database '%s' not found." % (sourceParts.GetDatabase(), sourceParts.GetTable())) 
				# End try/except
			# End if
		#  End for
	else:
		try:
			params.sql_sources=sqlConnection.GetDatabases()
		except NoDatabasesFound:
			sys.exit("Error: SQL databases not found on host '%s'." % sqlConnection.GetHost())
		# End try/except
	# End if
	verbosity.Say("... extended/validated.")

	verbosity.Say("Using following SQL-Sources for an import: ", params.sql_sources)

	# Import sources
	verbosity.Say("Importing ...")
	for source in params.sql_sources:
		# Split source-parts
		source=SourceParts(source)

		selectDb=source.GetDatabase()
		selectTables=[source.GetTable()] if source.GetTable() else sqlConnection.GetTablesFromDatabase(selectDb)

		for selectTable in selectTables:
			# Create used couch-db-name
			if params.couch_creation_type==CouchConnection.CREATION_TYPE_DB_TBL: couchUsingDb="%s_%s" % (selectDb, selectTable)
			if params.couch_creation_type==CouchConnection.CREATION_TYPE_DB: couchUsingDb=selectDb
			if params.couch_creation_type==CouchConnection.CREATION_TYPE_TBL: couchUsingDb=selectTable

			# Check and eliminate not valid characters for couch-db-name
			couchUsingDb=couchConnection.GetValidDatabaseName(couchUsingDb)

			verbosity.Say("%s.%s (%s)... " % (selectDb, selectTable, couchUsingDb))

			# Check if couch-db is already created
			if couchConnection.IsDatabase(couchUsingDb):
				verbosity.Say("Couch-Database available, already created.")
			else:
				verbosity.Say("Couch-Database not available, creating ...")

				# If not debugging, execute/create database
				try:
					if not params.debug: couchConnection.CreateDatabase(couchUsingDb)
				except:
					sys.exit("Error: Cannot create couch database '%s'" % couchUsingDb)
				# End try/except

				verbosity.Say("... created.")
			# End if

			rowCounter=0
			for row in sqlConnection.YieldRowsFromTable(selectDb, selectTable, params.sql_limit):
				# Increase row-counter
				rowCounter+=1

				# Verbose and write row to couch-doc
				verbosity.Say("Writing couch-doc #%i ..." % rowCounter)

				# If not debugging, execute/write document
				docResult={"docId": "", "docRev": ""}

				try:
					if not params.debug: docResult=couchConnection.WriteDoc(couchUsingDb, row)
				except CouchWriteDocument:
					print "Document: ", row
					sys.exit("Error: Cannot write document to couch.")
				# End try/except

				if docResult:
					verbosity.Say("... written (id: %s, rev: %s)." % (docResult["docId"], docResult["docRev"]))
				# End if
			# End for
		# End for

		verbosity.Say("")
	# End for

# End if
