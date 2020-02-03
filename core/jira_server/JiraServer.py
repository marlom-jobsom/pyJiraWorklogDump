# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from jira import JIRA

from core.jira_server.beans.JiraAutomationRequest import JiraAutomationRequest
from core.jira_server.beans.JiraEpic import JiraEpic
from core.jira_server.beans.JiraTask import JiraTask
from core.jira_server.exceptions.UnexpectedJiraIssueTypeException import UnexpectedJiraIssueTypeException
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

    def search_jira_issues_by_jql(self, jql):
        """
        :param str jql:
        :return list[AbstractJiraIssue]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_issues = list()
        issues = self._run_query(jql, JiraServer._build_all_unique_fields())
        logger.info('Retrieved #{} JIRA issues'.format(len(issues)))

        for issue in issues:
            issue_type_name = issue.fields.issuetype.name

            if issue_type_name in JiraAutomationRequest.expected_types:
                jira_issue = JiraAutomationRequest(issue)
            elif issue_type_name in JiraEpic.expected_types:
                jira_issue = JiraEpic(issue)
            elif issue_type_name in JiraTask.expected_types:
                issue_worklogs = self._instance.worklogs(issue)
                jira_issue = JiraTask(issue, issue_worklogs)
            else:
                raise UnexpectedJiraIssueTypeException(issue_type_name)

            jira_issues.append(jira_issue)

        return jira_issues

    def search_jira_issues_by_keys(self, keys):
        """
        :param list[str] keys:
        :return list[AbstractJiraIssue]:
        """
        jira_task_keys = ','.join(set(keys))
        jql = 'issueKey in ({})'.format(jira_task_keys)
        return self.search_jira_issues_by_jql(jql)

    def search_jira_tasks_by_jql(self, jql):
        """
        :param str jql:
        :return list[JiraTask]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_tasks = list()
        issues = self._run_query(jql, JiraTask.fields)
        logger.info('Retrieved #{} {}'.format(len(issues), JiraTask.__name__))

        for issue in issues:
            issue_worklogs = self._instance.worklogs(issue)
            jira_task = JiraTask(issue, issue_worklogs)
            jira_tasks.append(jira_task)

        return jira_tasks

    def search_jira_tasks_by_keys(self, keys):
        """
        :param list[str] keys:
        :return list[JiraTask]:
        """
        jira_task_keys = ','.join(set(keys))
        jql_str = 'issueKey in ({})'.format(jira_task_keys)
        return self.search_jira_tasks_by_jql(jql_str)

    def search_jira_epics_by_jql(self, jql):
        """
        :param str jql:
        :return list[JiraEpic]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_epics = list()
        issues = self._run_query(jql, JiraEpic.fields)
        logger.info('Retrieved #{} {}'.format(len(issues), JiraEpic.__name__))

        for issue in issues:
            jira_epic = JiraEpic(issue)
            jira_epics.append(jira_epic)

        return jira_epics

    def search_jira_epics_by_jira_tasks(self, jira_tasks):
        """
        :param list[JiraTask] jira_tasks:
        :return list[JiraEpic]:
        """
        tasks_epics_links = [task.epic_key for task in jira_tasks if task.epic_key]
        tasks_missing_epic_link = [task.key for task in jira_tasks if not task.epic_key]

        if tasks_missing_epic_link:
            logger.warning(' '.join(['JIRA Tasks missing Epic Links:', *tasks_missing_epic_link]))

        jira_epics_keys = ','.join(set(tasks_epics_links))
        jql = 'issueKey in ({})'.format(jira_epics_keys)
        return self.search_jira_epics_by_jql(jql)

    def search_jira_epics_by_keys(self, keys):
        """
        :param list[str] keys:
        :return list[JiraEpic]:
        """
        jira_epics_keys = ','.join(set(keys))
        jql = 'issueKey in ({})'.format(jira_epics_keys)
        return self.search_jira_epics_by_jql(jql)

    def search_jira_automation_request_by_jql(self, jql):
        """
        :param str jql:
        :return list[JiraAutomationRequest]:
        """
        logger.info('JQL: {}'.format(jql))
        jira_epics = list()
        issues = self._run_query(jql, JiraAutomationRequest.fields)
        logger.info('Retrieved #{} {}'.format(len(issues), JiraAutomationRequest.__name__))

        for issue in issues:
            jira_epic = JiraAutomationRequest(issue)
            jira_epics.append(jira_epic)

        return jira_epics

    def search_jira_automation_request_by_jira_epics(self, jira_epics):
        """
        :param list[JiraEpic] jira_epics:
        :return list[JiraAutomationRequest]:
        """
        jira_epics_keys = ','.join(set([
            epic.automation_request_key for epic in jira_epics if epic.automation_request_key]))
        jql = 'issueKey in ({})'.format(jira_epics_keys)
        return self.search_jira_automation_request_by_jql(jql)

    def search_jira_automation_request_by_keys(self, keys):
        """
        :param list[str] keys:
        :return list[JiraAutomationRequest]:
        """
        jira_epics_keys = ','.join(keys)
        jql = 'issueKey in ({})'.format(jira_epics_keys)
        return self.search_jira_automation_request_by_jql(jql)

    def _run_query(self, jql, fields):
        """
        :param str jql:
        :param str fields:
        :return list[jira.resources.Issue]:
        """
        return self._instance.search_issues(jql_str=jql, maxResults=False, fields=fields)

    @staticmethod
    def _build_all_unique_fields():
        """
        :return str:
        """
        fields = JiraAutomationRequest.fields.split(',')
        fields.extend(JiraEpic.fields.split(','))
        fields.extend(JiraTask.fields.split(','))
        return ','.join(list(set(fields)))
