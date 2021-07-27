import requests
from xml.etree import ElementTree
response = requests.get("https://s3.eu-central-1.wasabisys.com/aicrowd-public-datasets")

tree = ElementTree.fromstring(response.content)
###root = tree.getroot()

for event in tree.findall('{http://s3.amazonaws.com/doc/2006-03-01/}Contents'):
    print(event[0].text)


