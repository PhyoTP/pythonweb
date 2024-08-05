"""Activate a Python virtual environment.

This file can be used to activate a virtual environment from within a Python script.

The activation consists of:
- Adding the virtual environment's site-packages to sys.path
- Setting the sys.prefix and sys.exec_prefix to the virtual environment's paths
- Modifying the `PATH` and other environment variables
"""

import os
import site
import sys

def activate_virtualenv():
    # Virtual environment path
    venv_path = os.path.dirname(os.path.abspath(__file__))

    # Add the virtual environment's site-packages to sys.path
    site_packages = os.path.join(venv_path, 'lib', 'python' + sys.version[:3], 'site-packages')
    if site_packages not in sys.path:
        sys.path.append(site_packages)

    # Set the sys.prefix and sys.exec_prefix to the virtual environment's path
    sys.prefix = venv_path
    sys.exec_prefix = venv_path

    # Update the PATH environment variable
    os.environ['PATH'] = os.path.join(venv_path, 'bin') + os.pathsep + os.environ.get('PATH', '')

    # Set the VIRTUAL_ENV environment variable
    os.environ['VIRTUAL_ENV'] = venv_path

# Activate the virtual environment
activate_virtualenv()
