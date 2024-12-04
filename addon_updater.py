#!/usr/bin/env python3

from argparse import ArgumentParser
import os
# import logging
import sqlite3

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

	parser.add_argument( "-p", "--path", dest="wowpath", nargs="*", metavar="PATH", default=["/Applications/World of Warcraft/"],
			help="Path to look for addons." )
	parser.add_argument( "--curseforge", dest="addcurseforge", nargs="*", metavar="ADDONID",
			help="Add addon id from curseforge." )


	options = parser.parse_args()
	print( options )

	wowInstances = []
	for wowpath in options.wowpath:
		wowInstances.append( WoWInstance(wowpath) )
	print( wowInstances )

	for instance in wowInstances:
		for addon in instance.addons:
			print( addon )



	# print( wowpath )

	# print( "Warcraft path: %s" % (wowpath, ) )

	# print( os.path.exists( wowpath ) )
