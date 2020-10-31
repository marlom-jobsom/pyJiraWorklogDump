# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from core.jira_server.beans.AbstractJiraIssue import AbstractJiraIssue
from core.jira_server.beans.JiraVersion import JiraVersion
from core.jira_server.beans.JiraWorkLog import JiraWorkLog
from utils import moment


class JiraTask(AbstractJiraIssue):
    """Tracks teammate work-log"""

    def __init__(self, issue, worklogs):
        """
        :param jira.resources.Issue issue:
        :param list[jira.resources.Worklog]:
        """
        super().__init__(issue)
        self._resolution_type = JiraTask._extract_resolution_type(issue)
        self._resolution_date = JiraTask._extract_resolution_date(issue)

        self._affected_versions = JiraTask._extract_affected_versions(issue)
        self._fix_versions = JiraTask._extract_fix_versions(issue)

        self._time_estimated_in_sec = issue.fields.timeoriginalestimate
        self._worklogs = JiraTask._build_jira_worklogs(worklogs)

        self._epic_key = issue.fields.customfield_13010

    @staticmethod
    def get_jira_fields():
        """
        :return list:
        """
        common_fields = super(JiraTask, JiraTask).get_jira_fields()
        task_fields = [
            'resolution',
            'resolutiondate',
            'versions',
            'fixVersions',
            'timeoriginalestimate',

            # This is the "Epic Link" field
            'customfield_13010',

            # This is the "Sprint" field
            'customfield_11610']

        return common_fields + task_fields

    @staticmethod
    def get_expected_types():
        """
        :return list:
        """
        return ['Engineering Work', 'Defect', 'Task']

    def build_csv_data(self):
        """
        :return list:
        """
        csv_data_entries = list()
        csv_data_entry = super().build_csv_data()
        csv_data_entry.update({
            'resolution type': self._resolution_type,
            'resolution date': self._resolution_date,
            'affected versions': self._affected_versions[0].name if self._affected_versions else None,
            'fix versions': self._fix_versions[0].name if self._fix_versions else None,
            'time estimated in sec': self._time_estimated_in_sec,
            'epic key': self._epic_key,
            'logger': None,
            'log date': None,
            'time spent in sec': None})

        if self._worklogs:
            for worklog in self._worklogs:

                # Register a new entry for each work-log
                entry = csv_data_entry.copy()
                entry.update({
                    'logger': worklog.author_create.name,
                    'log date': worklog.started_at,
                    'time spent in sec': worklog.time_spent_in_sec})

                csv_data_entries.append(entry)
        else:
            csv_data_entries.append(csv_data_entry)

        return csv_data_entries

    @property
    def resolution_type(self):
        """
        :return str:
        """
        return self._resolution_type

    @property
    def resolution_date(self):
        """
        :return datetime.datetime:
        """
        return self._resolution_date

    @property
    def affected_versions(self):
        """
        :return list[JiraVersion]:
        """
        return self._affected_versions

    @property
    def fix_versions(self):
        """
        :return list[JiraVersion]:
        """
        return self._fix_versions

    @property
    def time_estimated_in_sec(self):
        """
        :return int:
        """
        return self._time_estimated_in_sec

    @property
    def worklogs(self):
        """
        :return list[JiraWorkLog]:
        """
        return self._worklogs

    @property
    def epic_key(self):
        """
        :return str:
        """
        return self._epic_key

    @staticmethod
    def _extract_resolution_type(issue):
        """
        :param jira.resources.Issue issue:
        :return str:
        """
        if issue.fields.__dict__.get('resolution'):
            return issue.fields.resolution.name

    @staticmethod
    def _extract_resolution_date(issue):
        """
        :param jira.resources.Issue issue:
        :return datatime.datetime:
        """

        if issue.fields.__dict__.get('resolutiondate'):
            return moment.jira_date_to_datetime(issue.fields.resolutiondate)

    @staticmethod
    def _extract_affected_versions(issue):
        """
        :param jira.resources.Issue issue:
        :return list[JiraVersion]:
        """
        affected_versions = list()

        for affected_version in issue.fields.versions:
            affected_versions.append(JiraVersion(affected_version))

        return affected_versions

    @staticmethod
    def _extract_fix_versions(issue):
        """
        :param jira.resources.Issue issue:
        :return list[JiraVersion]:
        """
        fix_versions = list()

        for fix_version in issue.fields.fixVersions:
            fix_versions.append(JiraVersion(fix_version))

        return fix_versions

    @staticmethod
    def _build_jira_worklogs(worklogs):
        """
        :param list[jira.resources.Worklog] worklogs:
        :return list[JiraWorkLog]:
        """
        jira_worklogs = list()

        for worklog in worklogs:
            jira_worklogs.append(JiraWorkLog(worklog))

        return jira_worklogs
