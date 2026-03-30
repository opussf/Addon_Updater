#!/usr/bin/env python3

from argparse import ArgumentParser
import os
import json
import logging
# import aiohttp
# import asyncio

# import threading


class DataStorage:
	""" Singleton datastorage object """
	_instance = None
	base_path = "~/.addon_updater"
	data_file = "addons.json"
	# paths = ["cache","working"]

	def __new__(cls, *args, **kwargs):
		if not cls._instance:
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, logger: logging.Logger | None = None):
		self.logger = logger
		if not logger:
			self.logger = logging.getLogger("addon_updater")
		self.full_path = os.path.expanduser(self.base_path)
		if not os.path.exists(self.full_path):
			self.logger.debug("Creating path: %s" % (self.full_path,))
			os.makedirs(self.full_path, exist_ok=True)
		# init self.data
		self.data = {}
		# read json file if it exists.
		self.json_file = os.path.join(self.full_path, self.data_file)

		if os.path.exists(self.json_file):
			with open(self.json_file, "r") as f:
				self.data = json.load(f)
		self.logger.debug(f"Data:\n{self.data}")

	def __save(self):
		self.logger.debug("DataStorage: Performing a save")
		# write to the file
		with open(self.json_file, "w") as f:
			json.dump(self.data, f, indent=4)

class Cache:
	path = "cache"

	def __init__(self, dataStorage: DataStorage, logger: logging.Logger | None = None):
		self.logger = logger
		if not logger:
			self.logger = logging.getLogger("addon_updater")
		self.logger.debug("Cache.__init__")


class AddonData:
	"""Addons:
		installID | service | addonID | current version
	"""
	def __init__(self, logger: logging.Logger | None = None):
		self.logger = logger
		if not logger:
			self.logger = logging.getLogger("addon_updater")

	def getFilesURL(self) -> str:
		""" get the url to get a file list
		"""
		raise NotImplementedError


class Curseforge(AddonData):
	"""Just get something started
	https://www.curseforge.com/api/v1/mods/957044/files/7660240/download
	"""
	def __init__(self, cfID: int, logger: logging.Logger | None = None):
		print(logger)
		super().__init__(logger)
		self.cfID = cfID
		self.logger.debug(f"Starting {self.__class__.__name__} with {self.cfID}")

	def getMostRecentFileURL(self) -> str:
		return ""

	def getFilesURL(self) -> str:
		return f"https://www.curseforge.com/api/v1/mods/{self.cfID}/files/"


class GitHub(AddonData):
	"""Also to just get started"""
	def __init__(self, path: str, logger: logging.Logger | None = None):
		super().__init__(logger)
		self.path = path
		self.logger.debug(f"Starting {self.__class__.__name__} with {self.path}")

	# def getFilesURL(self) -> str:
	# 	return ""


class Installs:
	def __init__(self, dataStorage):
		self.logger = logging.getLogger("addon_updater")
		self.dataStorage = dataStorage
		self._wowpaths = []



		# self.cursor = self.dataStorage.cursor
		# try:
		# 	self.cursor.execute("CREATE TABLE installs(id integer primary key, path string unique)")
		# 	self.logger.debug("Installs creating table.")
		# except sqlite3.OperationalError:
		# 	pass
		# for row in self.cursor.execute("SELECT id, path from installs;"):
		# 	self.logger.debug("Row: %s" % (row,))
		# 	self._wowpaths.append(row[1])

	@property
	def wowpaths(self):
		print("Get property")
		return self._wowpaths

	@wowpaths.setter
	def wowpaths(self, value):
		self._wowpaths = value
		# for path in self._wowpaths:
		# 	try:
		# 		self.cursor.execute("INSERT INTO installs (path) values(?)", (path,))
		# 	except sqlite3.IntegrityError:
		# 		pass
		# self.dataStorage.commit()


class AddonInfo:
	""" Addon Info Class
	Has access methods to get addon info
	"""
	def __init__(self, path):
		print("AddonInfo: %s" % (path,))


class AddonIterator:
	""" Becomes a wrapper around the list iterator """
	def __init__(self, basePath):
		print(basePath)
		self.basePath = basePath

	def __iter__(self):
		self.scandirIterator = os.scandir(self.basePath)
		return self   # The iterator object is returned

	def __next__(self):
		while True:
			f = next(self.scandirIterator)
			if f.is_dir():
				break
		return AddonInfo(f)


class WoWInstance:
	""" WoWInstance Class
	This class takes a path, confirms the path, exposes a few helper functions.
	The path should point to the base install path.  folders like _retail_ should be here.
	"""
	__subPaths = ["_retail_", "Interface", "Addons"]

	def __init__(self, path):
		for subPathLen in range(len(self.__subPaths) + 1):
			checkPath = os.path.join(path, *self.__subPaths[:subPathLen])
			if not os.path.exists(checkPath):
				print("%s does not exist." % (checkPath,))
			self.addonPath = checkPath
		self.path = path
		self.addons = AddonIterator(self.addonPath)
		print(self.addons)

	def something(self):
		pass


def setupLogger():
	logger = logging.getLogger("addon_updater")
	logger.setLevel(logging.DEBUG)
	sh = logging.StreamHandler()
	sh.setLevel(options.verbose and logging.DEBUG or logging.INFO)

	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	sh.setFormatter(formatter)
	logger.addHandler(sh)

	return logger


if __name__ == "__main__":
	parser = ArgumentParser(description="WoW Addon Updater version ")

	parser.add_argument("-p", "--paths", dest="wowpaths", nargs="*", metavar="PATH",
			help="Path to look for addons")
	parser.add_argument("--curseforge", dest="curseforgeids", nargs="*", metavar="ADDONID",
			help="Add addon id from curseforge")
	parser.add_argument("--github", dest="githubpaths", nargs="*", metavar="REPOPATH",
			help="Add addon from github")
	parser.add_argument("-v", "--verbose", dest="verbose", action="store_true", default=False,
			help="Verbose mode")
	parser.add_argument("-x", "--execute", dest="dryrun", action="store_false", default=True,
			help="Execute updates (default is dryrun mode)")

	options = parser.parse_args()

	logger = setupLogger()
	logger.info("Starting")

	myInstalls = Installs(DataStorage())
	if options.wowpaths:
		print("wowpath: %s (%s)" % (options.wowpaths, type(options.wowpaths)))
		myInstalls.wowpaths = options.wowpaths

	myWowPaths = myInstalls.wowpaths
	logger.debug("myWowPaths: %s" % (myWowPaths,))

	logger.info(options.curseforgeids)
	logger.info(options.githubpaths)

	addons: list[AddonData] = []
	print(options.curseforgeids)
	if options.curseforgeids:
		for cfID in options.curseforgeids:
			addons.append(Curseforge(cfID))

	print(options.githubpaths)
	if options.githubpaths:
		for github_path in options.githubpaths:
			addons.append(GitHub(github_path))

	logger.info(addons)

	for addon in addons:
		print(addon.getFilesURL())
