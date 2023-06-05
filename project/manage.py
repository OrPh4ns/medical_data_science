#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if(sys.argv[1]) == "runparser":
        from Controllers.NasController import NasController
        nas = NasController()
        nas.download_start(nas.org)
    elif (sys.argv[1]) == "runms" and sys.argv[2] == "sync":
        from Controllers.NasController import NasController
        import Controllers.Parser as parser
        par = parser()
        par.parse_dicom()
        nas = NasController()
        nas.insert_into_msdb()
    else:
        execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
