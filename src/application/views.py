"""
views.py

URL route handlers

Note that any handler params must match the URL route params.
"""


import logging
import re

from google.appengine.api import users, urlfetch, memcache
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import render_template, flash, url_for, redirect

from bs4 import BeautifulSoup

from decorators import login_required, admin_required


def home():
    return redirect(url_for('front'))


def front():
    """Front page"""
    hnfront = memcache.get('hn:front')
    if hnfront is None:
        r = urlfetch.fetch(url='http://news.ycombinator.com/')
        hnfront = r.content
        memcache.add('hn:front', r.content, 3600)

    hnList = parse(hnfront)

    return render_template('slides.html', hnList=hnList)

def newest():
    """Newest"""
    hnnewest = memcache.get('hn:newest')
    if hnnewest is None:
        r = urlfetch.fetch(url='http://news.ycombinator.com/newest')
        hnnewest = r.content
        memcache.add('hn:newest', r.content, 300)

    hnList = parse(hnnewest)

    return render_template('slides.html', hnList=hnList)

def warmup():
    """App Engine warmup handler
    See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests

    """
    return ''


def parse(html):
    soup = BeautifulSoup(html)
    soupData = soup('td', {'class': ['title', 'subtext']})

    hnList = []
    nodeData = {}

    for node in soupData:
        if ''.join(node['class']) == 'title' and node.a:
            if node.a['href'] == 'news2' and node.a.string == 'More':
                continue
            else:
                nodeData['link'] = node.a['href']
                if nodeData['link'].startswith('item?id='):
                    nodeData['link'] = 'http://news.ycombinator.com/' + nodeData['link']

                nodeData['title'] = node.a.string
        elif ''.join(node['class']) == 'subtext':
            if node.find('span', {'id' : re.compile('^score.*')}):
                nodeData['score'] = node.find('span', {'id' : re.compile('^score.*')}).string

            if node.find('a', {'href' : re.compile('^user.*')}):
                nodeData['user'] = node.find('a', {'href' : re.compile('^user.*')}).string

            if node.find('a', {'href' : re.compile('^item.*')}):
                nodeData['itemId'] = node.find('a', {'href' : re.compile('^item.*')})["href"]
                if nodeData['itemId'].startswith('item?id='):
                    nodeData['itemId'] = 'http://news.ycombinator.com/' + nodeData['itemId']

            if node.find('a', {'href' : re.compile('^item.*')}):
                nodeData['comments'] = node.find('a', {'href' : re.compile('^item.*')}).string

            hnList.append(nodeData)
            nodeData = {}

    return hnList
