# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.jira_server.beans.JiraUser import JiraUser
from utils import moment


class JiraWorkLog:
    """Work-log of a JIRA task"""

    def __init__(self, worklog):
        """
        :param jira.resources.Worklog worklog:
        """
        self._author_create = JiraUser(worklog.author)
        self._author_update = JiraUser(worklog.updateAuthor)
        self._created_at = moment.jira_date_to_datetime(worklog.created)
        self._updated_at = moment.jira_date_to_datetime(worklog.updated)
        self._time_spent_in_sec = worklog.timeSpentSeconds

    @property
    def author_create(self):
        """
        :return JiraUser:
        """
        return self._author_create

    @property
    def author_update(self):
        """
        :return JiraUser:
        """
        return self._author_update

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
    def time_spent_in_sec(self):
        """
        :return int:
        """
        return self._time_spent_in_sec
