#!/usr/bin/env python3

from optparse import OptionParser
import os

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option( "-p", "--path", action="store", type="string", dest="wowpath", default="/Applications/World of Warcraft/",
			help="Path to look for addons.")

	(options, args) = parser.parse_args()

	print( "Warcraft path: %s" % (options.wowpath, ) )

	print( os.path.exists( options.wowpath ) )
