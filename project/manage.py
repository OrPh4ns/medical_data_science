#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    
    # Set the default Django settings module in the environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Handle ImportError by providing an error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Check the command-line arguments and execute the corresponding task
    if(sys.argv[1]) == "runparser":
        # Import the NasController and start the download task
        from Controllers.NasController import NasController
        nas = NasController()
        nas.download_start(nas.org)
    elif(sys.argv[1]) == "runms" and sys.argv[2] == "sync":
        # Import the NasController and insert data into MSDB
        from Controllers.NasController import NasController
        nas = NasController()
        nas.insert_into_msdb()
    elif(sys.argv[1]) == "mongoparse":
        # Import the Parser module and run the DICOM parsing task
        import Controllers.Parser as Parser
        Parser.parse_dicom()
    elif (sys.argv[1]) == "createdb":
        # Import the MSDatabase module and initialize the database
        import Core.MSDatabase as MSDb
        MSDb.init_db()
    else:
        # Execute the Django management command based on the command-line arguments
        execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
