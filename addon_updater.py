#!/usr/bin/env python3

from argparse import ArgumentParser
import os

class WoWInstance:
	""" WoWInstance Class
	This class takes a path, confirms the path, exposes a few helper functions.
	"""
	def __init__(self,path):
		self.path = path



if __name__ == "__main__":
	parser = ArgumentParser(description="WoW Addon Updater version ")

	parser.add_argument( "-p", "--path", dest="wowpath", nargs="*", metavar="PATH", default=["/Applications/World of Warcraft/"],
			help="Path to look for addons.")

	options = parser.parse_args()

	for wowpath in options.wowpath:
		print( wowpath )

		print( "Warcraft path: %s" % (wowpath, ) )

		print( os.path.exists( wowpath ) )
