#!/usr/bin/env python3

from argparse import ArgumentParser
import os
# import logging
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

	def __del__( self ):
		print( "On delete" )
		self.connection.close()

class Cache:
	path = "cache"
	def __init__( self ):
		print( "Cache.__init__" )

class Options:
	def __init__( self ):
		self.cursor = DataStorage().cursor
		try:
			self.cursor.execute( "CREATE TABLE config(wowpath type UNIQUE)" )
		except sqlite3.OperationalError:
			pass
		print( "option init")
		for row in self.cursor.execute("SELECT wowpath from config"):
			print( "Row: ", row )
			self._wowpath = row[0]

	@property
	def wowpath(self):
		return self._wowpath

	@wowpath.setter
	def wowpath(self,value):
		self._wowpath = value
		try:
			self.cursor.execute( "INSERT INTO config values(?)", (self._wowpath,) )
		except sqlite3.IntegrityError:
			pass



# Addons:
# Service | addonID | current version

class AddonData:
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

	parser.add_argument( "-p", "--path", dest="wowpath", nargs="*", metavar="PATH",
			help="Path to look for addons." )
	parser.add_argument( "--curseforge", dest="addcurseforge", nargs="*", metavar="ADDONID",
			help="Add addon id from curseforge." )


	options = parser.parse_args()
	print( options )

	myOptions = Options()
	addonData = AddonData()

	if options.wowpath:
		print(options.wowpath[0])
		myOptions.wowpath = options.wowpath[0]

	print(options.wowpath)


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
