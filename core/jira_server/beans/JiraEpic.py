# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.jira_server.beans.AbstractJiraIssue import AbstractJiraIssue


class JiraEpic(AbstractJiraIssue):
    """Groups JIRA tasks"""

    # IMPORTANT: It must not have any space after the comma
    fields = (
        AbstractJiraIssue.fields + ','
        'issuelinks,'

        # This is the "Epic Name" field
        'customfield_13011')

    expected_types = ['Epic']

    def __init__(self, issue):
        """
        :param jira.resources.Issue issue:
        """
        super().__init__(issue)
        self._name = issue.fields.customfield_13011
        self._automation_request_key = JiraEpic._extract_automation_request_key(issue)

    def build_csv_data(self):
        """
        :return list[dict]:
        """
        csv_data_entries = list()
        csv_data_entry = super().build_csv_data()
        csv_data_entry.update({
            'epic name'.title(): self._name,
            'automation request key'.title(): self._automation_request_key})

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
