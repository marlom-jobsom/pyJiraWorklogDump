# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.jira_server.beans.AbstractJiraIssue import AbstractJiraIssue


class JiraEpic(AbstractJiraIssue):
    """Groups JIRA tasks"""

    def __init__(self, issue):
        """
        :param jira.resources.Issue issue:
        """
        super().__init__(issue)
        self._name = issue.fields.customfield_13011
        self._automation_request_key = JiraEpic._extract_automation_request_key(issue)

    @staticmethod
    def get_jira_fields():
        """
        :return list:
        """
        common_fields = super(JiraEpic, JiraEpic).get_jira_fields()
        epic_fields = [
            'issuelinks',

            # This is the "Epic Name" field
            'customfield_13011']

        return common_fields + epic_fields

    @staticmethod
    def get_expected_types():
        """
        :return list:
        """
        raise ['Epic']

    def build_csv_data(self):
        """
        :return list[dict]:
        """
        csv_data_entries = list()
        csv_data_entry = super().build_csv_data()
        csv_data_entry.update({
            'epic name': self._name,
            'automation request key': self._automation_request_key})

        csv_data_entries.append(csv_data_entry)

        return csv_data_entries

    @property
    def name(self):
        """
        :return str:
        """
        return self._name

    @property
    def automation_request_key(self):
        """
        :return str:
        """
        return self._automation_request_key

    @staticmethod
    def _extract_automation_request_key(issue):
        """
        :param jira.resources.Issue issue:
        :return str:
        """
        issue_links = issue.fields.issuelinks

        for issue_link in issue_links:
            if issue_link.type.outward == 'is a requirement of':
                if issue_link.outwardIssue.fields.issuetype.name == 'Automation Request':
                    return issue_link.outwardIssue.key
