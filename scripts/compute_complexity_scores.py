import os
import sys
import json
import logging
import sbol3
import scriptutils
from calculate_complexity_scores import IDTAccountAccessor, idt_calculate_sequence_complexity_scores
from pathlib import Path
from unittest.mock import patch
from scriptutils.directories import EXPORT_DIRECTORY, SBOL_PACKAGE_NAME
from scriptutils.helpers import vector_to_insert

BUILD_PRODUCTS_COLLECTION = 'BuildProducts'
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
#with open(file_path, 'w') as json_file:
#    json.dump(secret_input, json_file, indent=4)

#print(f"JSON file has been created at: {file_path}")
""""
try:
    #Test that a command-line invocation of complexity scoring works
    test_dir = Path(__file__).parent
    test_args = ['calculate_complexity_scores.py',
                     '--credentials', file_path,
                     os.path.join(package, EXPORT_DIRECTORY, SBOL_PACKAGE_NAME), 'package.nt']
    with patch.object(sys, 'argv', test_args):
        calculate_complexity_scores.main()

except (OSError, ValueError) as e:
    print(f'Could not calculate complexity scores for {os.path.basename(package)}: {e}')
    error = True
"""
try:
     # get the collection of linear build products - the things to actually be synthesized
    print(f'Exporting files for synthesis')
    doc = sbol3.Document()
    doc.read(os.path.join(package, EXPORT_DIRECTORY, SBOL_PACKAGE_NAME))#Take package.nt as SBOL document

    build_plan = doc.find(BUILD_PRODUCTS_COLLECTION)
    if not build_plan or not isinstance(build_plan, sbol3.Collection):
        raise ValueError(f'Document does not contain linear products collection "{BUILD_PRODUCTS_COLLECTION}"')

    # identify the full constructs and synthesis targets to be copied
    non_components = [m for m in build_plan.members if not isinstance(m.lookup(), sbol3.Component)]
    if len(non_components):
        raise ValueError(f'Linear products collection should contain only Components: {non_components}')

    full_constructs = [m.lookup() for m in sorted(build_plan.members)]
    #inserts = {c: vector_to_insert(c) for c in full_constructs}  # May contain non-vector full_constructs

    # for GenBank export, copy build products to new Document, omitting ones without sequences
    sequence_number_warning = 'Omitting {}: Complexity Scores exports require 1 sequence, but found {}'
    #build_doc = sbol3.Document()
    #components_copied = set(full_constructs)  # all of these will be copied directly in the next iterator
    #n_genbank_constructs = 0
    for c in full_constructs:
        # if build is missing sequence, warn and skip
        if len(c.sequences) != 1:
            print(sequence_number_warning.format(c.identity, len(c.sequences)))
            build_plan.members.remove(c.identity)
            continue
    
    full_constructs = [m.lookup() for m in sorted(build_plan.members)]
    inserts = [vector_to_insert(c) for c in full_constructs]  # May contain non-vector full_constructs
    print(type(inserts[0]))
    sequences = [obj.sequences[0].lookup() for obj in inserts if isinstance(obj, sbol3.Component)]
    print(len(sequences))
    print(type(sequences[0]))
    with open(file_path) as credentials:
            idt_accessor = IDTAccountAccessor.from_json(json.load(credentials))

    results = idt_calculate_sequence_complexity_scores(idt_accessor, sequences)
    #doc.write(os.path.join(package, EXPORT_DIRECTORY, SBOL_PACKAGE_NAME))
    #logging.info('SBOL file written to %s with %i new scores calculated', "package.nt", len(results))

except (OSError, ValueError) as e:
    print(f'Could not calculate complexity scores for {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
