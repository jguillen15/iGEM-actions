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
import sbol_utilities.sbol_diff

package = scripts.scriptutils.package_dirs()

class TestIDTCalculateComplexityScore(unittest.TestCase):

    @unittest.skipIf(sys.platform == 'win32', reason='Not working on Windows https://github.com/SynBioDex/SBOL-utilities/issues/221')
    def test_IDT_calculate_complexity_score(self):
        """Test that a library-call invocation of complexity scoring works"""

        secret_input = os.getenv('SECRET_INPUT')  # Note: GitHub actions inputs are prefixed with 'INPUT_' and converted to uppercase with '-' replaced by '_'
        if secret_input:
            print(f'The secret is: {secret_input}')
        else:
            print('Secret input not found.')

        # File path where the JSON file will be created
        root = git.Repo('.', search_parent_directories=True).working_tree_dir
        file_path = os.path.join(root, 'test_secret_idt_credentials.json')
        print("Credentials JSON path: ", file_path)
        with open(file_path) as test_credentials:
            idt_accessor = IDTAccountAccessor.from_json(json.load(test_credentials))


        """test_dir = Path(__file__).parent
        with open(test_dir.parent / 'test_secret_idt_credentials.json') as test_credentials:
            idt_accessor = IDTAccountAccessor.from_json(json.load(test_credentials)) """

        doc = sbol3.Document()
        doc.read(root / 'test_files' / 'BBa_J23101.nt')

        # Check the scores - they should initially be all missing
        sequences = [obj for obj in doc if isinstance(obj, sbol3.Sequence)]
        scores = get_complexity_scores(sequences)
        self.assertEqual(scores, dict())
        # Compute sequences for
        results = idt_calculate_sequence_complexity_scores(idt_accessor, sequences)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[sequences[0]], 0)  # score is zero because the sequence both short and easy
        scores = get_complexity_scores(sequences)
        self.assertEqual(scores, results)

        # Compute results again: results should be blank, because the calculation is already made
        results = idt_calculate_complexity_scores(idt_accessor, doc)
        self.assertEqual(len(results), 0)
        self.assertEqual(results, dict())
        scores = get_complexity_scores(sequences)
        self.assertEqual(scores, {sequences[0]: 0})

if __name__ == '__main__':
    unittest.main()