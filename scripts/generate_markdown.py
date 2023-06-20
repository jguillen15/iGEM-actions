import os
import sys
import sbol3

import scriptutils

error = False
package = scriptutils.package_dirs()


print(f'Generating README for package {os.path.basename(package)}')
try:
    doc = sbol3.Document()
    doc.read(os.path.join(package, scriptutils.EXPORT_DIRECTORY, scriptutils.SBOL_PACKAGE_NAME))
    scriptutils.generate_package_summary(package, doc)

except (OSError, ValueError) as e:
    print(f'Could not generate README for package {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
