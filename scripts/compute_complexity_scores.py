import os
import sys

import scriptutils
import calculate_complexity_scores
#from sbol_utilities.calculate_complexity_scores.py
from pathlib import Path
from unittest.mock import patch

error = False
package = scriptutils.package_dirs()


print(f'Calculating complexity scores for {os.path.basename(package)}')
try:
    """Test that a command-line invocation of complexity scoring works"""
    test_dir = Path(__file__).parent
    test_args = ['calculate_complexity_scores.py',
                     '--credentials', str(test_dir.parent / 'test_secret_idt_credentials.json'),
                     str(package / 'views' / 'package.nt'), 'distro_output.nt']
    with patch.object(sys, 'argv', test_args):
        calculate_complexity_scores.main()

except (OSError, ValueError) as e:
    print(f'Could not calculate complexity scores for {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
