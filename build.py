#!/usr/bin/env python3
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
import requests
from bs4 import BeautifulSoup
import multiprocessing
from multiprocessing.pool import ThreadPool

VERSION = '1.0'
SRC_CSV_FILE = "app-ids.csv"
SRC_MARKDOWN_FILE = "template.README.md"
SRC_MARKDOWN_PLACEHOLDER = '%%APPS%%'
SRC_MARKDOWN_TIMESTAMP = '%%BUILD_TIMESTAMP%%'
DIST_README = 'README.md'
DIST_JSON = 'google-app-ids.json'
APP_LINK_PLACEHOLDER = "[{0}](https://play.google.com/work/apps/details?id={1})"

def csv_parse(csv_path):
    print ('Parsing apps from CSV file...')
    if not os.path.exists(csv_path):
        raise Exception('{} source file could not be found!'.format(csv_path))

    apps = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            apps.append([row[0], row[1] == 'true'])
    return apps[1:]

def apps_preprocess(apps):
    apps_new = []

    def app_download_details(app):
        print ('|--Downloading ', app[0])
        html_contents = requests.get(
            'https://play.google.com/work/apps/details?id={0}'.format(app[0]))
        soup = BeautifulSoup(html_contents.text, 'html.parser')
        logo_img = soup.find('img' ,attrs={'itemprop':'image',
            'alt': 'Cover art'})
        title = soup.find('h1' ,attrs={'itemprop':'name'})
        title_text = title.text if title else ''
        logo_src = logo_img['src'] if logo_img else ''        
        return [app[0], app[1], title_text, logo_src]

    try:
        cpus = min(multiprocessing.cpu_count(), 8)
    except NotImplementedError:
        cpus = 2    # default
    
    print ("| Downloading {0} app details using {1} parallel threads ...".format(
        len(apps), cpus))

    pool = ThreadPool(processes=cpus)
    for app in apps:
        pool.apply_async(app_download_details, args=(app,), 
            callback=lambda new_app : apps_new.append(new_app))

    pool.close()
    pool.join()

    return apps_new

def dist_json(apps, output_path):
    print ('Writing json file...')
    json_data = []
    for app in apps:
        obj = {
            'img_src': app[3] if len(app) > 3 else '',
            'name': app[2] if len(app) > 2 else '',
            'package_name': app[0],
            'privileged': app[1]
            }
        json_data.append(obj)

    with open(output_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=2, ensure_ascii=False)

def dist_readme(apps, template_path, output_path):
    print ('Writing Markdown file...')
    with open(template_path, 'r') as template:
        template_contents = template.read()

    app_contents = ''
    for app in apps:
        name = app[2] if len(app) > 2 else ''
        logo_src = app[3].replace('=s180', '=s64') if len(app) > 3 else ''
        line = '| ![App Logo]({0}) | {1} |  {2} | {3}'.format(logo_src, app[0], 
            APP_LINK_PLACEHOLDER.format(name, app[0]), 
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

        apps = apps_preprocess(csv_parse(csv_path))
        dist_readme(apps, os.path.join(cur_path, 'src', SRC_MARKDOWN_FILE), 
            os.path.join(cur_path, DIST_README))
        dist_json(apps, os.path.join(cur_path, 'dist', DIST_JSON))

        print ('Done.')
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print ("[ERROR] {0}".format(e))