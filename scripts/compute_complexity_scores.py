import os
import sys
import json
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

secret_input = os.getenv('SECRET_INPUT')  # Get the IDT Credentials

# File path where the JSON file will be created
file_path = os.path.join(package, 'test_secret_idt_credentials.json')

try:
     # Get the collection of linear build products - the things to actually be synthesized
    print(f'Exporting files for synthesis')
    doc = sbol3.Document()
    doc.read(os.path.join(package, EXPORT_DIRECTORY, SBOL_PACKAGE_NAME)) 

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

    with open(file_path) as credentials:
            idt_accessor = IDTAccountAccessor.from_json(json.load(credentials))

    results = idt_calculate_sequence_complexity_scores(idt_accessor, sequences)
    doc.write(os.path.join(package, EXPORT_DIRECTORY, SBOL_PACKAGE_NAME), sbol3.SORTED_NTRIPLES)
    print(f'SBOL file written to {package} with {len(results)} new complexity scores calculated')

except (OSError, ValueError) as e:
    print(f'Could not calculate complexity scores for {os.path.basename(package)}: {e}')
    error = True

# If there was an error, flag on exit in order to notify executing YAML script
if error:
    sys.exit(1)
