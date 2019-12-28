# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Handles date/time manipulation"""

from datetime import datetime


def jira_version_date_to_datetime(version_date):
    """
    :param str version_date:
    :return datetime:
    """
    return datetime.strptime(version_date, '%Y-%m-%d')


def jira_date_to_datetime(issue_date):
    """
    :param issue_date:
    :return datetime:
    """
    return datetime.strptime(issue_date, '%Y-%m-%dT%H:%M:%S.%f%z')


def get_now():
    """
    :return datetime:
    """
    return datetime.utcnow()
