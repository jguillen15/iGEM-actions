from pathlib import Path

import json
import os
import unittest
import sys
import tempfile
import git
import sbol3
from unittest.mock import patch
import scripts
import scripts.scriptutils
from scripts.calculate_complexity_scores import IDTAccountAccessor, idt_calculate_complexity_scores, \
    idt_calculate_sequence_complexity_scores, get_complexity_scores

package = scripts.scriptutils.package_dirs()

class TestIDTCalculateComplexityScore(unittest.TestCase):

    #@unittest.skipIf(sys.platform == 'win32', reason='Not working on Windows https://github.com/SynBioDex/SBOL-utilities/issues/221')
    def test_IDT_compute_complexity_score(self):
        """Test that a library-call invocation of complexity scoring works"""

        secret_input = os.getenv('SECRET_INPUT')  # Note: GitHub actions inputs are prefixed with 'INPUT_' and converted to uppercase with '-' replaced by '_'

        # File path where the JSON file will be created
        root = git.Repo('.', search_parent_directories=True).working_tree_dir
        file_path = os.path.join(root, 'test_secret_idt_credentials.json')
        print("Credentials JSON path: ", file_path)
        with open(file_path) as test_credentials:
            idt_accessor = IDTAccountAccessor.from_json(json.load(test_credentials))

        doc = sbol3.Document()
        doc.read(os.path.join(root, 'scripts', 'test', 'test_files', 'package.nt'))

        # Check the scores - they should initially be all missing
        sequences = [obj for obj in doc if isinstance(obj, sbol3.Sequence)]
        scores = get_complexity_scores(sequences)
        self.assertEqual(scores, dict())
        # Compute sequences for
        results = idt_calculate_sequence_complexity_scores(idt_accessor, sequences)
        print(results)
        self.assertEqual(len(results), 12)
        self.assertEqual(results[sequences[0]], 0)  # score is zero because the sequence is both short and easy
        scores = get_complexity_scores(sequences)
        self.assertEqual(scores, results)


if __name__ == '__main__':
    unittest.main()