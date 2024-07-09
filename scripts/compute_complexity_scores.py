import os
import sys
import json

import scriptutils
#import sbol_utilities.calculate_complexity_scores
import calculate_complexity_scores
from pathlib import Path
from unittest.mock import patch
from scriptutils.directories import EXPORT_DIRECTORY, SBOL_EXPORT_NAME, DISTRIBUTION_NAME

error = False
package = scriptutils.package_dirs()


print(f'Calculating complexity scores for {os.path.basename(package)}')

secret_input = os.getenv('SECRET_INPUT')  # Note: GitHub actions inputs are prefixed with 'INPUT_' and converted to uppercase with '-' replaced by '_'
if secret_input:
    print(f'The secret is: {secret_input}')
else:
    print('Secret input not found.')

# File path where the JSON file will be created
file_path = os.path.join(package, 'test_secret_idt_credentials.json')

# Writing data to the JSON file
with open(file_path, 'w') as json_file:
    json.dump(secret_input, json_file, indent=4)

print(f"JSON file has been created at: {file_path}")

try:
    """Test that a command-line invocation of complexity scoring works"""
    test_dir = Path(__file__).parent
    test_args = ['calculate_complexity_scores.py',
                     '--credentials', file_path,
                     os.path.join(package, EXPORT_DIRECTORY, DISTRIBUTION_NAME), 'distro_output.nt']
    with patch.object(sys, 'argv', test_args):
        calculate_complexity_scores.main()

except (OSError, ValueError) as e:
    print(f'Could not calculate complexity scores for {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
