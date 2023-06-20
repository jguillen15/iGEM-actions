import os
import sys
import git

import scriptutils

error = False
package = scriptutils.package_dirs()

print(f'Collating specification and imports into complete package {os.path.basename(package)}')
try:
    scriptutils.collate_package(package)

except (OSError, ValueError) as e:
    print(f'Could not collate package {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
