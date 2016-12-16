#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
#import os
#import httplib
#import urllib
import urllib2
#import time
from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding('utf8')

require_count = 500
require_level = 8.9

def curl(url):
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(request, timeout=5)
		return response.read()
	except urllib2.URLError,e:
		return str(e)

def get_books(tag):
	books = []
	idx = 0
	while True:
	        url = "https://book.douban.com/tag/%s?start=%d&type=S" % (urllib2.quote(tag.encode("utf-8")),idx)
                cnt = 0
		page = curl(url)
		start = page.find("<ul class=\"subject-list")
		end = page.find("<div class=\"paginator")
                if -1==start or -1==end:
                    break
		soup = BeautifulSoup(page[start:end],'lxml')
		modlist = soup.findAll("li",{"class":"subject-item"})
		for mod in modlist:
                    try:
                        book = {}
                        aa = mod.findAll("a")
                        book['title'] = aa[1].get("title")
                        book['href'] = aa[0].get("href")
                        book['score'] = mod.find("div",{"class":"star clearfix"}).find("span",{"class":"rating_nums"}).string
                        book['author'] = mod.find("div",{"class":"pub"}).string.partition("/")[0].strip()
                        if float(book['score'])>require_level:
		            books.append(book)
                            cnt += 1
                    except:
                        pass 
                print url+ " \t%d"%cnt
		idx+=20
                if idx>require_count or cnt==0:
                    break
	return books

def show_result(member):
        print "----"*16
	for book in member:
		print "%s\t%s\t%s(%s)" % (book['score'], book['href'], book['title'], book['author'])


########################################################################################
if __name__=='__main__':
    assert len(sys.argv)>1
    if len(sys.argv)==3:
        require_level = float(sys.argv[2])
    show_result(get_books(sys.argv[1].encode("utf-8")))
