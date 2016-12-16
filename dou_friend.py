#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import httplib
import urllib
import urllib2
import json
import time
import socket
from bs4 import BeautifulSoup
reload(sys) 
sys.setdefaultencoding('utf8')

GET_START = 0
GET_LIMIT = 7000



def curl(url):
	request = urllib2.Request(url)
	try:
		response = urllib2.urlopen(request, timeout=5)
		return response.read()
	except urllib2.URLError,e:
		return str(e)

def search_user(name):
    args = {"q":name, "cat":1005,"start":0}
    url = "https://www.douban.com/j/search?" + urllib.urlencode(args)
    print url
    print curl(url)

def get_member(group):
	member = []
	index = GET_START
	ooo = "http://www.douban.com/group/%s/members?start=" % (group)
	while True:
		url = "%s%d" %(ooo,index)
                print url
		page = curl(url)
		start = page.find("div class=\"article\"")-1
		end = page.find("div class=\"aside\"")-1
		soup = BeautifulSoup(page[start:end],'lxml')
		modlist = soup.findAll("div",{"class":"mod"})
		for mod in modlist:
			mlist = mod.find("div",{"class":"member-list"})
			if mlist!=None:
				part = mlist.find("ul").findAll("li")
				if len(part)==0:
					break
				for people in part:
                                        p = {}
					p['name'] = people.find("div",{"class":"name"}).find("a").string
					p['link'] = people.find("div",{"class":"name"}).find("a").get("href")
                                        p['place'] = people.find("span",{"class":"pl"}).string
					member.append(p)
		index+=35
		if index>=GET_LIMIT:
			break
	return member

def show_members(member):
	for people in member:
		print "[%s]\t%s" % (people['name'], people['link'])

def intersection(list1,list2):
	inters = []
	for li in list1:
		if list2.count(li)>0:
			inters.append(li)
	return inters

def get_session(group,people):
	index = 0
	ooo = "http://www.douban.com/group/%s/discussion?start=" % (group)
	while True:
		url = "%s%d" %(ooo,index)
		page = curl(url) 
		start = page.find("table class=\"olt\"")-1
		end = page.find("div class=\"paginator\"")-40
		soup = BeautifulSoup(page[start:end])
		lines = soup.findAll("tr",{"class":""})
		for line in lines:
			tds = line.findAll("td")
			if len(tds)>1:
				if tds[1].find("a").string==people[0] or tds[1].find("a").get("href")==people[1]:
					print "%s  \t%s" % (tds[0].find("a").get("href"),tds[0].find("a").string)
		index+=25
		if index>=500:
			break

def get_sessions(group,peoples):
	index = 0
	ooo = "http://www.douban.com/group/%s/discussion?start=" % (group)
	while True:
		url = "%s%d" %(ooo,index)
		page = curl(url) 
		start = page.find("table class=\"olt\"")-1
		end = page.find("div class=\"paginator\"")-40
		soup = BeautifulSoup(page[start:end],'lxml')
		lines = soup.findAll("tr",{"class":""})
		for line in lines:
			tds = line.findAll("td")
			if len(tds)>1:
				peoplelink = tds[1].find("a").get("href")
				for people in peoples:
					if peoplelink==people[1]:
						print "%s  \t%s  \t%s" % (tds[0].find("a").get("href"), tds[0].find("a").string, people[0])
		index+=25
		if index>=3500:
			break


def get_all_post(people):
    pass
	#url = "http://www.douban.com/group/people/%s/joins" % (people)
	#page = curl(url)
	#url = "<div class="group-list group-cards">"
#####################################################################################################
if __name__=='__main__ii':
	members = get_member("intj")
	members2 = get_member("sz-love")
	target = intersection(members,members2)
	print len(target)
	show_members(target)
	print '----------------------------------'
	get_sessions("sz-love",target)

def find_people(group, name):
    allmember = get_member('sz-love')
    for people in allmember:
        if people['name']==name:
            print people['url']


if __name__=='__main__':
    search_user("–°∑…œË")
    #find_people('sz-love','–°∑…œË')
