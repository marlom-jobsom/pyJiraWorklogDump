# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Initialize the application"""

import argparse
import os

from dotenv import load_dotenv

from utils import logger

logger.info('Initializing system variables with `.env` file')
load_dotenv()

APP_NAME = 'JIRA Work-log Dump'
DESCRIPTION = 'Dumps JIRA work-log data of tasks'
HELP_JIRA_URL = 'The URL to JIRA server'
HELP_JIRA_USER = 'The JIRA server login user'
HELP_JIRA_PWD = 'The JIRA server login user password'
HELP_JQL = 'The JQL to be performed at JIRA server'


def get_args():
    """
    :return argparse.Namespace: the arguments from CLI interface
    """
    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument(
        '--jira_url', type=str, help=HELP_JIRA_URL, default=_get_jira_url(), required=True)
    parser.add_argument(
        '--jira_user', type=str, help=HELP_JIRA_USER, default=_get_jira_user(), required=True)
    parser.add_argument(
        '--jira_password', type=str, help=HELP_JIRA_PWD, default=_get_jira_password(), required=True)
    parser.add_argument(
        '--jql', type=str, help=HELP_JQL, default=_get_jql(), required=True)

    args, _ = parser.parse_known_args()

    return args


def _get_jira_url():
    """
    :return str:
    """
    return os.getenv('JIRA_URL')


def _get_jira_user():
    """
    :return str:
    """
    return os.getenv('JIRA_USER')


def _get_jira_password():
    """
    :return str:
    """
    return os.getenv('JIRA_PASSWORD')


def _get_jql():
    """
    :return str:
    """
    return os.getenv('JQL')
