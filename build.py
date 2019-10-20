#!/usr/bin/env python
# coding: utf-8
# pylint: disable=C0111
# pylint: disable=C0103
# pylint: disable=C0330

from __future__ import print_function
from datetime import datetime
import os
import sys
import traceback
import re
import csv
import json

VERSION = '1.0'
SRC_CSV_FILE = "app-ids.csv"
SRC_MARKDOWN_FILE = "template.README.md"
SRC_MARKDOWN_PLACEHOLDER = '%%APPS%%'
SRC_MARKDOWN_TIMESTAMP = '%%BUILD_TIMESTAMP%%'
DIST_README = 'README.md'
DIST_JSON = 'google-app-ids.json'
APP_LINK_PLACEHOLDER = "[{0}](https://play.google.com/work/apps/details?id={1})"

def csv_parse(csv_path):
    if not os.path.exists(csv_path):
        raise Exception('{} source file could not be found!'.format(csv_path))

    apps = []
    with open(csv_path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            apps.append([row[0], row[1] == 'true'])
    return apps[1:]

def dist_json(apps, output_path):
    json_data = []
    for app in apps:
        obj = {
            'name': 'DUMMY',
            'package_name': app[0],
            'privileged': app[1]
            }
        json_data.append(obj)

    with open(output_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=2, ensure_ascii=False)

def dist_readme(apps, template_path, output_path):
    with open(template_path, 'r') as template:
        template_contents = template.read()

    app_contents = ''
    for app in apps:
        line = '| ... | {0} |  {1} | {2}'.format(app[0], 
            APP_LINK_PLACEHOLDER.format('DUMMY', app[0]), 
            'Yes' if app[1] == True else 'No' )
        line += "\n"
        app_contents += line

    with open(output_path, 'w') as output:
        today = datetime.today()
        template_contents = template_contents.replace(SRC_MARKDOWN_TIMESTAMP,
            today.strftime('%b %d, %Y at %H:%M:%S'))
        template_contents = template_contents.replace(SRC_MARKDOWN_PLACEHOLDER, 
            app_contents)
        output.write(template_contents)

#############################################################################
# Main
if __name__ == "__main__":
    try:
        cur_path = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(cur_path, 'src', SRC_CSV_FILE)

        apps = csv_parse(csv_path)
        dist_readme(apps, os.path.join(cur_path, 'src', SRC_MARKDOWN_FILE), 
            os.path.join(cur_path, DIST_README))
        dist_json(apps, os.path.join(cur_path, 'dist', DIST_JSON))

    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print ("[ERROR] {0}".format(e))