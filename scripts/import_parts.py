import os
import sys
import scriptutils

error = False
package = scriptutils.package_dirs()

print(f'Importing parts for package {os.path.basename(package)}')
scriptutils.import_parts(package)

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
