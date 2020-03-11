# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.jira_server.beans.AbstractJiraIssue import AbstractJiraIssue


class JiraAutomationRequest(AbstractJiraIssue):
    """Groups JIRA epics"""

    def __init__(self, issue):
        """
        :param jira.resources.Issue issue:
        """
        super().__init__(issue)

    def build_csv_data(self):
        """
        :return list[dict]:
        """
        return [super().build_csv_data()]

    @staticmethod
    def get_expected_types():
        """
        :return list:
        """
        return ['Automation Request']
