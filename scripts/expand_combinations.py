import os
import sys

import scriptutils

error = False
package = scriptutils.package_dirs()


print(f'Expanding package build plan {os.path.basename(package)}')
try:
    scriptutils.expand_build_plan(package)

except (OSError, ValueError) as e:
    print(f'Could not compute build plan for {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
