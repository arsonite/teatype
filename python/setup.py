# Copyright (C) 2024-2025 Burak Günaydin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# System imports
import os
import requests

# From system imports
from typing import List

# From package imports
from setuptools import setup, find_packages

# From-as package imports
from setuptools.command.sdist import sdist as _sdist

# From local imports
# from teatype import __version__

PARENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
with open('version.txt') as f:
    __VERSION__ = f.read().strip()

# Custom `sdist` command to include/exclude files from source distribution
class sdist(_sdist):
    def make_release_tree(self, base_dir, files):
        _sdist.make_release_tree(self, base_dir, files)
        # Exclude specific files
        exclude_files = ['.env', 'tests/*', '*.log', '*.pyc', 'scripts/*']
        for filename in exclude_files:
            filepath = os.path.join(base_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                
def gather_requirements(variants:List[str]):
    for file in os.listdir('requirements'):
        if file.endswith('.txt'):
            with open(os.path.join('requirements', file)) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        yield line
                
def ask_for_version():
    """
    Asks the user for a new version or auto-increments the latest version.

    Returns:
        str: The determined version string.
    """
    return __VERSION__
    with open("requirements.txt") as f:
        # Read all lines from 'requirements.txt' and split them into a list
        install_requires = f.read().splitlines()
        
        def get_existing_versions(package_name):
            """
            Fetches all existing versions of a package from PyPI.

            Args:
                package_name (str): The name of the package to retrieve versions for.

            Returns:
                List[str]: A sorted list of version strings.
            """
            response = requests.get(f'https://pypi.org/pypi/{package_name}/json')
            if response.status_code != 200:
                # If the package is not found or another error occurs, return an empty list
                return []
            data = response.json()
            # Sort the versions numerically
            return sorted(
                data['releases'].keys(),
                key=lambda s: list(map(int, s.split('.')))
            )
        
        def increment_version(version):
            """
            Increments the patch version of a semantic version string.
            Rolls over to the next minor version if patch reaches 10,
            and to the next major version if minor reaches 10.

            Args:
                version (str): The current version string in 'major.minor.patch' format.

            Returns:
                str: The incremented version string.
            """
            major, minor, patch = map(int, version.split('.'))
            patch += 1  # Increment the patch version
            if patch >= 10:
                patch = 0
                minor += 1  # Increment the minor version
                if minor >= 10:
                    minor = 0
                    major += 1  # Increment the major version
            return f"{major}.{minor}.{patch}"
        
        package_name = 'teatype'
        # Retrieve all existing versions of the package from PyPI
        existing_versions = get_existing_versions(package_name)
        if existing_versions:
            latest_version = existing_versions[-1]  # Get the latest version
            # Prompt the user to enter a new version or auto-increment
            user_version = input(
                f'Latest version is {latest_version}. Enter new version or press Enter to auto-increment: '
            )
            if not user_version:
                # If no input is provided, automatically increment the latest version
                new_version = increment_version(latest_version)
            else:
                new_version = user_version  # Use the user-provided version
        version = new_version  # Set the determined version

# Detect variants via env var or command line arg
variants = ['base', 'test'] # default
# if '--gpu' in sys.argv:
#     variant = 'gpu'
#     sys.argv.remove('--gpu')
# if '--fastapi' in sys.argv:
#     variant = 'fastapi'
#     sys.argv.remove('--fastapi')
# if '--django' in sys.argv:
#     variant = 'django'
#     sys.argv.remove('--django')
# # Conditional packages
# packages = find_packages()
# if variant == 'cpu':
#     # Remove AI folder
#     packages = [package for package in packages if not package.startswith('teatype.ai')]
# # Conditional dependencies
# if variant == 'gpu':
#     install_requires.append('llama-cpp-python')
INSTALL_REQUIRES = list(gather_requirements(variants))

# Package name adjustment
PACKAGE_NAME = 'teatype-gpu' if 'gpu' in variants else 'teatype'
VERSION = ask_for_version()

setup(
    author='arsonite',
    author_email='notarson@gmail.com',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Own License',
        'Operating System :: OS Independent',
    ],
    cmdclass={
        # 'develop': deploy,
        # 'install': deploy,
        'sdist': sdist
    },
    description='A package for tea',
    install_requires=INSTALL_REQUIRES,
    name=PACKAGE_NAME,
    packages=find_packages(),
    python_requires='>=3.11',
    url='https://github.com/arsonite/teatype',
    version=VERSION,
)