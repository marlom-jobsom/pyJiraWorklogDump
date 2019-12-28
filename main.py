# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import init
from core.jira_server.JiraServer import JiraServer
from core.reporter.Reporter import Reporter


def main():
    """Entry-point"""
    args = init.get_args()
    jira = JiraServer(args.jira_url, args.jira_user, args.jira_password)

    jira_tasks = jira.search_jira_tasks_by_jql(args.jql)
    jira_epics = jira.search_jira_epics_by_jira_tasks(jira_tasks)
    jira_automation_request = jira.search_jira_automation_request_by_jira_epics(jira_epics)

    Reporter.csv(jira_tasks)
    Reporter.csv(jira_epics)
    Reporter.csv(jira_automation_request)


if __name__ == '__main__':
    main()
