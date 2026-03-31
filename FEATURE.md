# Features

## Design persistance DB and strucutre

~/.addon_updater/addons.json
~/.addon_updater/cache/ID/zip1.zip
~/.addon_updater/working/zip1/Files

DB:

WoWInstalls:
list of wow paths (need to have "Interface" as a sub directory to be valid)


Addons:
Service | addonID | current version






Installs:
id | path

Addons:
installID | service | addonID | current version




## Calling convention

Calling with no parameters (dryrun), will update caches (download new addons), and report which ones will be updated.

Calling with -x and no other parameters will update caches, and update installs for all addons for all wow installs.

Calling with a specific path will update that path only.

Calling with addon data only will either install for all wow installs, or update just that one addon for any install.




