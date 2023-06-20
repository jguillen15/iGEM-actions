import os
import sys
import scriptutils
import git

error = False
root = git.Repo('.', search_parent_directories=True).working_tree_dir

# Create list to allow check for only one excel file
package_path = []
package_name = []

for file in os.scandir(root):
    if file.name.endswith('xlsx') or file.name.endswith('xls'):
        package_path.append(file.path)
        package_name.append(file.name)

# Preliminary check to ensure that there is only one excel package file
if len(package_name) == 1 and len(package_path) == 1:
    package_path = package_path[0]
    package_name = package_name[0] 
    print(f'Only one excel file detected')
else:
    raise ValueError("More than one excel file detected")

print(f'Exporting CSVs for package {package_name}')
print(f'Exporting CSVs from {os.path.dirname(package_path)}')

try:
    scriptutils.export_csvs(package_path)
except OSError as e:
    print(f'Could not export CSV files for package {package_name}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)