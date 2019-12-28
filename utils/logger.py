# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Application logger"""

import logging
import sys

_logger = logging.getLogger('jira_worklog_dump')
_logger.setLevel(logging.INFO)
_formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(funcName)s:%(message)s')

_console_output_handler = logging.StreamHandler(sys.stdout)
_console_output_handler.setLevel(logging.INFO)
_console_output_handler.setFormatter(_formatter)

_logger.addHandler(_console_output_handler)

info = _logger.info
warning = _logger.warning
