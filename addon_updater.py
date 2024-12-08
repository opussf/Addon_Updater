#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import logging
import sqlite3

class DataStorage:
	""" Singleton datastorage object """
	_instance = None
	basePath = "~/.addon_uppdater"
	sqliteFilename = "addons.db"
	# paths = ["cache","working"]

	def __new__( cls, *args, **kwargs ):
		if not cls._instance:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__( self ):
		self.fullPath = os.path.expanduser( self.basePath )
		if not os.path.exists(self.fullPath):
			os.makedirs( self.fullPath, exist_ok=True )
		# Make the sqllite storage file, connection, and cursor
		self.sqliteFile = os.path.join( self.fullPath, self.sqliteFilename )
		self.connection = sqlite3.connect( self.sqliteFile )

		self.cursor = self.connection.cursor()
		self.cursor.execute("VACUUM")
		self.connection.commit()

	def commit( self ):
		self.connection.commit()

	def __del__( self ):
		print( "On delete" )
		self.connection.close()

class Cache:
	path = "cache"
	def __init__( self ):
		print( "Cache.__init__" )

class Installs:
	def __init__( self, dataStorage ):
		self.dataStorage = dataStorage
		self._wowpaths = []

		self.cursor = self.dataStorage.cursor
		try:
			self.cursor.execute( "CREATE TABLE installs(id integer primary key, path string unique)" )
		except sqlite3.OperationalError:
			pass
		print( "installs init")
		for row in self.cursor.execute("SELECT id, path from installs;"):
			print( "Row: ", row )
			self._wowpaths.append( row[1] )

	@property
	def wowpaths(self):
		print("Get property")
		return self._wowpaths

	@wowpaths.setter
	def wowpaths(self,value):
		self._wowpaths = value
		for path in self._wowpaths:
			try:
				self.cursor.execute( "INSERT INTO installs (path) values(?)", (path,) )
			except sqlite3.IntegrityError:
				pass
		self.dataStorage.commit()

class AddonData:
	"""Addons:
		installID | service | addonID | current version
	"""
	def __init__( self ):
		self.cursor = DataStorage()

class AddonInfo:
	""" Addon Info Class
	Has access methods to get addon info
	"""
	def __init__( self, path):
		print( "AddonInfo: %s" % (path,) )

class AddonIterator:
	""" Becomes a wrapper around the list iterator """
	def __init__( self, basePath ):
		print( basePath )
		self.basePath = basePath
	def __iter__( self):
		self.scandirIterator = os.scandir( self.basePath )
		return self   # The iterator object is returned
	def __next__( self):
		while True:
			f = next( self.scandirIterator )
			if f.is_dir():
				break
		return AddonInfo(f)

class WoWInstance:
	""" WoWInstance Class
	This class takes a path, confirms the path, exposes a few helper functions.
	The path should point to the base install path.  folders like _retail_ should be here.
	"""
	__subPaths = ["_retail_", "Interface", "Addons"]
	def __init__( self, path):
		for subPathLen in range(len( self.__subPaths)+1):
			checkPath = os.path.join( path, *self.__subPaths[:subPathLen])
			if not os.path.exists( checkPath):
				print( "%s does not exist." % ( checkPath,) )
			self.addonPath = checkPath
		self.path = path
		self.addons = AddonIterator( self.addonPath )

	def something(self):
		pass

if __name__ == "__main__":
	parser = ArgumentParser(description="WoW Addon Updater version ")

	parser.add_argument( "-p", "--paths", dest="wowpaths", nargs="*", metavar="PATH",
			help="Path to look for addons." )
	parser.add_argument( "--curseforge", dest="addcurseforge", nargs="*", metavar="ADDONID",
			help="Add addon id from curseforge." )
	parser.add_argument( "--github", dest="addgithub", nargs="*", metavar="REPOPATH",
			help="Add addon from github." )
	parser.add_argument( "-v", "--verbose", dest="verbose", action="store_true", default=False,
			help="Verbose mode." )

	options = parser.parse_args()

	logger = logging.getLogger("addon_uppdater")
	logger.setLevel(logging.DEBUG)
	sh = logging.StreamHandler()
	sh.setLevel(options.verbose and logging.DEBUG or logging.INFO)

	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	sh.setFormatter(formatter)
	logger.addHandler(sh)

	logger.info("Starting")

	myInstalls = Installs( DataStorage() )
	if options.wowpaths:
		print( "wowpath: %s (%s)" % (options.wowpaths,type(options.wowpaths)) )
		myInstalls.wowpaths = options.wowpaths

	myWowPaths = myInstalls.wowpaths
	print( "myWowPaths: %s" % (myWowPaths,) )



	# addonData = AddonData()

	# if options.wowpath:
	# 	print(options.wowpath[0])
	# 	myOptions.wowpath = options.wowpath[0]

	# print(options.wowpath)


	# wowInstances = []
	# for wowpath in options.wowpath:
	# 	wowInstances.append( WoWInstance(wowpath) )
	# print( wowInstances )

	# for instance in wowInstances:
	# 	for addon in instance.addons:
	# 		print( addon )



	# print( wowpath )

	# print( "Warcraft path: %s" % (wowpath, ) )

	# print( os.path.exists( wowpath ) )
