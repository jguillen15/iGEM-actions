import os
import sys
import scriptutils

error = False
package = scriptutils.package_dirs()

print(f'Exporting SBOL from Excel for package {os.path.basename(package)}')
try:
    doc = scriptutils.export_sbol(package)
    print(f'  {len(doc.objects)} designs and collections exported')
except (OSError, ValueError) as e:
    print(f'Could not export SBOL file for package {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
