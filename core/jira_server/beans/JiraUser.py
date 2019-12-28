# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class JiraUser:
    """JIRA server user"""

    def __init__(self, user):
        """
        :param jira.resources.User user:
        """
        self._name = user.displayName
        self._email = user.emailAddress
        self._core_id = user.name
        self._is_active = user.active

    @property
    def name(self):
        """
        :return str:
        """
        return self._name

    @property
    def email(self):
        """
        :return str:
        """
        return self._email

    @property
    def core_id(self):
        """
        :return str:
        """
        return self._core_id

    @property
    def is_active(self):
        """
        :return bool:
        """
        return self._is_active
