# !/usr/bin/env python3
# -*- coding: utf-8 -*-


class JiraUser:
    """JIRA server user"""

    def init(self, user):
        """
        :param jira.resources.User user:
        """
        self._name = user.displayName if user else 'Unassigned'
        self._email = user.emailAddress if user else 'Unassigned'
        self._core_id = user.name if user else 'Unassigned'
        self._is_active = bool(user)

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
