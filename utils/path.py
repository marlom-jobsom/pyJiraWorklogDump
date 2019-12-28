# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Paths for files and folders into the project
"""

import os

UTILS_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PROJECT_FOLDER_PATH = os.path.dirname(UTILS_FOLDER_PATH)
DUMPS_FOLDER_PATH = os.path.join(ROOT_PROJECT_FOLDER_PATH, 'dumps')


def build_today_dump_folder_path(now):
    """
    :param datetime.datetime now:
    """
    year = str(now.year)
    month = str(now.month)
    day = str(now.day)
    folder_path = os.path.join(DUMPS_FOLDER_PATH, year, month, day)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path
