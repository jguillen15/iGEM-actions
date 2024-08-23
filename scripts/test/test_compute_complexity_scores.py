import json
import os
import unittest
import git
import sbol3
import scripts
from scripts.calculate_complexity_scores import IDTAccountAccessor, idt_calculate_complexity_scores, \
    idt_calculate_sequence_complexity_scores, get_complexity_scores
from scripts.scriptutils.helpers import vector_to_insert

BUILD_PRODUCTS_COLLECTION = 'BuildProducts'
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

        #Filter sequences

        build_plan = doc.find(BUILD_PRODUCTS_COLLECTION)
        if not build_plan or not isinstance(build_plan, sbol3.Collection):
            raise ValueError(f'Document does not contain linear products collection "{BUILD_PRODUCTS_COLLECTION}"')

        # Identify the full constructs and synthesis targets to be copied
        non_components = [m for m in build_plan.members if not isinstance(m.lookup(), sbol3.Component)]
        if len(non_components):
            raise ValueError(f'Linear products collection should contain only Components: {non_components}')

        full_constructs = [m.lookup() for m in sorted(build_plan.members)]

        # For GenBank export, copy build products to new Document, omitting ones without sequences
        sequence_number_warning = 'Omitting {}: Complexity Scores exports require 1 sequence, but found {}'

        for c in full_constructs:
            # if build is missing sequence, warn and skip
            if len(c.sequences) != 1:
                print(sequence_number_warning.format(c.identity, len(c.sequences)))
                build_plan.members.remove(c.identity)
                continue
        
        full_constructs = [m.lookup() for m in sorted(build_plan.members)]
        inserts = [vector_to_insert(c) for c in full_constructs]  # May contain non-vector full_constructs
        sequences = [obj.sequences[0].lookup() for obj in inserts if isinstance(obj, sbol3.Component)]


        # Compute sequences for
        results = idt_calculate_sequence_complexity_scores(idt_accessor, sequences)
        self.assertEqual(len(results), 12)
        scores = list(results.values())
        zeros_list = [0] * 12
        self.assertEqual(scores, zeros_list)  # Scores are zero because the sequences are easy to synthesize



if __name__ == '__main__':
    unittest.main()