# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import codecs
import csv
import os

from utils import logger
from utils import moment
from utils import path


class Reporter:
    """Report JIRA data"""

    @staticmethod
    def csv(jira_issues):
        """
        :param list[AbstractJiraIssue] jira_issues:
        """
        file_path = Reporter._get_file_path(jira_issues[0])
        header = Reporter._get_header(jira_issues[0])
        logger.info('Saving #{} {}'.format(len(jira_issues), str(jira_issues[0])))

        with codecs.open(filename=file_path, mode='w', encoding='utf-8') as _file:
            csv_writer = csv.DictWriter(_file, delimiter=',', fieldnames=header)
            csv_writer.writeheader()

            for jira_issue in jira_issues:
                csv_data = jira_issue.build_csv_data()

                for entry in csv_data:
                    csv_writer.writerow(entry)

    @staticmethod
    def _get_file_path(jira_issue):
        """
        :param AbstractJiraIssue jira_issue:
        :return str:
        """
        file_name = '{}.csv'.format(str(jira_issue).lower())
        folder_path = path.build_today_dump_folder_path(moment.get_now())
        file_path = os.path.join(folder_path, file_name)

        logger.info('{} file path: {}'.format(str(jira_issue), file_path))
        return file_path

    @staticmethod
    def _get_header(jira_issue):
        """
        :param AbstractJiraIssue jira_issue:
        :return dict_keys:
        """
        csv_data = jira_issue.build_csv_data()[0]
        header = csv_data.keys()

        logger.info('{} CSV header: {}'.format(str(jira_issue), list(header)))
        return header
