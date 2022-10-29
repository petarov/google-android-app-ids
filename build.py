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
from operator import itemgetter
import requests
from bs4 import BeautifulSoup
import multiprocessing
from multiprocessing.pool import ThreadPool

SRC_CSV_FILE = "app-ids.csv"
SRC_MARKDOWN_FILE = "template.README.md"
SRC_APPS_PLACEHOLDER = '%%APPS%%'
SRC_APPSCOUNT_PLACEHOLDER = '%%APPS_COUNT%%'
SRC_TIMESTAMP_PLACEHOLDER = '%%BUILD_TIMESTAMP%%'
SRC_VERSION_PLACEHOLDER = '%%VERSION%%'
DIST_README = 'README.md'
DIST_JSON = 'google-app-ids.json'
DIST_CSV = 'google-app-ids.csv'
APP_LINK_PLACEHOLDER = "[{0}](https://play.google.com/store/apps/details?id={1})"

def csv_parse(csv_path):
    print ('Parsing apps from CSV file...')
    if not os.path.exists(csv_path):
        raise Exception('{} source file could not be found!'.format(csv_path))

    apps = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            apps.append([row[0]])
    return apps[1:]

def apps_preprocess(apps):
    apps_new = []

    def app_download_details(app):
        print ('|--Downloading ', app[0])
        html_contents = requests.get(
            'https://play.google.com/store/apps/details?id={0}'.format(app[0]))
        soup = BeautifulSoup(html_contents.text, 'html.parser')
        logo_img = soup.find('img' ,attrs={'itemprop':'image',
            'alt': 'Icon image'})
        logo_src = logo_img['src'] if logo_img else ''
        title = soup.find('h1' ,attrs={'itemprop':'name'})
        title_text = title.text if title else 'NOT FOUND'
        cat = soup.find('a' ,attrs={'itemprop':'genre'})
        cat_text = cat.text if cat else 'NOT FOUND'
        return [app[0], title_text, logo_src, cat_text]

    try:
        cpus = max(min(multiprocessing.cpu_count(), 8), 2)
    except NotImplementedError:
        cpus = 2    # default
    
    print ("| Downloading {0} app details using {1} parallel threads ...".format(
        len(apps), cpus))

    pool = ThreadPool(processes=cpus)
    for app in apps:
        pool.apply_async(app_download_details, args=(app,), 
            callback=lambda x : apps_new.append(x) if x[2] != 'NOT FOUND' \
                else print ("|----> NOT FOUND: {}".format(x[0])))

    pool.close()
    pool.join()

    return sorted(apps_new, key=lambda x: x[2].lower())

def dist_json(apps, output_path):
    print ('Saving json file...')
    json_data = []
    for app in apps:
        obj = {
            'img_src': app[2],
            'package_name': app[0],
            'name': app[1],
            'genre': app[3]
            }
        json_data.append(obj)

    with open(output_path, 'w') as outfile:
        json.dump(json_data, outfile, indent=2, ensure_ascii=False)

def dist_csv(apps, output_path):
    print ('Saving csv file...')
    with open(output_path, 'w') as outfile:
        outfile.write("Icon,Package,Name,Genre\n")
        for app in apps:
            outfile.write("{0},{1},\"{2}\",\"{3}\"\n".format(
                app[2], # logo
                app[0], # package
                app[1], # name
                app[3]  # category
            ))

def dist_readme(apps, template_path, package_path, output_path):
    print ('Saving Markdown file...')
    with open(template_path, 'r') as template:
        template_contents = template.read()

    app_contents = ''
    for app in apps:
        logo_src = app[2].replace('=w240', '=w80') if len(app) > 3 else ''
        line = '| ![App Logo]({0}) | {1} |  {2} | {3}'.format(logo_src, app[0], 
            APP_LINK_PLACEHOLDER.format(app[1], app[0]), 
            app[3])
        line += "\n"
        app_contents += line

    with open(package_path) as json_file:
        package = json.load(json_file)

    with open(output_path, 'w') as output:
        today = datetime.today()
        template_contents = template_contents.replace(SRC_VERSION_PLACEHOLDER, 
            package['version'])
        template_contents = template_contents.replace(SRC_TIMESTAMP_PLACEHOLDER,
            today.strftime('%b %d, %Y at %H:%M:%S'))
        template_contents = template_contents.replace(SRC_APPS_PLACEHOLDER, 
            app_contents)
        template_contents = template_contents.replace(SRC_APPSCOUNT_PLACEHOLDER, 
            str(len(apps)))
        output.write(template_contents)

#############################################################################
# Main
if __name__ == "__main__":
    try:
        cur_path = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(cur_path, 'src', SRC_CSV_FILE)

        apps = apps_preprocess(csv_parse(csv_path))
        dist_readme(apps, os.path.join(cur_path, 'src', SRC_MARKDOWN_FILE), 
            os.path.join(cur_path, 'package.json'),
            os.path.join(cur_path, DIST_README))
        dist_json(apps, os.path.join(cur_path, 'dist', DIST_JSON))
        dist_csv(apps, os.path.join(cur_path, 'dist', DIST_CSV))

        print ('Done.')
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        print ("[ERROR] {0}".format(e))