import cfg
from bs4 import BeautifulSoup
import requests
import re
import datetime
from pymongo import MongoClient
from requests import exceptions
from requests.compat import urljoin,urlparse
import time
import uuid
import mimetypes
import os

def writetofile(fn,r):
    """
        # Function To write response content to file
    """
    try:
        path = os.path.join(os.path.curdir,'/crawl_res/')
        os.mkdir(path)
    except Exception:
        pass
    if fn=="":
        exttype = r.headers['content-type']
        ext = mimetypes.guess_extension(exttype)
        if ext is None:
            ext=".html"
        fn = str(uuid.uuid4())+ext
    fp = open(path+fn,'wb')
    if fp:
        try:
            fp.write(r.content)
        except:
            print("cannot write to file")
            pass
    fp.close()

def extractPage(r,src,table):
    data = str(r.content)
    soup = BeautifulSoup(data,"html.parser")
    links = {link.attrs.get('href') for link in soup.findAll('a', href=True)}
    count = 0
    for link in links:
        if link=="":
            continue
        if link[0]=='//':
            continue
        elif link[0]=='/':
            link = urljoin(src,link)
        if not (urlparse(link).scheme and urlparse(link).netloc):
            continue
        if table.find({"Link":link}).count() > 0: #check if link already exists
            continue
        obj = {
            "Link":link,
            "SourceLink":src,
            "IsCrawled":False,
            "LastCrawlDate":None,
            "ResponseStatus":None,
            "Contenttype":None,
            "ContentLength": None,
            "Filepath":"",
            "CreatedDate":datetime.datetime.utcnow()
        }
        table.insert_one(obj)
        count += 1
    return count
        
