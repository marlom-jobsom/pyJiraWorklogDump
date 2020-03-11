# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC

from core.jira_server.beans.JiraUser import JiraUser
from utils import moment


class AbstractJiraIssue(ABC):
    """An abstract JIRA issue"""

    def __init__(self, issue):
        """
        :param jira.resources.Issue issue:
        """
        self._key = issue.key
        self._created_at = moment.jira_date_to_datetime(issue.fields.created)
        self._updated_at = moment.jira_date_to_datetime(issue.fields.updated)
        self._status = issue.fields.status.name
        self._status_category = issue.fields.status.statusCategory.key
        self._summary = issue.fields.summary
        self._assignee = JiraUser(issue.fields.assignee)
        self._issue_type = issue.fields.issuetype.name

    def __str__(self):
        """
        :return str:
        """
        return type(self).__name__

    @staticmethod
    def get_jira_fields():
        """
        :return list:
        """
        return ['created', 'updated', 'status', 'summary', 'assignee', 'issuetype']

    @staticmethod
    def get_expected_types():
        """
        :return list:
        """
        raise NotImplementedError('Missing expected JIRA types name')

    def build_csv_data(self):
        """
        :return dict:
        """
        return {
            'key': self._key,
            'created at': self._created_at,
            'updated at': self._updated_at,
            'status': self._status,
            'summary': self._summary,
            'assignee': self._assignee.name,
            'issue type': self._issue_type}

    @property
    def key(self):
        """
        :return str:
        """
        return self._key

    @property
    def created_at(self):
        """
        :return datetime.datetime:
        """
        return self._created_at

    @property
    def updated_at(self):
        """
        :return datetime.datetime:
        """
        return self._updated_at

    @property
    def status(self):
        """
        :return str:
        """
        return self._status

    @property
    def status_category(self):
        """
        :return str:
        """
        return self._status_category

    @property
    def summary(self):
        """
        :return str:
        """
        return self._summary

    @property
    def assignee(self):
        """
        :return JiraUser:
        """
        return self._assignee

    @property
    def issue_type(self):
        """
        :return str:
        """
        return self._issue_type
