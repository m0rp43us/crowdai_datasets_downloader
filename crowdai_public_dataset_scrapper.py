from typing import Dict
import requests
import xml.etree.ElementTree as ET
import glob
from anonfile import AnonFile
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.firefox import GeckoDriverManager
import selenium.webdriver.support.ui as ui
import http.client
from collections import defaultdict
import os
import time


def patch_http_response_read(func):
    def inner(*args):
        try:
            return func(*args)
        except http.client.IncompleteRead as e:
            return e.partial
    return inner

http.client.HTTPResponse.read = patch_http_response_read(http.client.HTTPResponse.read)

download_url = "https://s3.eu-central-1.wasabisys.com/aicrowd-public-datasets/"
response = requests.get(download_url)

anon = AnonFile("your api key")
with open('aicrowd.xml', 'wb') as f:
        f.write(response.content)


tree = ET.parse('aicrowd.xml')

root = tree.getroot()

print(root)

link_list = []
data = defaultdict(list)
for child in root:
    key = 0
    #print(child.tag,child.attrib)
    children = child.getchildren()
    list_data = []
    for i in range(len(children)-1):
        if i==2:
            key=str(children[i].text)[1:len(children[i].text)-1]
        elif i==3:
            list_data.append(int(children[i].text)/(1024.0*1024))
        else:
            list_data.append(children[i].text)
        
    data[key]=list_data


dir = '/media/morpheus/Nouveau nom/ai_crowd_download/'


WINDOW_SIZE = "1920,1080"


firefox_options = webdriver.FirefoxOptions()
firefox_options.add_argument('--no-sandbox')
firefox_options.add_argument("--disable-extensions")
firefox_options.add_argument("--incognito")
firefox_options.add_argument("--headless")
firefox_options.add_argument("--window-size=%s" % WINDOW_SIZE)

#webdriver config & settings
fp = webdriver.FirefoxProfile("/home/morpheus/.mozilla/firefox/")
fp.set_preference("browser.download.panel.shown", False)
fp.set_preference("browser.helperApps.neverAsk.openFile", 'application/csv')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/csv')
fp.set_preference("browser.helperApps.neverAsk.openFile", 'text/csv')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'text/csv')
fp.set_preference("browser.helperApps.neverAsk.openFile", 'application/vnd.ms-excel')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/vnd.ms-excel')
fp.set_preference("browser.helperApps.neverAsk.openFile", 'application/octet-stream')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", 'application/octet-stream')

fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.folderList",2)
fp.set_preference("browser.download.dir", dir)
fp.set_preference("profile.default_content_setting_values.automatic_downloads",1)


#for key in data:
#    if len(data[key])!=0:
#        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install(),firefox_profile=fp)
#        browser.maximize_window()
#        print(key, '->', data[key][0])
#        browser.get(download_url+data[key][0])
#        time.sleep(3)   
#        browser.refresh()
#        print(glob.glob(dir+"*"))
#        file = glob.glob(dir+"*")[0]
#        upload = anon.upload(file, progressbar=True)
#        print(upload.url.geturl())
#        data[key].append(upload.url.geturl())
#        for f in os.listdir(dir):
#            os.remove(os.path.join(dir, f))

#json_object = json.dumps(data)

with open(dir+'data.json', 'w') as outfile:
    json.dump(data, outfile)

print(downloads)
