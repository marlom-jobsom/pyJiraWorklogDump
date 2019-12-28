# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import moment


class JiraVersion:
    """Groups JIRA tasks for a given automation request version"""

    def __init__(self, version):
        """
        :param jira.resources.Version version:
        """
        self._name = version.name
        self._was_released = version.released
        self._description = JiraVersion._extract_description(version)
        self._release_date = JiraVersion._extract_release_date(version)

    @property
    def name(self):
        """
        :return str:
        """
        return self._name

    @property
    def was_released(self):
        """
        :return bool:
        """
        return self._was_released

    @property
    def description(self):
        """
        :return str:
        """
        return self._description

    @property
    def release_date(self):
        """
        :return datetime.datetime:
        """
        return self._release_date

    @staticmethod
    def _extract_description(version):
        """
        :param jira.resources.Version version:
        :return str:
        """
        if version.__dict__.get('description'):
            return version.description

    @staticmethod
    def _extract_release_date(version):
        """
        :param jira.resources.Version version:
        :return datetime.datetime:
        """
        if version.__dict__.get('releaseDate'):
            return moment.jira_version_date_to_datetime(version.releaseDate)
