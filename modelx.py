#!/usr/bin/python
import os
import sys
import time
import random
import urllib2
#import string
from bs4 import BeautifulSoup

URL=[]
PRE=""

def curl(url):
    request = urllib2.Request(url)
    request.add_header('Referer','http://www.modelx.org/') 
    request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 
    try:
        response = urllib2.urlopen(request, timeout=10)
        return response.read()
    except urllib2.URLError,e:
        return str(e)

def download(url,directory):
    if  os.path.exists(directory)==False:
        os.mkdir(directory)
    jpgname = url[url.rfind("/")+1:len(url)]
    filename =  directory + "/"
    if jpgname[0].isdigit() == True:
        filename += PRE
    filename += jpgname
    
    req = urllib2.Request(url) 
    req.add_header('Referer','http://www.modelx.org/') 
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.2; rv:16.0) Gecko/20100101 Firefox/16.0') 

    try:
        f = urllib2.urlopen(req, timeout=10) 
        data = f.read()
        with open(filename, "wb") as code:
            code.write(data)
        return True
    except:
        return False

def get_index(url):
    print url
    global URL
    global PRE
    del URL[:]
    start = url.rfind("-")
    end = url[start:].find("/")
    PRE = url[start+1:start+end]
    if False == PRE.isdigit():
        PRE = ""
    page = curl(url)
    start = page.find("<div id=\'gallery-2")
    end = page[start:].find("<div class=\"clear")
    if start==-1 or end==-1:
        print "Get Index Fail!"
        return
    soup = BeautifulSoup(page[start:start+end],'lxml')
    model = soup.find("dd").string.replace("AsiaNude4u","").replace(" ","").strip().replace("88Squaremodels","").replace("Gallery","")
    piclist = soup.findAll("dt",{"class":"gallery-icon portrait"})
    for pic in piclist:
        url = pic.find("a").get("href")
        URL.append(url)
    return model


def get_dir():
    PREFIX="http://www.modelx.org/wp-content/uploads/2015/11/20/"
    for no in range(50,999):
        sno = str(no)
        sno = "0"*(3-len(sno))+sno
        url = PREFIX+sno+"16.jpg"
        print url
        if False == download(url, "LawHoyan"):
            if False == download(url, "LawHoyan"):
                print " False"

def get_all(index):
    model = get_index(index)
    model = str(model)
    assert len(model)>0
    print model
    print "pics: %d" % len(URL)
    no = 0
    for u in URL:
        no+=1
        log = str(no)+" "+u
        if False==download(u,model):
            if False==download(u,model):
                log += "  False"
        print log



if __name__=="__main__":
    #url = "http://www.modelx.org/asian-exclusive/asianude4u/asianude4u-law-ho-yan/"
    assert len(sys.argv)>1
    get_all(sys.argv[1])


