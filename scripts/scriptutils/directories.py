import os
import glob
from typing import List

import git

EXPORT_DIRECTORY = 'views'
"""Export directory into which sheets and other products will be placed"""
EXPORT_SHEETS = ['Parts and Devices', 'Libraries and Composites']
"""List of sheets to export, which will be written as CSVs with the same name"""
SBOL_EXPORT_NAME = 'package_specification.nt'
"""Name of the base SBOL3 export name (not filled in with details)"""
SBOL_PACKAGE_NAME = 'package.nt'
"""Name of the fully assembled SBOL3 package"""

DISTRIBUTION_NAME = 'distribution.nt'
"""File name for the distribution as a whole, to be located in the root directory"""
DISTRIBUTION_FASTA = 'distribution_synthesis_inserts.fasta'
"""File name for the distribution FASTA export for synthesis, to be located in the root directory"""
DISTRIBUTION_GENBANK = 'distribution.gb'
"""File name for the distribution GenBank export for synthesis/review, to be located in the root directory"""


def distribution_dir() -> str:
    """Returns the root directory for the distribution.

    :return: Path for distribution directory
    """
    root = git.Repo('.', search_parent_directories=True).working_tree_dir
    return root


def package_dirs() -> str:
    """Find all packages in the repository

    Returns
    -------
    String defining package directory path name
    """
    root = git.Repo('.', search_parent_directories=False).working_tree_dir
    print(f"Package path: {root}")
    
    return root


def package_excel(directory) -> str:
    """Check that there is exactly one excel package file (ignoring temp-files)

    Returns
    -------
    Path to package Excel file
    """
    excel_files = [f for f in map(os.path.basename, glob.glob(os.path.join(directory, '*.xlsx')))
                   if not f.startswith('~$')]
    print(excel_files)
    if len(excel_files) == 0:
        raise ValueError(f' Could not find package excel file')
    elif len(excel_files) > 1:
        raise ValueError(f' Found multiple Excel files in package: {excel_files}')
    else:
        print(f"Success: found one excel file: {excel_files}")
        return os.path.join(directory, excel_files[0])


def regularize_directory(dir: str):
    """Ensure that a package has one export directory, no other subdirectories, and precisely one package Excel file
    Ignores subdirectories related to git and scripting.
    """
    # Check that there is exactly one subdirectory
    ignore_dirs = {'scripts', '.git', '.github'}
    sub_dirs = [s for s in os.scandir(dir) if s.is_dir() and not s.name in ignore_dirs]
    if len(sub_dirs) == 0:
        os.mkdir(os.path.join(dir, EXPORT_DIRECTORY))
        print(f' Created missing export directory {EXPORT_DIRECTORY}')
    elif len(sub_dirs) == 1:
        if not sub_dirs[0].name == EXPORT_DIRECTORY:
            raise ValueError(f' Found unexpected subdirectory: {sub_dirs[0]}')
    else:  # more than one
        raise ValueError(
            f' Found unexpected subdirectories: {"".join(s.name for s in sub_dirs if not s.name == EXPORT_DIRECTORY)}')

    # Confirm that package excel file can be located
    package_excel(dir)
