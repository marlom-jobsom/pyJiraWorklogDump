# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from jira import JIRA

from core.jira_server.beans.JiraAutomationRequest import JiraAutomationRequest
from core.jira_server.beans.JiraEpic import JiraEpic
from core.jira_server.beans.JiraTask import JiraTask
from utils import logger


class JiraServer:
    """Access layer to JIRA server"""

    def __init__(self, jira_url, jira_user, jira_password):
        """
        :param str jira_url:
        :param str jira_user:
        :param str jira_password:
        """
        self._instance = JIRA(
            server=jira_url,
            basic_auth=(jira_user, jira_password),
            validate=True,
            get_server_info=True)

    @staticmethod
    def _warn_jira_task_missing_epic_key(jira_tasks):
        """
        :param list[JiraTask] jira_tasks:
        """
        tasks_missing_epic_link = [task.key for task in jira_tasks if not task.epic_key]

        if tasks_missing_epic_link:
            logger.warning(' '.join(['JIRA Tasks missing Epic Links:', *tasks_missing_epic_link]))

    @staticmethod
    def _get_jira_fields_name_for_sql(jira_fields_names):
        """
        :param list[str] jira_fields_names:
        :return str:
        """
        # IMPORTANT: It must not have any space after the comma
        return ','.join(jira_fields_names)

    def search_jira_tasks_by_jql(self, jql):
        """
        :param str jql:
        :return list[JiraTask]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_tasks = list()
        issues = self._run_query(jql, JiraTask.get_jira_fields())
        logger.info('Retrieved #{} {}'.format(len(issues), JiraTask.__name__))

        for issue in issues:
            issue_worklogs = self._instance.worklogs(issue)
            jira_task = JiraTask(issue, issue_worklogs)
            jira_tasks.append(jira_task)

        return jira_tasks

    def search_jira_epics_by_jql(self, jql):
        """
        :param str jql:
        :return list[JiraEpic]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_epics = list()
        issues = self._run_query(jql, JiraEpic.get_jira_fields())
        logger.info('Retrieved #{} {}'.format(len(issues), JiraEpic.__name__))

        for issue in issues:
            jira_epic = JiraEpic(issue)
            jira_epics.append(jira_epic)

        return jira_epics

    def search_jira_automation_request_by_jql(self, jql):
        """
        :param str jql:
        :return list[JiraAutomationRequest]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_epics = list()
        issues = self._run_query(jql, JiraAutomationRequest.get_jira_fields())
        logger.info('Retrieved #{} {}'.format(len(issues), JiraAutomationRequest.__name__))

        for issue in issues:
            jira_epic = JiraAutomationRequest(issue)
            jira_epics.append(jira_epic)

        return jira_epics

    def search_jira_epics_by_jira_tasks(self, jira_tasks):
        """
        :param list[JiraTask] jira_tasks:
        :return list[JiraEpic]:
        """
        self._warn_jira_task_missing_epic_key(jira_tasks)

        tasks_epics_links = [task.epic_key for task in jira_tasks if task.epic_key]
        unique_jira_epics_keys = ','.join(set(tasks_epics_links))
        jql = 'issueKey in ({})'.format(unique_jira_epics_keys)

        return self.search_jira_epics_by_jql(jql)

    def search_jira_automation_request_by_jira_epics(self, jira_epics):
        """
        :param list[JiraEpic] jira_epics:
        :return list[JiraAutomationRequest]:
        """
        jira_epics_keys = ','.join(set([
            epic.automation_request_key for epic in jira_epics if epic.automation_request_key]))
        jql = 'issueKey in ({})'.format(jira_epics_keys)
        return self.search_jira_automation_request_by_jql(jql)

    def _run_query(self, jql, fields):
        """
        :param str jql:
        :param list[str] fields:
        :return list[jira.resources.Issue]:
        """
        return self._instance.search_issues(
            jql_str=jql,
            maxResults=False,
            fields=JiraServer._get_jira_fields_name_for_sql(fields))
