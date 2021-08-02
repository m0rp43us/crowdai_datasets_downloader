import requests
from xml.etree import ElementTree

from anonfile import AnonFile

anon = AnonFile()

response = requests.get("https://s3.eu-central-1.wasabisys.com/aicrowd-public-datasets")

tree = ElementTree.fromstring(response.content)
###root = tree.getroot()
i = 0
for event in tree.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents'):
    file = requests.get("https://s3.eu-central-1.wasabisys.com/aicrowd-public-datasets/"+event[0].text, stream=False,timeout=5)
    print(file.content)
    print(file.headers.get('content-type').split(';')[0].split('/')[1])
    print(event[0].text)
    #upload = anon.upload('/home/guest/jims_paperwork.doc', progressbar=True)
    #print(upload.url.geturl())
    if i == 10:
        break
    i+=1

