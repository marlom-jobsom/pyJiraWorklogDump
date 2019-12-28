# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class UnexpectedJiraIssueTypeException(Exception):
    """Raised when an unexpected JIRA issue is given"""

    def __init__(self, issue_type, *args, **kwargs):
        """
        :param str issue_type:
        :param list args:
        :param dict kwargs:
        """
        super().__init__('Unexpected JIRA issue type: "{}"'.format(issue_type), args, kwargs)
