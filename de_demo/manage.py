#!/usr/bin/env python
import os
import sys
from os.path import join, dirname, abspath


app_path = abspath(join(dirname(abspath(__file__)), '..'))
sys.path.append(app_path)


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
