import os
import sys
import scriptutils

error = False
package = scriptutils.package_dirs()
print(f'Scanning; found {len(package)} package')

try:
    scriptutils.regularize_directory(package)
except ValueError as e:
    print(f'Bad structure for package {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
