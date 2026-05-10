# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import io
import gc
import json
import os
import ssl
import sys
import time
from time import sleep
from datetime import datetime, timedelta
from urllib.parse import urlparse

import re, itertools

import pymysql.cursors
import sqlalchemy
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from croniter import croniter
from pyppeteer import launch
import ijson

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
import base64
import slugify                          ### !!!!!! pip install python-slugify !!!!!!!!!!!!!!!!!!
import random

ssl._create_default_https_context = ssl._create_unverified_context

import hashlib

import lxml
import lxml.etree as lxmlET
import lxml.html as lh

new_path = './cfg'
if new_path not in sys.path:
    sys.path.append(new_path)

from cfg.config import Config  # noqa: E402


# noinspection PyPackageRequirements
class ClassProcessHandlers:
    debug = False
    debuglevel = 0
    gHandle = 0
    gFeed = 0
    gCron = 0
    params = ''
    getstatement = ''
    actst = 0
    cfg = Config(debug=debug)
    cfgmain = Config(debug=debug)
    myConnection = ''
    myConnectionMain = ''
    email1 = 'noreply@ylperon.co.uk'
    email2 = 'techsupport@vacancygroup.com'

    processdatetime = datetime.now()

    start = datetime.now()
    emailvars = {}
    feedlocks = ""
    active = ""
    ats = ""
    feedtype = ""
    url = ""
    headers = ""
    jobtagfromfeed = ""
    seccallcols = ""
    tablename = ""
    tablenamekarchermapping = "karcher_webscraper_mapping"
    arctablename = ""
    updatetablename = ""
    deletetablename = ""
    inserttablename = ""
    tablejobtag = ""
    add2ref = ""
    refcol = ""
    limitjobposting = ""
    cleardata = ""
    jobfeedid = ""
    ustatid = ""
    sendemails = ""
    emailsto = ""
    emailssubject = ""
    emailsbody = ""
    lastrun = ""
    upload = ""
    conntype = ""
    server = ""
    port = ""
    path = ""
    reppath = ''
    feeduser = ""
    feedpass = ""
    database_check = ""
    rss_check = ""

    jobsindb = 0

    postcodelookuptablenamejoin = ""
    postcodeouttags = ""

    pageoutput = ""

    insvals = ''
    inscols = ''
    updcolsvals = ''
    colsfromfeed = ''
    error = ''

    insvalscp = ''
    inscolscp = ''
    updcolsvalscp = ''
    createtablecols = {}

    itemcount = 0

    jobsinfeed = 0

    updatedjobs = 0
    insertedjobs = 0
    deletedjobs = 0

    tagfound = False

    dtarr = []
    boolarr = []
    intarr = []

    shortcode = ''
    requestHeader = {}
    mainurl = ''
    mainurladd = ''

    skudetails = {}

    def __init__(self, actstat=4, debug=False, debuglevel=0, handle=0, feed=0, cron=0):
        self.debug = debug
        self.debuglevel = debuglevel
        self.actst = actstat
        self.gHandle = handle
        self.gFeed = feed
        self.gCron = cron
        print("Processing handlers:")
        print("Debug        -> " + str(self.debug))
        print("Debug level  -> " + str(self.debuglevel))
        print("Active       -> " + str(self.actst))
        print("Handle       -> " + str(self.gHandle))
        print("Feed         -> " + str(self.gFeed))
        print("Cron         -> " + str(self.gCron))
        self.myConnectionMain = self.cfg.myConnectionMain
        self.myConnection = self.cfg.myConnection

        # self.myConnection = pymysql.connect(
        #     host=self.cfg.hostname,
        #     user=self.cfg.username,
        #     password=self.cfg.password,
        #     db=self.cfg.database,
        #     charset='utf8mb4',
        #     cursorclass=pymysql.cursors.DictCursor
        # )
        # self.myConnectionMain = pymysql.connect(
        #     host=self.cfgmain.hostname,
        #     user=self.cfgmain.username,
        #     password=self.cfgmain.password,
        #     db=self.cfgmain.database,
        #     charset='utf8mb4',
        #     cursorclass=pymysql.cursors.DictCursor
        # )

        while self.gFeed == 1 or self.gCron == 1:
            time.sleep(1)

        if self.gHandle != 1:
            return

    def __del__(self):
        try:
            if self.myConnection.open:
                self.myConnection.close()
            gc.collect()
        except Exception as e:
            print(e)
            return
        self.closeMySqlPool()

    def closeMySqlPool(self):
        self.myConnectionMain.close()

    def resetFeedVars(self):
        self.start = datetime.now()
        self.emailvars = {}
        self.feedlocks = ""
        self.active = ""
        self.ats = ""
        self.feedtype = ""
        self.url = ""
        self.headers = ""
        self.jobtagfromfeed = ""
        self.seccallcols = ""
        self.tablename = ""
        self.arctablename = ""
        self.updatetablename = ""
        self.deletetablename = ""
        self.inserttablename = ""
        self.tablejobtag = ""
        self.add2ref = ""
        self.refcol = ""
        self.limitjobposting = ""
        self.cleardata = ""
        self.jobfeedid = ""
        self.ustatid = ""
        self.sendemails = ""
        self.emailsto = ""
        self.emailssubject = ""
        self.emailsbody = ""
        self.lastrun = ""
        if self.lastrun is None:
            self.lastrun = datetime.now()
        self.upload = ""
        self.conntype = ""
        self.server = ""
        self.port = ""
        self.path = ""
        self.reppath = ""
        self.feeduser = ""
        self.feedpass = ""
        self.database_check = ""
        self.rss_check = ""

        self.insvals = ''
        self.inscols = ''
        self.updcolsvals = ''
        self.colsfromfeed = ''
        self.createtablecols = {}
        self.error = ''

        self.insvalscp = ''
        self.inscolscp = ''
        self.updcolsvalscp = ''

        self.itemcount = 0

        self.jobsinfeed = 0

        self.dtarr.clear()
        self.boolarr.clear()
        self.intarr.clear()

        self.shortcode = ''
        self.requestHeader = {}
        self.mainurl = ''

        self.skudetails = {}
        self.skudetails.clear()

    def loadFeedVars(self, handler):
        self.start = datetime.now()
        self.emailvars = {}
        self.feedlocks = ("" if handler['locks'] is None else handler['locks'])
        self.active = ("" if handler['active'] is None else handler['active'])
        self.ats = ("" if handler['ats'] is None else handler['ats'])
        self.feedtype = ("" if handler['feedtype'] is None else handler['feedtype'])
        self.url = ("" if handler['jobfeedurl'] is None else handler['jobfeedurl'])
        self.headers = ("" if handler['headers'] is None else handler['headers'])
        self.jobtagfromfeed = ("" if handler['jobtagfromfeed'] is None else handler['jobtagfromfeed'])
        self.seccallcols = ("" if handler['seccallcols'] is None else handler['seccallcols'])
        self.tablename = ("" if handler['tablename'] is None else handler['tablename'])
        self.arctablename = ("" if handler['arctablename'] is None else handler['arctablename'])
        self.updatetablename = ("" if handler['updatetablename'] is None else handler['updatetablename'])
        self.deletetablename = ("" if handler['deletetablename'] is None else handler['deletetablename'])
        self.inserttablename = ("" if handler['inserttablename'] is None else handler['inserttablename'])
        self.tablejobtag = ("" if handler['tablejobtag'] is None else handler['tablejobtag'])
        self.add2ref = ("" if handler['add2ref'] is None else handler['add2ref'])
        self.refcol = ("" if handler['refcol'] is None else handler['refcol'])
        self.limitjobposting = ("" if handler['limitjobposting'] is None else handler['limitjobposting'])
        self.cleardata = ("" if handler['cleardata'] is None else handler['cleardata'])
        self.jobfeedid = ("" if handler['jobfeed_id'] is None else handler['jobfeed_id'])
        self.ustatid = ("" if handler['ustatid'] is None else handler['ustatid'])
        self.sendemails = ("" if handler['sendemails'] is None else handler['sendemails'])
        self.emailsto = ("" if handler['emailsto'] is None else handler['emailsto'])
        self.emailssubject = ("" if handler['emailssubject'] is None else handler['emailssubject'])
        self.emailsbody = ("" if handler['emailsbody'] is None else handler['emailsbody'])
        if '\r\n' in self.emailsbody:
            self.emailsbody = self.emailsbody.replace('\r\n', '\n')
        elif '\r' in self.emailsbody:
            self.emailsbody = self.emailsbody.replace('\r', '\n')
        handler['emailsbody'] = self.emailsbody

        self.lastrun = (datetime.now() if handler['lastrun'] is None else handler['lastrun'])
        self.upload = ("" if handler['upload'] is None else handler['upload'])
        self.conntype = ("" if handler['conntype'] is None else handler['conntype'])
        self.server = ("" if handler['server'] is None else handler['server'])
        self.port = ("" if handler['port'] is None else handler['port'])
        self.path = ("" if handler['path'] is None else handler['path'])
        self.reppath = ("" if handler['reppath'] is None else handler['reppath'])
        self.feeduser = ("" if handler['user'] is None else handler['user'])
        self.feedpass = ("" if handler['pass'] is None else handler['pass'])
        # self.database_check = "<span style=\"color:green;\">Successfull</span>"
        # self.rss_check = '<span style="color:green;">Successful run for handler ' + self.jobfeedid + '</span>'
        self.database_check = "<span style=\"color:red;\">Error DB Connection!</span>"
        self.rss_check = '<span style="color:red;">NOT successful run for handler ' + self.jobfeedid + '</span>'

        self.insvals = ''
        self.inscols = ''
        self.updcolsvals = ''
        self.colsfromfeed = ''
        self.createtablecols = {}
        self.error = ''

        self.insvalscp = ''
        self.inscolscp = ''
        self.updcolsvalscp = ''

        self.itemcount = 0

        self.jobsinfeed = 0

        self.dtarr.clear()
        self.boolarr.clear()
        self.intarr.clear()

        self.shortcode = ''
        self.requestHeader = {}
        self.mainurl = ''

        self.skudetails = {}
        self.skudetails.clear()

        if self.debug and self.debuglevel >= 0:
            print(self.start)
            print(self.feedlocks)
            print(self.active)
            print(self.ats)
            print(self.feedtype)
            print(self.url)
            print(self.headers)
            print(self.jobtagfromfeed)
            print(self.seccallcols)
            print(self.tablename)
            print(self.arctablename)
            print(self.updatetablename)
            print(self.deletetablename)
            print(self.inserttablename)
            print(self.tablejobtag)
            print(self.add2ref)
            print(self.refcol)
            print(self.limitjobposting)
            print(self.cleardata)
            print(self.jobfeedid)
            print(self.ustatid)
            print(self.sendemails)
            print(self.emailsto)
            print(self.emailssubject)
            print(self.emailsbody)
            print(self.upload)
            print(self.conntype)
            print(self.server)
            print(self.port)
            print(self.path)
            print(self.reppath)
            print(self.database_check)
            print(self.rss_check)

            print(self.insvals)
            print(self.inscols)
            print(self.updcolsvals)
            print(self.colsfromfeed)
            print(self.createtablecols)

            print(self.error)

            print(self.insvalscp)
            print(self.inscolscp)
            print(self.updcolsvalscp)

            print(self.itemcount)

            print(self.jobsinfeed)

            print(self.dtarr)
            print(self.boolarr)

            print(self.shortcode)
            print(self.requestHeader)
            print(self.mainurl)

            print(self.skudetails)

    def updJobsTable(self, handler):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            updateexistinfeed = "UPDATE `" + self.cfg.database + "`.`" + self.tablename \
                                + "` SET existinfeed = NULL " \
                                  "WHERE job_feed_id = '" \
                                + self.jobfeedid + "';"

            dbhandler.execute(updateexistinfeed)
        except pymysql.Error as e:
            print(e)
            print(updateexistinfeed)
            self.cfgmain.sendErrorEmail(handler, str(e) + " " + str(updateexistinfeed))
            return
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def getJobsInDB(self, handler):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            stmnt = "SELECT count(*) as cnt FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "';"

            try:
                if self.debug and self.debuglevel >= 0:
                    print(stmnt)
                dbhandler.execute(stmnt)
                for item in dbhandler.fetchall():
                    self.jobsindb = item["cnt"]
            except pymysql.Error as e:
                print(e)
                print(stmnt)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(stmnt))
                return
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def updHandlersTable(self, handler):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            updatehandlers = "UPDATE handlers SET status = 1, lastrun = now(), ustatid = ustatid + 1 WHERE jobfeed_id = '" + self.jobfeedid + "';"
            try:
                dbhandler.execute(updatehandlers)
            except pymysql.Error as e:
                print(e)
                print(updatehandlers)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(updatehandlers))
                return
        finally:
            handlersconn.close()  # returns the connection to the pool

    def getHeaders(self, headers, token=''):
        requestHeader = {}

        if headers is not None and headers != '':
            req = headers.split(",")
            if self.debug and self.debuglevel >= 9:
                print(req)
            for k in range(len(req)):
                rr = req[k].split(":")
                if self.debug and self.debuglevel >= 9:
                    print(rr)
                strrr = ''
                if len(rr) <= 2:
                    strrr = rr[1].replace("'", "").strip()
                    if token != '':
                        strrr = strrr + " " + token
                    requestHeader[rr[0].replace("'", "").strip()] = strrr
                else:
                    for kk in range(len(rr)-1):
                        strrr += rr[kk+1].replace("'", "").strip() + ":"
                        if self.debug and self.debuglevel >= 9:
                            print(strrr)
                    if token != '':
                        strrr = strrr + " " + token
                    strrr = strrr[:-1]
                    requestHeader[rr[0].replace("'", "").strip()] = strrr

            if self.debug and self.debuglevel >= 9:
                print(requestHeader)

        return requestHeader

    def getChromeOptions(self, randomset=''):
        useragentsdesktop = []

        useragentsdesktop.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0')
        useragentsdesktop.append('Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36')
        useragentsdesktop.append('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Safari/605.1.15')
        useragentsdesktop.append('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36>')
        useragentsdesktop.append('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1')

        # print(useragentsdesktop)

        useragentdesktopsize = []

        useragentdesktopsize.append({'1920':'1080'})
        useragentdesktopsize.append({'2560':'1440'})
        useragentdesktopsize.append({'3840':'2160'})
        useragentdesktopsize.append({'1600':'900'})
        useragentdesktopsize.append({'1536':'864'})
        useragentdesktopsize.append({'1440':'900'})
        useragentdesktopsize.append({'1366':'768'})
        useragentdesktopsize.append({'1360':'768'})
        useragentdesktopsize.append({'1280':'720'})

        # print(list(random.choice(useragentdesktopsize))[0])
        # print(list(random.choice(useragentdesktopsize).items())[0][1])

        # 1920×1080 (Full HD) – Most common for desktops, laptops, and large smartphones.
        # 2560×1440 (QHD) – Popular for high-end monitors and premium laptops.
        # 3840×2160 (4K UHD) – Found on 4K monitors, TVs, and ultra-premium laptops.
        # 1600×900 – Common in mid-range laptops and displays.
        # 1536×864 – Seen on newer mid-range laptops.
        # 1440×900 – Used in older widescreen monitors and budget laptops.
        # 1366×768 – Typical for budget laptops and older notebooks.
        # 1360×768 – Slight variant used in older TVs and budget displays.
        # 1280×720 (HD) – Standard for entry-level laptops and small monitors.

        useragentsmobile = []

        useragentsmobile.append('')

        # Android User Agents With the Client Hints support
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)')

        # Samsung Galaxy S25
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 15; SM-S931B Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 15; SM-S931U Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36')
        # Samsung Galaxy S24 Ultra
        useragentsmobile.append('Mozila/5.0 (Linux; Android 14; SM-S928B/DS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36')
        useragentsmobile.append('Mozila/5.0 (Linux; Android 14; SM-S928W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36')
        # Samsung Flip
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; SM-F9560 Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; SM-F956U) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36')
        # Samsung Galaxy Xcover7
        useragentsmobile.append('Mozilla/5.0 (Android 15; Mobile; SM-G556B/DS; rv:130.0) Gecko/130.0 Firefox/130.0')
        useragentsmobile.append('Mozilla/5.0 (Android 15; Mobile; SM-G556B; rv:130.0) Gecko/130.0 Firefox/130.0')
        # Samsung Galaxy S23
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36 Dalvik/2.1.0 (Linux; U; Android 13; SM-S911B Build/TP1A.220624.014)')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-S911U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy S22 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy S22 Ultra 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy S21 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy S21 Ultra 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy A53 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-A536U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy A51
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; SM-A515U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Samsung Galaxy S10
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')

        # Google Pixel 9 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro Build/AD1A.240418.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.54 Mobile Safari/537.36')
        # Google Pixel 9
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; Pixel 9 Build/AD1A.240411.003.A5; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.54 Mobile Safari/537.36')
        # Google Pixel 8 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 15; Pixel 8 Pro Build/AP4A.250105.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36')
        # Google Pixel 8
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 15; Pixel 8 Build/AP4A.250105.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36')
        # Google Pixel 7 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Google Pixel 7
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Google Pixel 6 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Google Pixel 6a
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Google Pixel 6
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')

        # Motorola Moto G (2025)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 15; moto g - 2025 Build/V1VK35.22-13-2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36')
        # Motorola Moto Edge 30 Neo
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 15; moto edge 30 neo Build/AP3A.241105.008)')
        # Motorola Moto g04
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; Moto g04) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36 Instabridge/22')
        # Motorola Moto G Stylus 5G (2024)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; moto g stylus 5G - 2024 Build/U2UB34.44-86; wv)')
        # Motorola Moto G Power 5G (2024)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; moto g power 5G - 2024 Build/U1UD34.16-62; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/123.0.6312.99 Mobile Safari/537.36')
        # Motorola Razr 50 Ultra
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; motorola razr 50 ultra Build/U3UX34.56-29-2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36')
        # Motorola Moto G Pure
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; moto g pure) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Motorola Moto G Stylus 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; moto g stylus 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36v')
        # Motorola Moto G Stylus 5G (2022)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; moto g stylus 5G (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Motorola Moto G 5G (2022)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; moto g 5G (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Motorola Moto G Power (2022)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Motorola Moto G Power (2021)
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 11; moto g power (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')

        # Redmi Note 13 4G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; 23129RAA4G Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36')
        # Redmi Turbo 4
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 15; 24129RT7CC Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36')
        # Huawei Pura 70 Ultra
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; HBP-LX9 Build/HUAWEIHBP-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36')
        # Huawei Nova 12 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; U; Android 12; zh-Hans-CN; ADA-AL00 Build/HUAWEIADA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Quark/6.11.2.531 Mobile Safari/537.36')
        # Huawei Nova Flip
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; PSD-AL00 Build/HUAWEIPSD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36')
        # Xiaomi 14 Ultra
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; 24030PN60G Build/UKQ1.231003.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.119 Mobile Safari/537.36')
        # Mix Flip
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 14; 2405CPX3DC Build/UKQ1.240116.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.193 Mobile Safari/537.36')
        # Redmi Note 9 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Redmi Note 8 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Huawei P30 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Huawei P30 lite
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 10; MAR-LX1A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Redmi Note 10 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Xiaomi Poco X3 Pro
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # Redmi Note 11 Pro 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')
        # OnePlus Nord N200 5G
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36')

        # Apple iPhone 16e
        useragentsmobile.append('Mozilla/5.0 (iPhone17,5; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 FireKeepers/1.7.0')
        # Apple iPhone 16 Pro
        useragentsmobile.append('Mozilla/5.0 (iPhone17,1; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Mohegan Sun/4.7.4')
        # Apple iPhone 16 Pro Max
        useragentsmobile.append('Mozilla/5.0 (iPhone17,2; CPU iPhone OS 18_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.5.2')
        # Apple iPhone 16
        useragentsmobile.append('Mozilla/5.0 (iPhone17,3; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 FireKeepers/1.6.1')
        # Apple iPhone 16 Plus
        useragentsmobile.append('Mozilla/5.0 (iPhone17,4; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.7.5')
        # Apple iPhone 15 Pro
        useragentsmobile.append('Mozilla/5.0 (iPhone16,2; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.7.5')
        # Apple iPhone 14
        useragentsmobile.append('Mozilla/5.0 (iPhone14,7; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Mohegan Sun/4.7.3')
        # Apple iPhone 13 Pro
        useragentsmobile.append('Mozilla/5.0 (iPhone14,2; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Mohegan Sun/4.7.4')
        # Apple iPhone SE (3rd generation)
        useragentsmobile.append('Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1')
        # iPhone 13 Pro Max
        useragentsmobile.append('Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1')
        # iPhone 12
        useragentsmobile.append('Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1')
        # iPhone 11
        useragentsmobile.append('Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1')
        # iPhone 11
        useragentsmobile.append('Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1')
        # Apple iPhone XR (Safari)
        useragentsmobile.append('Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1')
        # Apple iPhone XS (Chrome)
        useragentsmobile.append('Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1')
        # Apple iPhone XS Max (Firefox)
        useragentsmobile.append('Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15')
        # Apple iPhone X
        useragentsmobile.append('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1')
        # Apple iPhone 8
        useragentsmobile.append('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1')
        # Apple iPhone 8 Plus
        useragentsmobile.append('Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1')
        # Apple iPhone 7
        useragentsmobile.append('Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1')
        # Apple iPhone 7 Plus
        useragentsmobile.append('Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1')
        # Apple iPhone 6
        useragentsmobile.append('Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3')

        # Microsoft Lumia 650
        useragentsmobile.append('Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254')
        # Microsoft Lumia 550
        useragentsmobile.append('Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536')
        # Microsoft Lumia 950
        useragentsmobile.append('Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058')

        # Apple iPad Pro (11 5th Gen)
        useragentsmobile.append('Mozilla/5.0 (iPad16,3; CPU OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Tropicana_NJ/5.7.1')
        # Samsung Galaxy Tab Active5 5G
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 14; SM-X306B Build/UP1A.231005.007)')
        # Samsung Galaxy Tab S6 Lite
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 14; SM-P619N Build/UP1A.231005.007)')
        # Xiaomi Pad 7 Pro
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 15; 24091RPADG Build/AQ3A.240801.002)')
        # Amazon Fire HD 8 (2024, 12th Gen)
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 11; KFRASWI Build/RS8332.3115N)')
        # Samsung Galaxy Tab S6 Lite
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 14; SM-P619N Build/UP1A.231005.007)')
        # Lenovo Tab M10a 5G
        useragentsmobile.append('Dalvik/2.1.0 (Linux; U; Android 13; LET02 Build/TKQ1.230127.002)')
        # Apple iPad Air 11 (M3)
        useragentsmobile.append('Mozilla/5.0 (iPad15,3; CPU OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.7.5')
        # Samsung Galaxy Tab S8 Ultra
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36')
        # Lenovo Yoga Tab 11
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
        # Google Pixel C
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36')
        # Sony Xperia Z4 Tablet
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36')
        # Nvidia Shield Tablet K1
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36')
        # Samsung Galaxy Tab S3
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36')
        # Samsung Galaxy Tab A
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36')
        # Amazon Kindle Fire HDX 7
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36')
        # LG G Pad 7.0
        useragentsmobile.append('Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36')

        useragentstv = []

        # Amazon Fire TV Stick 4K Max (2nd Gen 2023)
        useragentstv.append('Mozilla/5.0 (Linux; Android 11; AFTKRT Build/RS8101.1849N; wv)PlexTV/10.0.0.4149')
        # Amazon Fire TV Cube (3rd Gen)
        useragentstv.append('Mozilla/5.0 (Linux; Android 9; AFTGAZL Build/PS7607.3166N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.125 Mobile Safari/537.36 FE v1.79.1')
        # Doom Pro 5G
        useragentstv.append('Mozilla/5.0 (Linux; Android 14; DOOM PRO 5G Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Safari/537.36 FE v1.87.3')
        # Apple TV (2022)
        useragentstv.append('AppleTV14,1/16.1')
        # Minix NEO X39
        useragentstv.append('Mozilla/5.0 (Linux; Android 7.1.2; NEO_X39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Safari/537.36')
        # Amazon Fire TV Stick 4K Max
        useragentstv.append('Mozilla/5.0 (Linux; Android 9; AFTKA) AppleWebKit/537.36 (KHTML, like Gecko) Silk/92.2.11 like Chrome/92.0.4515.159 Safari/537.36')
        # Amazon Fire TV Cube
        useragentstv.append('Mozilla/5.0 (Linux; Android 9; AFTR) AppleWebKit/537.36 (KHTML, like Gecko) Silk/98.6.10 like Chrome/98.0.4758.136 Safari/537.36')
        # Google ADT-2
        useragentstv.append('Dalvik/2.1.0 (Linux; U; Android 9; ADT-2 Build/PTT5.181126.002)')
        # Chromecast
        useragentstv.append('Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36')
        # Roku Ultra
        useragentstv.append('Roku4640X/DVP-7.70 (297.70E04154A)')
        # Minix NEO X5
        useragentstv.append('Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30')
        # Amazon AFTWMST22
        useragentstv.append('Mozilla/5.0 (Linux; Android 9; AFTWMST22 Build/PS7233; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36')
        # Amazon 4K Fire TV
        useragentstv.append('Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36')
        # Google Nexus Player
        useragentstv.append('Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)')
        # Apple TV 6th Gen 4K
        useragentstv.append('AppleTV11,1/11.1')
        # Apple TV 5th Gen 4K
        useragentstv.append('AppleTV6,2/11.1')
        # Apple TV 4th Gen
        useragentstv.append('AppleTV5,3/9.1.1')

        useragentmobilesize = []

        useragentmobilesize.append({'1440':'3200'})
        useragentmobilesize.append({'1320':'2868'})
        useragentmobilesize.append({'1284':'2778'})
        useragentmobilesize.append({'1206':'2622'})
        useragentmobilesize.append({'1080':'2424'})
        useragentmobilesize.append({'1080':'2400'})
        useragentmobilesize.append({'828':'1792'})
        useragentmobilesize.append({'414':'896'})
        useragentmobilesize.append({'412':'915'})
        useragentmobilesize.append({'390':'844'})
        useragentmobilesize.append({'375':'812'})
        useragentmobilesize.append({'360':'640'})
        useragentmobilesize.append({'320':'480'})

        useragentmobilesize.append({'1280':'800'})
        useragentmobilesize.append({'800':'1280'})
        useragentmobilesize.append({'768':'1024'})
        useragentmobilesize.append({'1024':'768'})

        # Mobile Resolutions
        # 1440×3200 – Premium Android phones like the Samsung Galaxy S series.
        # 1320×2868 – iPhone 16 Pro Max.
        # 1284×2778 – iPhone 14 Pro Max.
        # 1206×2622 – iPhone 16 Pro.
        # 1080×2424 – Google Pixel 9 and similar devices.
        # 1080×2400 – Google Pixel 8 and many Android phones.
        # 828×1792 – iPhone XR and similar models.
        # 414×896 – iPhone 11 and similar large-screen iPhones.
        # 412×915 – Common mid-range Android phones.
        # 390×844 – iPhone 14 Pro.
        # 375×812 – iPhone X and XS.
        # 360×640 – Low-end Android smartphones.
        # 320×480 – Very old smartphone models.

        # Tablet Resolutions
        # 1280×800 – Android tablets and 2-in-1 devices.
        # 800×1280 – Common in small Android tablets.
        # 768×1024 – Standard for older iPads and 9–10" tablets.
        # 1024×768 – Seen in older tablets and legacy displays.

        useragentsgame = []

        # Playstation 5
        useragentsgame.append('Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15')
        # Playstation 4
        useragentsgame.append('Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)')
        # Playstation Vita
        useragentsgame.append('Mozilla/5.0 (PlayStation Vita 3.61) AppleWebKit/537.73 (KHTML, like Gecko) Silk/3.2')
        # Xbox Series X
        useragentsgame.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox Series X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/20.02')
        # Xbox One S
        useragentsgame.append('Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393')
        # Xbox One
        useragentsgame.append('Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586')
        # Nintendo Switch
        useragentsgame.append('Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, like Gecko) NF/4.0.0.5.10 NintendoBrowser/5.1.0.13343')
        # Nintendo Wii U
        useragentsgame.append('Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US')
        # Nintendo 3DS
        useragentsgame.append('Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU')

        useragentsereader = []

        # Amazon Kindle 4
        useragentsereader.append('Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+')
        # Amazon Kindle 3
        useragentsereader.append('Mozilla/5.0 (Linux; U; en-US) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600x800; rotate)')
        # Onyx Note Air 3C
        useragentsereader.append('Dalvik/2.1.0 (Linux; U; Android 12; NoteAir3C Build/2023-11-15_15-07_3.5_0a296ec2c)')


        useragentsbots = []

        # Facebook bot
        useragentsbots.append('Mozilla/5.0 (compatible; FacebookBot/1.0; +https://developers.facebook.com/docs/sharing/webmasters/facebookbot/)')
        # OpenAI Search bot
        useragentsbots.append('Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot')
        # ChatGPT
        useragentsbots.append('Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot')
        # Google bot
        useragentsbots.append('Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)')
        # Bing bot
        useragentsbots.append('Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)')
        # Yahoo! bot
        useragentsbots.append('Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)')

        useragentsall = useragentsdesktop + useragentsmobile + useragentstv + useragentsgame + useragentsereader

        useragentallsize = useragentdesktopsize + useragentmobilesize

        chrome_options = Options()
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--disable-gpu")
        # chrome_options.add_argument("start-maximized");
        all = ''
        if randomset == 'all':
            all = '1'
            self.useragent = random.choice(useragentsall)
            self.useragentsize = random.choice(useragentallsize)

        elif randomset == 'desktop':
            all = '2'
            self.useragent = random.choice(useragentsdesktop)
            self.useragentsize = random.choice(useragentdesktopsize)

        # Windows 10-based PC using Edge browser
        # Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0
        # Chrome OS-based laptop using Chrome browser (Chromebook)
        # Mozilla/5.0 (X11; CrOS x86_64 14541.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36
        # Mac OS X-based computer using a Safari browser
        # Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3.1 Safari/605.1.15
        # Windows 7-based PC using a Chrome browser
        # Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36>
        # Linux-based PC using a Firefox browser
        # Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1

        elif randomset == 'mobile':
            all = '3'
            self.useragent = random.choice(useragentsmobile)
            self.useragentsize = random.choice(useragentmobilesize)

        # Android User Agents With the Client Hints support
        # Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36
        # Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36,gzip(gfe)

        # Samsung Galaxy S25
        # Mozilla/5.0 (Linux; Android 15; SM-S931B Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 15; SM-S931U Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36
        # Samsung Galaxy S24 Ultra
        # Mozila/5.0 (Linux; Android 14; SM-S928B/DS) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36
        # Mozila/5.0 (Linux; Android 14; SM-S928W) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36
        # Samsung Flip
        # Mozilla/5.0 (Linux; Android 14; SM-F9560 Build/UP1A.231005.007; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/127.0.6533.103 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 14; SM-F956U) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36
        # Samsung Galaxy Xcover7
        # Mozilla/5.0 (Android 15; Mobile; SM-G556B/DS; rv:130.0) Gecko/130.0 Firefox/130.0
        # Mozilla/5.0 (Android 15; Mobile; SM-G556B; rv:130.0) Gecko/130.0 Firefox/130.0
        # Samsung Galaxy S23
        # Mozilla/5.0 (Linux; Android 13; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36 Dalvik/2.1.0 (Linux; U; Android 13; SM-S911B Build/TP1A.220624.014)
        # Mozilla/5.0 (Linux; Android 13; SM-S911U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy S22 5G
        # Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 13; SM-S901U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy S22 Ultra 5G
        # Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 13; SM-S908U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy S21 5G
        # Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 13; SM-G991U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy S21 Ultra 5G
        # Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 13; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy A53 5G
        # Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 13; SM-A536U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy A51
        # Mozilla/5.0 (Linux; Android 13; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 13; SM-A515U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Samsung Galaxy S10
        # Mozilla/5.0 (Linux; Android 12; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Mozilla/5.0 (Linux; Android 12; SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36

        # Google Pixel 9 Pro
        # Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro Build/AD1A.240418.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.54 Mobile Safari/537.36
        # Google Pixel 9
        # Mozilla/5.0 (Linux; Android 14; Pixel 9 Build/AD1A.240411.003.A5; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/124.0.6367.54 Mobile Safari/537.36
        # Google Pixel 8 Pro
        # Mozilla/5.0 (Linux; Android 15; Pixel 8 Pro Build/AP4A.250105.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36
        # Google Pixel 8
        # Mozilla/5.0 (Linux; Android 15; Pixel 8 Build/AP4A.250105.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36
        # Google Pixel 7 Pro
        # Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Google Pixel 7
        # Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Google Pixel 6 Pro
        # Mozilla/5.0 (Linux; Android 13; Pixel 6 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Google Pixel 6a
        # Mozilla/5.0 (Linux; Android 13; Pixel 6a) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Google Pixel 6
        # Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36

        # Motorola Moto G (2025)
        # Mozilla/5.0 (Linux; Android 15; moto g - 2025 Build/V1VK35.22-13-2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/132.0.6834.163 Mobile Safari/537.36
        # Motorola Moto Edge 30 Neo
        # Dalvik/2.1.0 (Linux; U; Android 15; moto edge 30 neo Build/AP3A.241105.008)
        # Motorola Moto g04
        # Mozilla/5.0 (Linux; Android 14; Moto g04) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.64 Mobile Safari/537.36 Instabridge/22
        # Motorola Moto G Stylus 5G (2024)
        # Mozilla/5.0 (Linux; Android 14; moto g stylus 5G - 2024 Build/U2UB34.44-86; wv)
        # Motorola Moto G Power 5G (2024)
        # Mozilla/5.0 (Linux; Android 14; moto g power 5G - 2024 Build/U1UD34.16-62; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/123.0.6312.99 Mobile Safari/537.36
        # Motorola Razr 50 Ultra
        # Mozilla/5.0 (Linux; Android 14; motorola razr 50 ultra Build/U3UX34.56-29-2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/126.0.6478.134 Mobile Safari/537.36
        # Motorola Moto G Pure
        # Mozilla/5.0 (Linux; Android 12; moto g pure) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Motorola Moto G Stylus 5G
        # Mozilla/5.0 (Linux; Android 12; moto g stylus 5G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36v
        # Motorola Moto G Stylus 5G (2022)
        # Mozilla/5.0 (Linux; Android 12; moto g stylus 5G (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Motorola Moto G 5G (2022)
        # Mozilla/5.0 (Linux; Android 12; moto g 5G (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Motorola Moto G Power (2022)
        # Mozilla/5.0 (Linux; Android 12; moto g power (2022)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Motorola Moto G Power (2021)
        # Mozilla/5.0 (Linux; Android 11; moto g power (2021)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36

        # Redmi Note 13 4G
        # Mozilla/5.0 (Linux; Android 13; 23129RAA4G Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36
        # Redmi Turbo 4
        # Mozilla/5.0 (Linux; Android 15; 24129RT7CC Build/AP3A.240905.015.A2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/130.0.6723.86 Mobile Safari/537.36
        # Huawei Pura 70 Ultra
        # Mozilla/5.0 (Linux; Android 12; HBP-LX9 Build/HUAWEIHBP-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36
        # Huawei Nova 12 Pro
        # Mozilla/5.0 (Linux; U; Android 12; zh-Hans-CN; ADA-AL00 Build/HUAWEIADA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Quark/6.11.2.531 Mobile Safari/537.36
        # Huawei Nova Flip
        # Mozilla/5.0 (Linux; Android 12; PSD-AL00 Build/HUAWEIPSD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.88 Mobile Safari/537.36
        # Xiaomi 14 Ultra
        # Mozilla/5.0 (Linux; Android 14; 24030PN60G Build/UKQ1.231003.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/122.0.6261.119 Mobile Safari/537.36
        # Mix Flip
        # Mozilla/5.0 (Linux; Android 14; 2405CPX3DC Build/UKQ1.240116.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.193 Mobile Safari/537.36
        # Redmi Note 9 Pro
        # Mozilla/5.0 (Linux; Android 12; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Redmi Note 8 Pro
        # Mozilla/5.0 (Linux; Android 11; Redmi Note 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Huawei P30 Pro
        # Mozilla/5.0 (Linux; Android 10; VOG-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Huawei P30 lite
        # Mozilla/5.0 (Linux; Android 10; MAR-LX1A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Redmi Note 10 Pro
        # Mozilla/5.0 (Linux; Android 13; M2101K6G) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Xiaomi Poco X3 Pro
        # Mozilla/5.0 (Linux; Android 12; M2102J20SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # Redmi Note 11 Pro 5G
        # Mozilla/5.0 (Linux; Android 12; 2201116SG) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36
        # OnePlus Nord N200 5G
        # Mozilla/5.0 (Linux; Android 12; DE2118) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36

        # Apple iPhone 16e
        # Mozilla/5.0 (iPhone17,5; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 FireKeepers/1.7.0
        # Apple iPhone 16 Pro
        # Mozilla/5.0 (iPhone17,1; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Mohegan Sun/4.7.4
        # Apple iPhone 16 Pro Max
        # Mozilla/5.0 (iPhone17,2; CPU iPhone OS 18_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.5.2
        # Apple iPhone 16
        # Mozilla/5.0 (iPhone17,3; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 FireKeepers/1.6.1
        # Apple iPhone 16 Plus
        # Mozilla/5.0 (iPhone17,4; CPU iPhone OS 18_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.7.5
        # Apple iPhone 15 Pro
        # Mozilla/5.0 (iPhone16,2; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.7.5
        # Apple iPhone 14
        # Mozilla/5.0 (iPhone14,7; CPU iPhone OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Mohegan Sun/4.7.3
        # Apple iPhone 13 Pro
        # Mozilla/5.0 (iPhone14,2; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Mohegan Sun/4.7.4
        # Apple iPhone SE (3rd generation)
        # Mozilla/5.0 (iPhone14,6; U; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19E241 Safari/602.1
        # iPhone 13 Pro Max
        # Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1
        # iPhone 12
        # Mozilla/5.0 (iPhone13,2; U; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1
        # iPhone 11
        # Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1
        # iPhone 11
        # Mozilla/5.0 (iPhone12,1; U; CPU iPhone OS 13_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/15E148 Safari/602.1
        # Apple iPhone XR (Safari)
        # Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1
        # Apple iPhone XS (Chrome)
        # Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/69.0.3497.105 Mobile/15E148 Safari/605.1
        # Apple iPhone XS Max (Firefox)
        # Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/13.2b11866 Mobile/16A366 Safari/605.1.15
        # Apple iPhone X
        # Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1
        # Apple iPhone 8
        # Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1
        # Apple iPhone 8 Plus
        # Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A5370a Safari/604.1
        # Apple iPhone 7
        # Mozilla/5.0 (iPhone9,3; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1
        # Apple iPhone 7 Plus
        # Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1
        # Apple iPhone 6
        # Mozilla/5.0 (Apple-iPhone7C2/1202.466; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543 Safari/419.3

        # Microsoft Lumia 650
        # Mozilla/5.0 (Windows Phone 10.0; Android 6.0.1; Microsoft; RM-1152) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Mobile Safari/537.36 Edge/15.15254
        # Microsoft Lumia 550
        # Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; RM-1127_16056) AppleWebKit/537.36(KHTML, like Gecko) Chrome/42.0.2311.135 Mobile Safari/537.36 Edge/12.10536
        # Microsoft Lumia 950
        # Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Microsoft; Lumia 950) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.1058

        # Apple iPad Pro (11 5th Gen)
        # Mozilla/5.0 (iPad16,3; CPU OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Tropicana_NJ/5.7.1
        # Samsung Galaxy Tab Active5 5G
        # Dalvik/2.1.0 (Linux; U; Android 14; SM-X306B Build/UP1A.231005.007)
        # Samsung Galaxy Tab S6 Lite
        # Dalvik/2.1.0 (Linux; U; Android 14; SM-P619N Build/UP1A.231005.007)
        # Xiaomi Pad 7 Pro
        # Dalvik/2.1.0 (Linux; U; Android 15; 24091RPADG Build/AQ3A.240801.002)
        # Amazon Fire HD 8 (2024, 12th Gen)
        # Dalvik/2.1.0 (Linux; U; Android 11; KFRASWI Build/RS8332.3115N)
        # Samsung Galaxy Tab S6 Lite
        # Dalvik/2.1.0 (Linux; U; Android 14; SM-P619N Build/UP1A.231005.007)
        # Lenovo Tab M10a 5G
        # Dalvik/2.1.0 (Linux; U; Android 13; LET02 Build/TKQ1.230127.002)
        # Apple iPad Air 11 (M3)
        # Mozilla/5.0 (iPad15,3; CPU OS 18_3_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Resorts/4.7.5
        # Samsung Galaxy Tab S8 Ultra
        # Mozilla/5.0 (Linux; Android 12; SM-X906C Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36
        # Lenovo Yoga Tab 11
        # Mozilla/5.0 (Linux; Android 11; Lenovo YT-J706X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36
        # Google Pixel C
        # Mozilla/5.0 (Linux; Android 7.0; Pixel C Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36
        # Sony Xperia Z4 Tablet
        # Mozilla/5.0 (Linux; Android 6.0.1; SGP771 Build/32.2.A.0.253; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.98 Safari/537.36
        # Nvidia Shield Tablet K1
        # Mozilla/5.0 (Linux; Android 6.0.1; SHIELD Tablet K1 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Safari/537.36
        # Samsung Galaxy Tab S3
        # Mozilla/5.0 (Linux; Android 7.0; SM-T827R4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.116 Safari/537.36
        # Samsung Galaxy Tab A
        # Mozilla/5.0 (Linux; Android 5.0.2; SAMSUNG SM-T550 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/3.3 Chrome/38.0.2125.102 Safari/537.36
        # Amazon Kindle Fire HDX 7
        # Mozilla/5.0 (Linux; Android 4.4.3; KFTHWI Build/KTU84M) AppleWebKit/537.36 (KHTML, like Gecko) Silk/47.1.79 like Chrome/47.0.2526.80 Safari/537.36
        # LG G Pad 7.0
        # Mozilla/5.0 (Linux; Android 5.0.2; LG-V410/V41020c Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/34.0.1847.118 Safari/537.36

        elif randomset == 'tv':
            all = '4'
            self.useragent = random.choice(useragentstv)
            self.useragentsize = random.choice(useragentdesktopsize)

        # Amazon Fire TV Stick 4K Max (2nd Gen 2023)
        # Mozilla/5.0 (Linux; Android 11; AFTKRT Build/RS8101.1849N; wv)PlexTV/10.0.0.4149
        # Amazon Fire TV Cube (3rd Gen)
        # Mozilla/5.0 (Linux; Android 9; AFTGAZL Build/PS7607.3166N; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/102.0.5005.125 Mobile Safari/537.36 FE v1.79.1
        # Doom Pro 5G
        # Mozilla/5.0 (Linux; Android 14; DOOM PRO 5G Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Safari/537.36 FE v1.87.3
        # Apple TV (2022)
        # AppleTV14,1/16.1
        # Minix NEO X39
        # Mozilla/5.0 (Linux; Android 7.1.2; NEO_X39) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.99 Safari/537.36
        # Amazon Fire TV Stick 4K Max
        # Mozilla/5.0 (Linux; Android 9; AFTKA) AppleWebKit/537.36 (KHTML, like Gecko) Silk/92.2.11 like Chrome/92.0.4515.159 Safari/537.36
        # Amazon Fire TV Cube
        # Mozilla/5.0 (Linux; Android 9; AFTR) AppleWebKit/537.36 (KHTML, like Gecko) Silk/98.6.10 like Chrome/98.0.4758.136 Safari/537.36
        # Google ADT-2
        # Dalvik/2.1.0 (Linux; U; Android 9; ADT-2 Build/PTT5.181126.002)
        # Chromecast
        # Mozilla/5.0 (CrKey armv7l 1.5.16041) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.0 Safari/537.36
        # Roku Ultra
        # Roku4640X/DVP-7.70 (297.70E04154A)
        # Minix NEO X5
        # Mozilla/5.0 (Linux; U; Android 4.2.2; he-il; NEO-X5-116A Build/JDQ39) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30
        # Amazon AFTWMST22
        # Mozilla/5.0 (Linux; Android 9; AFTWMST22 Build/PS7233; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.4324.152 Mobile Safari/537.36
        # Amazon 4K Fire TV
        # Mozilla/5.0 (Linux; Android 5.1; AFTS Build/LMY47O) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/41.99900.2250.0242 Safari/537.36
        # Google Nexus Player
        # Dalvik/2.1.0 (Linux; U; Android 6.0.1; Nexus Player Build/MMB29T)
        # Apple TV 6th Gen 4K
        # AppleTV11,1/11.1
        # Apple TV 5th Gen 4K
        # AppleTV6,2/11.1
        # Apple TV 4th Gen
        # AppleTV5,3/9.1.1

        elif randomset == 'game':
            all = '5'
            self.useragent = random.choice(useragentsgame)
            self.useragentsize = random.choice(useragentdesktopsize)

        # Playstation 5
        # Mozilla/5.0 (PlayStation; PlayStation 5/2.26) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0 Safari/605.1.15
        # Playstation 4
        # Mozilla/5.0 (PlayStation 4 3.11) AppleWebKit/537.73 (KHTML, like Gecko)
        # Playstation Vita
        # Mozilla/5.0 (PlayStation Vita 3.61) AppleWebKit/537.73 (KHTML, like Gecko) Silk/3.2
        # Xbox Series X
        # Mozilla/5.0 (Windows NT 10.0; Win64; x64; Xbox; Xbox Series X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36 Edge/20.02
        # Xbox One S
        # Mozilla/5.0 (Windows NT 10.0; Win64; x64; XBOX_ONE_ED) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393
        # Xbox One
        # Mozilla/5.0 (Windows Phone 10.0; Android 4.2.1; Xbox; Xbox One) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2486.0 Mobile Safari/537.36 Edge/13.10586
        # Nintendo Switch
        # Mozilla/5.0 (Nintendo Switch; WifiWebAuthApplet) AppleWebKit/601.6 (KHTML, like Gecko) NF/4.0.0.5.10 NintendoBrowser/5.1.0.13343
        # Nintendo Wii U
        # Mozilla/5.0 (Nintendo WiiU) AppleWebKit/536.30 (KHTML, like Gecko) NX/3.0.4.2.12 NintendoBrowser/4.3.1.11264.US
        # Nintendo 3DS
        # Mozilla/5.0 (Nintendo 3DS; U; ; en) Version/1.7412.EU

        elif randomset == 'ereader':
            all = '6'
            self.useragent = random.choice(useragentsereader)
            self.useragentsize = random.choice(useragentmobilesize)

        # Amazon Kindle 4
        # Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 Safari/533.2+ Kindle/3.0+
        # Amazon Kindle 3
        # Mozilla/5.0 (Linux; U; en-US) AppleWebKit/528.5+ (KHTML, like Gecko, Safari/528.5+) Version/4.0 Kindle/3.0 (screen 600x800; rotate)
        # Onyx Note Air 3C
        # Dalvik/2.1.0 (Linux; U; Android 12; NoteAir3C Build/2023-11-15_15-07_3.5_0a296ec2c)

        elif randomset == 'bots':
            all = '7'
            self.useragent = random.choice(useragentsbots)
            self.useragentsize = random.choice(useragentallsize)

        # Facebook bot
        # Mozilla/5.0 (compatible; FacebookBot/1.0; +https://developers.facebook.com/docs/sharing/webmasters/facebookbot/)
        # OpenAI Search bot
        # Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot
        # ChatGPT
        # Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot
        # Google bot
        # Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)
        # Bing bot
        # Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)
        # Yahoo! bot
        # Mozilla/5.0 (compatible; Yahoo! Slurp; http://help.yahoo.com/help/us/ysearch/slurp)

        else:
            all = '9'
            self.useragent = ''
            self.useragentsize = {'':''}

        chrome_options.add_argument(self.useragent)
        chrome_options.add_argument("disable-infobars");
        chrome_options.add_argument("--disable-extensions");
        chrome_options.add_argument("--no-sandbox")  # linux only
        chrome_options.add_argument("--headless=new")  # for Chrome >= 109
        chrome_options.add_argument("--headless")
        chrome_options.headless = True  # also works

        return chrome_options

    def insItemsStatement(self, handler, insstatement):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            try:
                dbhandler.execute(insstatement)
                self.database_check = '<span style=\"color:green;\">Successful</span>'
            except pymysql.Error as e:
                print(e)
                print(insstatement)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(insstatement))
                self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                return

            if self.debug and self.debuglevel >= 0:
                print(dbhandler.rowcount)
        finally:
            handlersconn.close()  # returns the connection to the pool

    def getJobsFiguresFromTables(self, handler):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            self.updatedjobs = 0
            getupdatedjobs = "SELECT count(*) as cnt FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed = 2;"
            if self.debug and self.debuglevel >= 0:
                print(getupdatedjobs)
            try:
                dbhandler.execute(getupdatedjobs)
                for item in dbhandler.fetchall():
                    self.updatedjobs = item["cnt"]
                    if self.debug and self.debuglevel >= 0:
                        print(self.updatedjobs)
            except pymysql.Error as e:
                print(e)
                print(getupdatedjobs)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(getupdatedjobs))
                return

            self.insertedjobs = 0
            getinsertedjobs = "SELECT count(*) as cnt FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed = 1;"
            if self.debug and self.debuglevel >= 0:
                print(getinsertedjobs)
            try:
                dbhandler.execute(getinsertedjobs)
                for item in dbhandler.fetchall():
                    self.insertedjobs = item["cnt"]
                    if self.debug and self.debuglevel >= 0:
                        print(self.insertedjobs)
            except pymysql.Error as e:
                print(e)
                print(getinsertedjobs)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(getinsertedjobs))
                return

            self.deletedjobs = 0
            getdeletedjobs = "SELECT count(*) as cnt FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed is null;"
            if self.debug and self.debuglevel >= 0:
                print(getdeletedjobs)
            try:
                dbhandler.execute(getdeletedjobs)
                for item in dbhandler.fetchall():
                    self.deletedjobs = item["cnt"]
                    if self.debug and self.debuglevel >= 0:
                        print(self.deletedjobs)
            except pymysql.Error as e:
                print(e)
                print(getdeletedjobs)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(getdeletedjobs))
                return
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def processDBJobsTables(self, handler, colsfromfeed, addcolumns = '', delete = 'delete'):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            if self.cleardata is not None and self.cleardata != "":
                cldata = self.cleardata.split(";")
            else:
                cldata = '0;0;0;0;0'.split(";")

            # if '`postcode`' not in colsfromfeed:
            #     addcolumns += ', `postcode`'
            # if '`ctown`' not in colsfromfeed:
            #     addcolumns += ', `ctown`'
            # if '`county`' not in colsfromfeed:
            #     addcolumns += ', `county`'
            # if '`country`' not in colsfromfeed:
            #     addcolumns += ', `country`'

            insertarctablefields = "`nj_date`, `dtstamp`, " + colsfromfeed + ", `existinfeed`, `job_feed_id`" + addcolumns
            insertselecttablefields = "`dtstamp`, " + colsfromfeed + ", `existinfeed`, `job_feed_id`" + addcolumns
            insertothertablefields = "`nj_date`, `ustatid`, `dtstamp`, " + colsfromfeed + ", `existinfeed`, `job_feed_id`" + addcolumns
            insertintoarctable = "INSERT INTO `" + self.cfg.database + "`.`" + self.arctablename + "` (" + insertarctablefields + ") SELECT now(), " + insertselecttablefields + " FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "';"
            if cldata[1] == '0' or cldata[1] == 0:
                if self.debug and self.debuglevel >= 0:
                    print(insertintoarctable)
                try:
                    dbhandler.execute(insertintoarctable)
                    print("Inserted into arc table! Affected rows -> " + str(dbhandler.rowcount))
                except pymysql.Error as e:
                    print(e)
                    print(insertintoarctable)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(insertintoarctable))
                    return

            insertintodeletetable = "INSERT INTO `" + self.cfg.database + "`.`" + self.deletetablename + "` (" + insertothertablefields + ") SELECT now(), '" + str(self.ustatid) + "', " + insertselecttablefields + " FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed is null;"
            if cldata[2] == '0' or cldata[2] == 0:
                if self.debug and self.debuglevel >= 0:
                    print(insertintodeletetable)
                try:
                    dbhandler.execute(insertintodeletetable)
                    print("Inserted into delete table! Affected rows -> " + str(dbhandler.rowcount))
                except pymysql.Error as e:
                    print(e)
                    print(insertintodeletetable)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(insertintodeletetable))
                    return

            insertintoinserttable = "INSERT INTO `" + self.cfg.database + "`.`" + self.inserttablename + "` (" + insertothertablefields + ") SELECT now(), '" + str(self.ustatid) + "', " + insertselecttablefields + " FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed = 1;"
            if cldata[3] == '0' or cldata[3] == 0:
                if self.debug and self.debuglevel >= 0:
                    print(insertintoinserttable)
                try:
                    dbhandler.execute(insertintoinserttable)
                    print("Inserted into insert table! Affected rows -> " + str(dbhandler.rowcount))
                except pymysql.Error as e:
                    print(e)
                    print(insertintoinserttable)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(insertintoinserttable))
                    return

            insertintoupdatetable = "INSERT INTO `" + self.cfg.database + "`.`" + self.updatetablename + "` (" + insertothertablefields + ") SELECT now(), '" + str(self.ustatid) + "', " + insertselecttablefields + " FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed = 2;"
            if cldata[4] == '0' or cldata[4] == 0:
                if self.debug and self.debuglevel >= 0:
                    print(insertintoupdatetable)
                try:
                    dbhandler.execute(insertintoupdatetable)
                    print("Inserted into update table! Affected rows -> " + str(dbhandler.rowcount))
                except pymysql.Error as e:
                    print(e)
                    print(insertintoupdatetable)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(insertintoupdatetable))
                    return

            if self.ats == 'tribepad':
                deletefrommedia = "DELETE FROM `" + self.cfg.database + "`.`tribepad_xml_media` WHERE job_feed_id = '" + self.jobfeedid + "' and job_id in (SELECT job_id FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed is null) and reference in (SELECT reference FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed is null);"
                try:
                    dbhandler.execute(deletefrommedia)
                    print("Deleted from media table! Affected rows -> " + str(dbhandler.rowcount))
                except pymysql.Error as e:
                    print(e)
                    print(deletefrommedia)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(deletefrommedia))
                    return

            if delete != 'donotdelete':
                deletejobs = "DELETE FROM `" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and existinfeed is null;"
                try:
                    dbhandler.execute(deletejobs)
                    print("Deleted from main table! Affected rows -> " + str(dbhandler.rowcount))
                except pymysql.Error as e:
                    print(e)
                    print(deletejobs)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(deletejobs))
                    return
        finally:
            handlersconn.close()  # returns the connection to the pool

    def getTableColsTypes(self, handler):
        gettablecolstypes = 'SELECT column_name, data_type FROM information_schema.columns where table_schema = \'' + self.cfg.dbname + '\' and table_name = \'' + self.tablename + '\';'
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            try:
                dbhandler.execute(gettablecolstypes)
            except pymysql.Error as e:
                print(e)
                print(gettablecolstypes)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(gettablecolstypes))
                if self.debug is not True:
                    return

            for rowret in dbhandler.fetchall():
                if self.debug and self.debuglevel >= 0:
                    print(rowret)
                try:
                    if rowret['data_type'] == 'date':
                        self.dtarr.append(rowret['column_name'])
                    if rowret['data_type'] == 'datetime':
                        self.dtarr.append(rowret['column_name'])
                    if rowret['data_type'] == 'tinyint':
                        self.boolarr.append(rowret['column_name'])
                    if rowret['data_type'] == 'int':
                        self.intarr.append(rowret['column_name'])
                except Exception as e:
                    if rowret['DATA_TYPE'] == 'date':
                        self.dtarr.append(rowret['COLUMN_NAME'])
                    if rowret['DATA_TYPE'] == 'datetime':
                        self.dtarr.append(rowret['COLUMN_NAME'])
                    if rowret['DATA_TYPE'] == 'tinyint':
                        self.boolarr.append(rowret['COLUMN_NAME'])
                    if rowret['DATA_TYPE'] == 'int':
                        self.intarr.append(rowret['COLUMN_NAME'])
                    if self.debug and self.debuglevel >= 0:
                        print(e)
        finally:
            handlersconn.close()                                # returns the connection to the pool

        if self.debug and self.debuglevel >= 0:
            print(self.dtarr)
            print(self.boolarr)
            print(self.intarr)

    def processAllFeeds(self):
        try:
            handlersconn = self.myConnectionMain.connection()
            handlers = handlersconn.cursor()

            handlers.execute('SET NAMES utf8mb4;')
            handlers.execute('SET character_set_connection=utf8mb4;')

            handlerstmnt = 'SELECT * FROM ' + self.cfg.database + '.handlers ' \
                           'WHERE active = ' + str(self.actst) + \
                           ' ORDER BY jobfeed_id;'

            handlers.execute(handlerstmnt)

            if self.debug and self.debuglevel >= 0:
                print(handlerstmnt)

            for handler in handlers.fetchall():
                if self.debug and self.debuglevel >= 0:
                    print(handler)
                print(str(self.processdatetime) + " -> " + str(handler['ats']) + " -> " + str(handler['jobfeed_id']))
                if str(self.actst) == '4':
                    if handler['cronjob'] is not None:
                        if croniter.match(handler['cronjob'], self.processdatetime):
                            if handler['ats'] == 'try':
                                # self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "1")
                                self.processTryFeed(handler)
                                # self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "0")
                            if handler['ats'] == 'unijson':
                                self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "1")
                                self.processUNIJSONFeed(handler)
                                self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "0")
                            if handler['ats'] == 'unijsonsku':
                                # self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "1")
                                self.importPerSKU(handler)
                                # self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "0")
                            if handler['ats'] == 'webscrape':
                                # self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "1")
                                self.prWebScraping(handler)
                                # self.cfgmain.lockExec("handlers", handler['active'], handler['jobfeed_id'], "0")
        finally:
            handlersconn.close()                                # returns the connection to the pool

    async def getpage(self, url, useselect=0, clicktag='', usesauth=False):
        # launch chromium browser in the background
        # browser = await launch()
        browser = await launch(options={'args': ['--no-sandbox']})
        # open a new tab in the browser
        page = await browser.newPage()
        # # set timeout to 0
        # await page.setDefaultNavigationTimeout(0)

        # await page.setViewport({width: 1366, height: 768});
        # await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');

        # print(await page.content())
        #
        if usesauth:
            await page.authenticate({'username':self.feeduser, 'password': self.feedpass});
            # await page.type('input#username', self.feeduser)
            # await page.type('input#password', self.feedpass)

        # add URL to a new page and then open it
        await page.goto(url)
        # wait 5 sec
        await page.waitFor(2000)
        if useselect == 1:
            # select an option from a select dropdown
            await page.select(clicktag, "50")
            await page.waitFor(2000)

        # create a screenshot of the page and save it
        self.pageoutput = await page.content()
        # await page.screenshot({"path": "python.png"})
        # close the browser
        await browser.close()

    # Wizzair flights checker and alerter
    def processTryFeed(self, handler):
        self.debug = True
        self.debuglevel = 0

        start = datetime.now()
        print(start)

        flightdb = self.myConnectionMain.cursor()

        self.resetFeedVars()
        self.loadFeedVars(handler)

        if self.feedlocks == 1:
            errormsg = self.jobfeedid + ' Handler locked!!!'
            print(errormsg)
            self.cfgmain.sendErrorEmail(handler, errormsg)
            return

        print('Processing: ' + self.jobfeedid)

        # url = 'https://login.microsoftonline.com/720b637a-655a-40cf-816a-f22f40755c2c/oauth2/v2.0/token'
        #
        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded'
        # }
        #
        # data = {
        #     'client_id': 'fc62accf-9120-4d6d-863c-b9a5bc3ba879',
        #     'client_secret': 'fXs8Q~B27ejTvXXe8sB22F1U3Tz5VvgrWsQO1avP',
        #     'scope': 'https://api.prod.ingka.com/.default',
        #     'grant_type': 'client_credentials',
        #     'content-type': 'application/x-www-form-urlencoded'
        # }
        #
        # r = requests.get(url, headers=headers, data=data)
        # print(r.status_code)
        # print(r.content)
        #
        # js = json.loads(r.content)
        # print(js['access_token'])
        #
        # url2 = 'https://api.ingka.ikea.com/peopledomain/recsrc/jobservice/jobs'
        #
        # headers2 = {
        #     'Content-Type': 'application/json',
        #     'X-Client-Id': 'fc62accf-9120-4d6d-863c-b9a5bc3ba879',
        #     'Authorization': 'Bearer ' + js['access_token']
        # }
        #
        # rr = requests.get(url2, headers=headers2)
        # print(rr.status_code)
        # print(rr.content)


        # exit(0)

        # self.updJobsTable(handler)

        headers = {
            'authority': 'be.wizzair.com',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://wizzair.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'referer': 'https://wizzair.com/en-gb/search/search',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6'}

        # 'referer': 'https://wizzair.com/en-gb/search/timetable',

        # 	'authority': 'be.wizzair.com',
        # 	'accept': 'application/json, text/plain, */*',
        # 	'origin': 'https://wizzair.com',
        # 	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        # 	'content-type': 'application/json;charset=UTF-8',
        # 	'sec-fetch-site': 'same-site',
        # 	'sec-fetch-mode': 'cors',
        # 	'referer': 'https://wizzair.com/en-gb/flights/timetable',
        # 	'accept-encoding': 'gzip, deflate, br',
        # 	'accept-language': 'en-GB,en;q=0.9,hu-HU;q=0.8,hu;q=0.7,en-US;q=0.6'

        wizzbuildnum = "https://wizzair.com/buildNumber"
        # wizzbuildnum = "https://wizzair.com/static_fe/metadata.json"

        # https://be.wizzair.com/25.5.0/Api/search/search
        # <Response [428]>
        # 428
        # b'{"sec-cp-challenge": "true","provider":"crypto","chlge_content_url":"/9Bj7qYOnhnVJMtmEOqEKtI3pU_E/Gf/eHk4MGgAJwM/JkVZVnd/vfgUAAQ","branding_url_content":"/9Bj7qYOnhnVJMtmEOqEKtI3pU_E/Gf/eHk4MGgAJwM/Un0NGVt/mZ0ICAQ","chlg_duration":30,"token":"AAQAAAAK_____35AP1ZAXRBC5CAIKsxqQ8-UOUVZBoFxHcDypZj6Uj371gFE41Le3lyxc7b3IBNJo5MAGjxR0ueddx8PRZ8KRjTo59ciA60lME5f4Xh4yzLwUOpfg6Tkpkojq_vB7z94P7UMfsbMdEjsZIoMeBoM-4HoRjDhywqDdtz2GbDeBUS13PDeauuwMdCBzhfELqZ6i7jvZ8RWhBRy2Xsg57MtPsWWxQcWxPNVcfPZc3VNUqNteV3o1CnJFMTybYgio6x5P3wVhImnmXdrtqtyGaKyQqY2QW7qZNPmNDI6XFqMDjdFOD5-W5ckc5lQRjVrstzyefxWwvPvIA","timestamp":1730569706,"nonce":"6e7ec92d4860a2a6e7e4","difficulty":15000,"count":1,"timeout":1000,"cpu":false,"verify_url":"https://be.wizzair.com/9Bj7qYOnhnVJMtmEOqEKtI3pU_E/GfwYfJwi/eHk4MGgAJwM/MWNYdjI/4GBgB"}'

        r = requests.get(wizzbuildnum, headers=headers)

        if self.debug and self.debuglevel >= 0:
            print(r.content)

        ver = str(r.content)[str(r.content).find("https://be.wizzair.com/")+23:-1]

        print(ver)

        # try:
        #     rr = json.loads(r.content)
        # except Exception as e:
        #     print(e)
        #
        # ver = rr['apiUrl'].split("/")
        #
        # print(ver[3])
        #
        # ver = ver[3]

        # rr = str(r.content).split(" ")
        #
        # if self.debug and self.debuglevel >= 0:
        #     print(rr)
        #     print(rr[2])
        #     print(rr[2][rr[2].find("m/")+2:])
        #
        # ver = rr[2][rr[2].find("m/")+2:]
        #
        # print(ver)

        # r = requests.get("https://be.wizzair.com/20.3.0/Api/asset/map?languageCode=en-gb&forceJavascriptOutput=true", headers=headers)
        #
        # # if self.debug and self.debuglevel >= 0:
        # print(r)
        # print(r.status_code)
        # print(r.content)
        #
        # jsondata = json.loads(r.content)
        #
        # print(jsondata)
        #
        # i = 0
        #
        # for item in jsondata:
        #     print(item)
        #     if item == 'javascript':
        #         print(item)
        #     else:
        #         for items in jsondata[item]:
        #             print(items)
        #             for key, value in items.items():
        #                 print(str(key) + " -> " + str(value))
        #                 print(type(value))
        #                 if isinstance(value, list):
        #                     print("list -> " + str(value))
        #                     print(len(value))
        #                     for k in range(0, len(value)):
        #                         if key == 'aliases' or key == 'categories':
        #                             print(key + " -> " + str(value[k]))
        #                         else:
        #                             for key1, value1 in value[k].items():
        #                                 print(str(key1) + " -> " + str(value1))
        #
        #             i += 1
        #
        #             # if i > 0:
        #             #     return
        #
        # return

        price_type = "wdc"

        # data = {"flightList": [{"departureStation": "LIS",  # Change this
        #                         "arrivalStation": "SOF",
        #                         "from": "2023-11-01",
        #                         "to": "2023-12-13"},
        #                        {"departureStation": "SOF",
        #                         "arrivalStation": "LIS",  # and this
        #                         "from": "2023-11-01",
        #                         "to": "2023-12-13"}], "priceType": price_type, "adultCount": 1, "childCount": 0, "infantCount": 0}

        datenow = datetime.now() # + timedelta(days=43)

        datefrom = (datenow + timedelta(days=1)).strftime("%Y-%m-%d")
        dateto = (datenow + timedelta(days=43)).strftime("%Y-%m-%d")

        if self.debug and self.debuglevel >= 0:
            print(datefrom)
            print(dateto)

        print(self.server)

        splitarr = []

        self.server = self.server.replace("\r", "")

        colsfromfeed = ''

        if self.server != '' and '|' in self.server:
            if '\n' in self.server:
                splitarr = self.server.split('\n')
            else:
                splitarr.append(self.server)
            for i in range(0,len(splitarr)):
                sparr = splitarr[i].split('|')

                data = {"flightList": [{"departureStation": sparr[0],  # Change this
                                        "arrivalStation": sparr[1],
                                        "from": datefrom,
                                        "to": dateto},
                                       {"departureStation": sparr[2],
                                        "arrivalStation": sparr[3],  # and this
                                        "from": datefrom,
                                        "to": dateto}], "priceType": price_type, "adultCount": 1, "childCount": 0, "infantCount": 0}

                # data = {}

                if self.debug and self.debuglevel >= 0:
                    print(data)

                # https://be.wizzair.com/19.3.0/Api/information/buildNumber - buildnumber in json
                # implemented # https://wizzair.com/buildNumber - buildnumber with some more info
                # implemented # https://be.wizzair.com/19.3.0/Api/search/timetable - timetable with POST request with header and data
                # https://wizzair.com/static_fe/metadata.json - some data?
                # https://be.wizzair.com/19.3.0/Api/asset/map?languageCode=en-gb&forceJavascriptOutput=true - all cities and routes from them
                # https://be.wizzair.com/19.3.0/Api/search/search/ - access dinied?

                # Web API endpoint: https://be.wizzair.com/9.14.1/Api/customer/
                # some known paths: /login, /profile, /mybookings

                if self.debug and self.debuglevel >= 0:
                    print(self.url)

                self.url = self.url.replace("XXX", ver)

                if self.debug and self.debuglevel >= 0:
                    print(self.url)

                # 'https://be.wizzair.com/' + ver + '/Api/search/timetable'

                rr = requests.post(self.url, headers=headers, data=json.dumps(data))
                print(rr.cookies)

                r = requests.post(self.url, headers=headers, data=json.dumps(data), cookies=r.cookies)
                print(r.cookies)

                if self.debug and self.debuglevel >= 0:
                    print(r)
                    print(r.status_code)
                    print(r.content)

                if r.status_code == 200:
                    outdata = r.json()["outboundFlights"]
                    indata = r.json()["returnFlights"]

                    if self.debug and self.debuglevel >= 0:
                        print(outdata)
                        print(indata)

                    inscols = ''
                    insvals = ''
                    updcolsvals = ''
                    colsfromfeed = ''
                    jobsinfeed = 0

                    for item in outdata:
                        if self.debug and self.debuglevel >= 0:
                            print(item)
                        for key in item:
                            if self.debug and self.debuglevel >= 0:
                                print(key)
                                print(item[key])
                            if key == 'price' or key == 'originalPrice':
                                if self.debug and self.debuglevel >= 0:
                                    print(key)
                                    print(item[key]['amount'])
                                    print(item[key]['currencyCode'])
                                inscols += "`" + key + "_" + "amount" + "`, "
                                insvals += "'" + str(item[key]['amount']) + "', "
                                updcolsvals += "`" + key + "_" + "amount" + "` = '" + str(item[key]['amount']) + "', "
                                inscols += "`" + key + "_" + "currencyCode" + "`, "
                                insvals += "'" + str(item[key]['currencyCode']) + "', "
                                updcolsvals += "`" + key + "_" + "currencyCode" + "` = '" + str(item[key]['currencyCode']) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "_" + "amount" + "`, "
                                    colsfromfeed = colsfromfeed + "`" + key + "_" + "currencyCode" + "`, "
                            elif key == 'departureDates':
                                if self.debug and self.debuglevel >= 0:
                                    print(key)
                                    print(item[key][0])
                                inscols += "`" + key + "`, "
                                insvals += "'" + str(item[key][0]) + "', "
                                updcolsvals += "`" + key + "` = '" + str(item[key][0]) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "
                            elif key == 'priceType':
                                inscols += "`" + key + "`, "
                                insvals += "'" + str(price_type) + "', "
                                updcolsvals += "`" + key + "` = '" + str(price_type) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "
                            elif key == 'hasMacFlight':
                                inscols += "`" + key + "`, "
                                insvals += str(item[key]) + ", "
                                updcolsvals += "`" + key + "` = " + str(item[key]) + ", "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "
                            else:
                                inscols += "`" + key + "`, "
                                insvals += "'" + str(item[key]) + "', "
                                updcolsvals += "`" + key + "` = '" + str(item[key]) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "

                        inscols = inscols[:-2]
                        insvals = insvals[:-2]
                        updcolsvals = updcolsvals[:-2]

                        if self.debug and self.debuglevel >= 0:
                            print(inscols)
                            print(insvals)
                            print(updcolsvals)

                        inscols += ", `" + "existinfeed" + "`"
                        insvals += ", '" + "1" + "'"
                        updcolsvals += ", `existinfeed` = '" + "2" + "'"

                        inscols += ", `" + "job_feed_id" + "`"
                        insvals += ", '" + self.jobfeedid + "'"
                        updcolsvals += ", `job_feed_id` = '" + self.jobfeedid + "'"

                        insstatement = "INSERT INTO `" + self.cfg.database + "`.`" + self.tablename + "` (" \
                                       + inscols + ")"
                        insstatement += " VALUES(" + insvals + ")"
                        insstatement += " ON DUPLICATE KEY UPDATE " + updcolsvals + ";"

                        if self.debug and self.debuglevel >= 9:
                            print(insstatement)

                        try:
                            flightdb.execute(insstatement)
                            self.database_check = '<span style=\"color:green;\">Successfull</span>'
                        except pymysql.Error as e:
                            print(e)
                            print(insstatement)
                            self.cfgmain.sendErrorEmail(handler, str(e) + str(insstatement))
                            self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                            return

                        inscols = ''
                        insvals = ''
                        updcolsvals = ''

                        jobsinfeed += 1


                    inscols = ''
                    insvals = ''
                    updcolsvals = ''
                    colsfromfeed = ''
                    jobsinfeed = 0

                    for item in indata:
                        if self.debug and self.debuglevel >= 0:
                            print(item)
                        for key in item:
                            if self.debug and self.debuglevel >= 0:
                                print(key)
                                print(item[key])
                            if key == 'price' or key == 'originalPrice':
                                if self.debug and self.debuglevel >= 0:
                                    print(key)
                                    print(item[key]['amount'])
                                    print(item[key]['currencyCode'])
                                inscols += "`" + key + "_" + "amount" + "`, "
                                insvals += "'" + str(item[key]['amount']) + "', "
                                updcolsvals += "`" + key + "_" + "amount" + "` = '" + str(item[key]['amount']) + "', "
                                inscols += "`" + key + "_" + "currencyCode" + "`, "
                                insvals += "'" + str(item[key]['currencyCode']) + "', "
                                updcolsvals += "`" + key + "_" + "currencyCode" + "` = '" + str(item[key]['currencyCode']) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "_" + "amount" + "`, "
                                    colsfromfeed = colsfromfeed + "`" + key + "_" + "currencyCode" + "`, "
                            elif key == 'departureDates':
                                if self.debug and self.debuglevel >= 0:
                                    print(key)
                                    print(item[key][0])
                                inscols += "`" + key + "`, "
                                insvals += "'" + str(item[key][0]) + "', "
                                updcolsvals += "`" + key + "` = '" + str(item[key][0]) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "
                            elif key == 'priceType':
                                inscols += "`" + key + "`, "
                                insvals += "'" + str(price_type) + "', "
                                updcolsvals += "`" + key + "` = '" + str(price_type) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "
                            elif key == 'hasMacFlight':
                                inscols += "`" + key + "`, "
                                insvals += str(item[key]) + ", "
                                updcolsvals += "`" + key + "` = " + str(item[key]) + ", "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "
                            else:
                                inscols += "`" + key + "`, "
                                insvals += "'" + str(item[key]) + "', "
                                updcolsvals += "`" + key + "` = '" + str(item[key]) + "', "
                                if jobsinfeed == 0:
                                    colsfromfeed = colsfromfeed + "`" + key + "`, "

                        inscols = inscols[:-2]
                        insvals = insvals[:-2]
                        updcolsvals = updcolsvals[:-2]

                        if self.debug and self.debuglevel >= 0:
                            print(inscols)
                            print(insvals)
                            print(updcolsvals)

                        inscols += ", `" + "existinfeed" + "`"
                        insvals += ", '" + "1" + "'"
                        updcolsvals += ", `existinfeed` = '" + "2" + "'"

                        inscols += ", `" + "job_feed_id" + "`"
                        insvals += ", '" + self.jobfeedid + "'"
                        updcolsvals += ", `job_feed_id` = '" + self.jobfeedid + "'"

                        insstatement = "INSERT INTO `" + self.cfg.database + "`.`" + self.tablename + "` (" \
                                       + inscols + ")"
                        insstatement += " VALUES(" + insvals + ")"
                        insstatement += " ON DUPLICATE KEY UPDATE " + updcolsvals + ";"

                        if self.debug and self.debuglevel >= 9:
                            print(insstatement)

                        try:
                            flightdb.execute(insstatement)
                            self.database_check = '<span style=\"color:green;\">Successfull</span>'
                        except pymysql.Error as e:
                            print(e)
                            print(insstatement)
                            self.cfgmain.sendErrorEmail(handler, str(e) + str(insstatement))
                            self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                            return

                        inscols = ''
                        insvals = ''
                        updcolsvals = ''

                        jobsinfeed += 1
                else:
                    print("Something is wrong!")
                    return

        colsfromfeed = colsfromfeed[:-2]

        if self.debug and self.debuglevel >= 0:
            print(colsfromfeed)

        currenttime = datetime.now()
        print(currenttime)

        time1 = currenttime - start

        self.getJobsFiguresFromTables(handler)

        self.processDBJobsTables(handler, colsfromfeed)

        self.getJobsInDB(handler)
        jobsindbafter = self.jobsindb

        currenttime = datetime.now()
        print(currenttime)

        time2 = currenttime - start
        print(time2)

        updatehandlers = "UPDATE `" + self.cfg.database + "`.`handlers` SET status = 1, lastrun = now(), ustatid = ustatid + 1 WHERE jobfeed_id = '" + self.jobfeedid + "';"
        try:
            flightdb.execute(updatehandlers)
        except pymysql.Error as e:
            print(e)
            print(updatehandlers)
            self.cfgmain.sendErrorEmail(handler, str(e) + str(updatehandlers))
            return

        currenttime = datetime.now()
        print(currenttime)

        time = currenttime - start

        print(time)

        if self.debug and self.debuglevel >= 0:
            print("updated " + str(self.updatedjobs))
            print("inserted " + str(self.insertedjobs))
            print("deleted " + str(self.deletedjobs))
            print("after " + str(jobsindbafter))

        selectstmnt = "select f.departureStation, f.arrivalStation, f.departureDates, f.originalPrice_amount as oldprice, f.originalPrice_currencyCode as oldpricecur, ff.originalPrice_amount as newprice, ff.originalPrice_currencyCode as newpricecur, (f.originalPrice_amount - ff.originalPrice_amount) as amt from (select `departureStation`, `arrivalStation`, `departureDate`, `price_amount`, `price_currencyCode`, `originalPrice_amount`, `originalPrice_currencyCode`, `priceType`, `departureDates`, `hasMacFlight` from `" + self.cfg.database + "`.flights_json) f left join (select `departureStation`, `arrivalStation`, `departureDate`, `price_amount`, `price_currencyCode`, `originalPrice_amount`, `originalPrice_currencyCode`, `priceType`, `departureDates`, `hasMacFlight` from `" + self.cfg.database + "`.flights_json_arc where dtstamp = '" + str(self.lastrun) + "') ff on f.departureStation = ff.departureStation and f.arrivalStation = ff.arrivalStation and f.departureDates = ff.departureDates where (f.originalPrice_amount - ff.originalPrice_amount) <> 0;"
        try:
            flightdb.execute(selectstmnt)
            print(flightdb.rowcount)
        except pymysql.Error as e:
            print(e)
            print(selectstmnt)
            self.cfgmain.sendErrorEmail(handler, str(e) + str(selectstmnt))
            return

        self.emailvars['emailbody'] = ""

        for rowret in flightdb.fetchall():
            if self.debug and self.debuglevel >= 0:
                print(rowret)

            stat = ''
            if rowret['amt'] > 0:
                stat = 'Prices going down!'
            else:
                stat = 'Prices going up!'

            self.emailvars['emailbody'] += stat + ' Wizzair alert for flight from ' + rowret['departureStation'] + ' to ' + rowret['arrivalStation'] + ' on ' + str(rowret['departureDates']) + ' old price : ' + str(rowret['oldprice']) + ' ' + str(rowret['oldpricecur']) + ' new price: ' + str(rowret['newprice']) + ' ' + str(rowret['newpricecur']) + ' difference : ' + str(rowret['amt']) + "<br>\n"

        if self.sendemails == 2 and len(self.emailvars['emailbody']) != 0:
            self.emailvars['emailto'] = self.emailsto
            self.emailvars['emailsubject'] = self.emailssubject

            seckey = 'RTJQrp4BKlgs6s7SkSVnDBV5ZavpPGxgyN93Ufpz75KEGDc68s5DtkaJmjJu1SjB'

            url = 'https://vprs.co.uk/vpmain/hfoc.php?DO=' + seckey

            postdata = {
                'jobfeed_id': self.jobfeedid,
                'datefor': datetime.now().strftime("%Y-%m-%d"),
                'hours': datetime.now().strftime("%H:%M:%S"),
                'admemlsubj': self.emailvars['emailsubject'],
                'admemlbody': self.emailvars['emailbody'],
                'admcronjob': '0 0,2,4,6,8,10,12,14,16,18,20,22 * * *'
            }

            print(postdata)

            r = requests.post(url, data=postdata)
            print(r.status_code)
            print(r.content)


            # emlstmnt = "INSERT INTO hfoutcomm (`active`, `jobfeed_id`, `feed_id`, `admsendemails`, `admemailto`, `admemlsubject`, `admemlbody`, `admlastrun`, `admcronjob`, `sendemails`, `emailsto`, `emailssubject`, `emailsbody`, `lastrun`, `cronjob`) VALUES (" + \
            #                                     "'1', '" + self.jobfeedid + "', null, '1', '" + self.emailvars['emailto'] + "', '" + self.emailvars['emailsubject'] + "', '" + self.emailvars['emailbody'] + "', '0 0,2,4,6,8,10,12,14,16,18,20,22 * * *', null, null, null, null, null, null);"
            #
            # try:
            #     flightdb.execute(emlstmnt)
            #     print(flightdb.rowcount)
            # except pymysql.Error as e:
            #     print(e)
            #     self.cfgmain.sendErrorEmail(handler, e)
            #     return

        flightdb.close()

    def importPerSKU(self, handler):
        # self.debug = True
        # self.debuglevel = 0

        updatestatus = 'null'   # '1'
        # updatestatus = '1'

        start = datetime.now()
        print(start)

        self.resetFeedVars()
        self.loadFeedVars(handler)

        if self.feedlocks == 1:
            errormsg = self.jobfeedid + ' Handler locked!!!'
            print(errormsg)
            self.cfgmain.sendErrorEmail(handler, errormsg)
            return

        print('Processing: ' + self.jobfeedid)

        limit = " limit 0, 2"

        try:
            handlersconn = self.myConnectionMain.connection()
            unijsondb = handlersconn.cursor()

            unijsondb.execute('SET NAMES utf8mb4;')
            unijsondb.execute('SET character_set_connection=utf8mb4;')

            getskus = "SELECT products_sku FROM " + self.cfg.database + "." + self.server + " WHERE job_feed_id = '" + self.jobfeedid + "' and active = 1 and status is null" + limit + ";"
            try:
                unijsondb.execute(getskus)
            except pymysql.Error as e:
                print(e)
                print(getskus)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(getskus))
                if self.debug is not True:
                    return

            callurl = self.url

            for rowret in unijsondb.fetchall():
                # if self.debug and self.debuglevel >= 0:
                print(rowret)
                self.url = callurl + rowret['products_sku']
                self.port = rowret['products_sku']
                print(self.url)
                self.processUNIJSONFeed(handler, donotresetvals=True)

                updateskutable = "UPDATE " + self.cfg.database + "." + self.server + " SET status = " + updatestatus + " where job_feed_id = '" + self.jobfeedid + "' and products_sku = '" + rowret['products_sku'] + "';"

                try:
                    unijsondb.execute(updateskutable)
                except pymysql.Error as e:
                    print(e)
                    print(updateskutable)
                    self.cfgmain.sendErrorEmail(handler, str(e) + str(updateskutable))
                    if self.debug is not True:
                        return

        finally:
            handlersconn.close()                                # returns the connection to the pool

    def processUNIJSONFeed(self, handler, donotresetvals=False):
        # self.debug = True
        # self.debuglevel = 0

        start = datetime.now()
        print(start)

        if donotresetvals == False:
            self.resetFeedVars()
            self.loadFeedVars(handler)

        if self.feedlocks == 1:
            errormsg = self.jobfeedid + ' Handler locked!!!'
            print(errormsg)
            self.cfgmain.sendErrorEmail(handler, errormsg)
            return

        print('Processing: ' + self.jobfeedid)

        if donotresetvals == False:
            self.updJobsTable(handler)

        try:
            handlersconn = self.myConnectionMain.connection()
            unijsondb = handlersconn.cursor()

            unijsondb.execute('SET NAMES utf8mb4;')
            unijsondb.execute('SET character_set_connection=utf8mb4;')

            self.getJobsInDB(handler)
            jobsindb = self.jobsindb

            self.getTableColsTypes(handler)

            retrows = 0
            gettablesexist = "SELECT table_name FROM information_schema.tables WHERE table_schema = '" + self.cfg.database + "' and table_name in ('peoplefluent_map', 'peoplefluent_countrymap', 'peoplefluent_citymap', 'peoplefluent_tagmap');"
            try:
                unijsondb.execute(gettablesexist)
                retrows = unijsondb.rowcount
            except pymysql.Error as e:
                print(e)
                print(gettablesexist)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(gettablesexist))
                if self.debug is not True:
                    return
        finally:
            handlersconn.close()                                # returns the connection to the pool

        if self.debug and self.debuglevel >= 0:
            print(self.url)
        url = urlparse(self.url)
        if self.debug and self.debuglevel >= 0:
            print(url)
        self.mainurl = url[0] + "://" + url[1] + url[2] + "/"
        self.mainurladd = url[0] + "://" + url[1]
        print(self.mainurladd)

        if self.server is not None and self.server != '' and 'http' in self.server:
            self.mainurl = self.server

        if self.debug and self.debuglevel >= 0:
            print(self.mainurl)

        page = ''

        if self.headers is not None and self.headers != '':
            self.requestHeader = self.getHeaders(self.headers)

            if self.debug and self.debuglevel >= 9:
                print(self.url)
                print(self.requestHeader)
        else:
            self.requestHeader = {}

        rr = ''
        jsr = {}

        try:
            print("Starting...")

            if self.conntype == "web" and self.feedtype == 'json-icims':
                # headers = HTTPBasicAuth(self.feeduser, self.feedpass)
                # headers = {'Authorization': basic_auth(self.feeduser, self.feedpass)}
                # headers = {'Authorization': 'Basic %s' % base64.b64encode(self.feeduser + ":" + self.feedpass)}
                # print(headers)

                # header = {
                #     'Content-Type': 'application/json',
                #     'Authorization': 'Basic ' + str(base64.b64encode((self.feeduser + ":" + self.feedpass).encode("ascii")))[2:-1]
                # }
                #
                # print(header)

                # r = requests.get(self.url, auth=(self.feeduser, self.feedpass))
                # r = requests.get(self.url, headers=header)
                #
                # print(sys.version)
                #
                # print(r.content)
                # print(r.status_code)

                session = requests.Session()
                session.auth = (self.feeduser, self.feedpass)

                # session.post(self.url)
                r = session.get(self.url)

                page = r.content

                if self.debug and self.debuglevel >= 0:
                    print(page)

            elif self.conntype == "web" and self.feedtype == 'json-ikea':
                data = {
                    'client_id': self.feeduser,
                    'client_secret': self.feedpass,
                    'scope': 'https://api.prod.ingka.com/.default',
                    'grant_type': 'client_credentials',
                    'content-type': 'application/x-www-form-urlencoded'
                }

                r = requests.get(self.server, headers=self.requestHeader, data=data)
                if self.debug and self.debuglevel >= 0:
                    print(r.status_code)
                    print(r.content)

                js = json.loads(r.content)
                if self.debug and self.debuglevel >= 0:
                    print(js['access_token'])

                headers2 = {
                    'Content-Type': 'application/json',
                    'X-Client-Id': self.feeduser,
                    'Authorization': 'Bearer ' + js['access_token']
                }

                rr = requests.get(self.url, headers=headers2)
                if self.debug and self.debuglevel >= 0:
                    print(rr.status_code)
                    print(rr.content)

                page = rr.content
            elif self.conntype == "bearer" and self.feedtype == 'call-json':
                if self.upload == 1:
                    callurl = self.server + '&' + self.feeduser + '&' + self.feedpass
                    if self.debug and self.debuglevel >= 0:
                        print(callurl)
                    rp = requests.post(callurl)

                    if self.debug and self.debuglevel >= 0:
                        print(rp.status_code)
                        print(rp.content)

                    js = json.loads(rp.content)

                    if self.debug and self.debuglevel >= 0:
                        print(js)
                        print(js['access_token'])

                    if self.debug and self.debuglevel >= 0:
                        print(self.headers)
                    self.requestHeader = self.getHeaders(self.headers, token=js['access_token'])
                    if self.debug and self.debuglevel >= 0:
                        print(self.requestHeader)
                        print(self.reppath)

                    rr = requests.get(self.reppath, headers=self.requestHeader)

                    if self.debug and self.debuglevel >= 0:
                        print(rr.status_code)
                        print(rr.content)

                    jsr = json.loads(rr.content)

                    if self.debug and self.debuglevel >= -1:
                        print(jsr)
                        print(len(jsr['results']))
                        print(jsr['results'])
                        print(jsr['Content']['StatusCode'])

            elif self.conntype == "web":
                if self.requestHeader is not None and self.requestHeader != '':
                    r = requests.get(self.url, headers=self.requestHeader)
                else:
                    r = requests.get(self.url)

                page = r.content.decode(r.encoding)

                # print(page)

                # ff = open('productExport', 'wb')
                # ff.write(page)
                # ff.close()

                if self.debug and self.debuglevel >= 10:
                    print(page)
            elif self.conntype == "file":
                # print(os.path.dirname(os.path.abspath(__file__)))
                # print(os.path.abspath(os.getcwd()))
                # print(os.path.dirname(os.path.realpath(__file__)))
                if os.path.isfile(self.server):
                    page = ""
                    # print("File found!")
                    # f = open(self.server, 'rb')
                    # page = f.read()
                    # f.close()
            elif self.conntype == "ijson":
                if os.path.exists(self.server):
                    os.remove(self.server)

                # os.system("/usr/bin/wget -c --read-timeout=300 --tries=0 " + self.url)
                print("Downloading " + self.url + "...")
                os.system("wget -q -c --read-timeout=300 --tries=0 " + self.url)

                # print(os.getcwd())

                if os.path.exists(self.server):
                    print("file " + str(self.server) + " with " + str(os.stat(self.server).st_size) + " downloaded and exists in the current location -> " + str(os.getcwd()))
                else:
                    iReTries = 0
                    while os.path.exists(self.server) != True and iReTries < 3:
                        print("Retrying download " + str(iReTries+1) + "...")
                        os.system("wget -q -c --read-timeout=300 --tries=0 " + self.url)
                        iReTries = iReTries + 1
                    if os.path.exists(self.server):
                        print("file " + str(self.server) + " with " + str(os.stat(self.server).st_size) + " downloaded after " + str(iReTries+1) + " retries and exists in the current location -> " + str(os.getcwd()))
                    else:
                        print("file "+ str(self.server) + " cannot be downloaded!!!")
                        return
            if self.debug and self.debuglevel >= 10:
                print(page)
        except Exception as e:
            print(e)

        self.insvals = ''
        self.inscols = ''
        self.updcolsvals = ''

        self.insvalscp = ''
        self.inscolscp = ''
        self.updcolsvalscp = ''

        self.colsfromfeed = ''
        self.error = ''
        jobsinfeed = 0
        itemcode = ''

        # print(page)

        self.rss_check = '<span style="color:green;">Successful run for handler ' + self.jobfeedid + '</span>'
        try:
            if self.conntype == "ijson" or self.conntype == "file":
                root = ""
            else:
                root = json.loads("{\"0\":" + page + "}")
        except json.JSONDecodeError as e:
            print(e)
            self.cfgmain.sendErrorEmail(handler, e)
            return

        jobsinfeed += self.prUNIJSONprocessPage(root, handler)

        self.colsfromfeed = self.colsfromfeed[:-2]

        if self.debug and self.debuglevel >= 0:
            print(self.colsfromfeed)

        currenttime = datetime.now()
        print(currenttime)

        time1 = currenttime - start

        self.getJobsFiguresFromTables(handler)

        self.processDBJobsTables(handler, self.colsfromfeed, ', `postcode`, `ctown`, `county`, `country`')

        self.getJobsInDB(handler)
        jobsindbafter = self.jobsindb

        currenttime = datetime.now()
        print(currenttime)

        # time2 = currenttime - start

        try:
            handlersconn = self.myConnectionMain.connection()
            unijsondb = handlersconn.cursor()

            unijsondb.execute('SET NAMES utf8mb4;')
            unijsondb.execute('SET character_set_connection=utf8mb4;')

            updatehandlers = "UPDATE `" + self.cfg.database + "`.`handlers` SET status = 1, lastrun = now(), ustatid = ustatid + 1 WHERE jobfeed_id = '" + self.jobfeedid + "';"
            try:
                unijsondb.execute(updatehandlers)
            except pymysql.Error as e:
                print(e)
                print(updatehandlers)
                self.cfgmain.sendErrorEmail(handler, str(e) + str(updatehandlers))
                return
        finally:
            handlersconn.close()                                # returns the connection to the pool

        currenttime = datetime.now()
        print(currenttime)

        time = currenttime - start

        print(currenttime - start)

        if self.debug and self.debuglevel >= 9:
            print("updated " + str(self.updatedjobs))
            print("inserted " + str(self.insertedjobs))
            print("deleted " + str(self.deletedjobs))
            print("after " + str(jobsindbafter))

        self.emailvars['rss_check'] = self.rss_check
        self.emailvars['database_check'] = self.database_check
        self.emailvars['jobsindbinit'] = jobsindb
        self.emailvars['jobsinfeed'] = jobsinfeed
        self.emailvars['jobsupdated'] = self.updatedjobs
        self.emailvars['jobsinserted'] = self.insertedjobs
        self.emailvars['jobsdeleted'] = self.deletedjobs
        self.emailvars['jobsindb'] = jobsindbafter
        self.emailvars['time1step'] = time1
        self.emailvars['time2step'] = time
        self.emailvars['time3end'] = time

        self.cfg.sendEmail(handler, self.emailvars)

        if self.conntype == "ijson" and os.path.exists(self.server):
            os.remove(self.server)

    def prUNIJSONprocessPage(self, root, handler, itemcode='', maparrpf={}, countrymaparrpf={}, citymaparrpf={}, tagmaparr = {}):
        # self.debug = True
        # self.debuglevel = 0

        pull_images = 0

        jobsinfeed = 0
        duplicatejob = False
        jobtagid = ""
        jobLocationTextNone = False
        locale = ''

        if self.conntype == "ijson" or self.conntype == "file":
            engine = sqlalchemy.create_engine(self.cfg.sqlalchemyconnstr, future=True)

            iCntAttr = 0

            if self.debug and self.debuglevel >= 10:
                fout = open("borotrade_attr_output.txt", "wb")
                foutins = open("borotrade_attr_output_ins.txt", "wb")

            # if os.path.exists(self.server):
            #     print("File exists!")

            with open(self.server, "rb") as f:
            # with (open(self.server, "r", encoding='utf-8') as f):
                for root in ijson.items(f, ""):
                    for i in range(len(root)):
                        self.shortcode = ''
                        productsid = ''
                        productssku = ''
                        gallery = ''
                        addtoshortdescr = '<div class="products_descr2">'
                        try:
                            job = root[i]
                        except Exception as e:
                            print(e)
                            job = root

                        for key, value in job.items():
                            if self.debug and self.debuglevel >= 10:
                                print(key)
                                print(value)

                            if value is not None:
                                # if "" in value:
                                #     print(value)
                                if type(value) is not dict and type(value) is not list:
                                    if "&nbsp;" in value:
                                        # value = value.replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("&nbsp;", " ").replace("\t", "").replace("\n", "").replace("\r", "").replace("\\r", " ")
                                        value = value.replace("&nbsp;", " ")

                            if key == 'products_sku':
                                productssku = value.strip()

                            if key == 'products_id':
                                productsid = value.strip()

                            # if productssku == '29971110':
                            #     print("products_sku -> 29971110")
                            #     print(str(key) + " -> " + str(value))

                            if key in self.dtarr:
                                try:
                                    value = "'" + str(datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")) + "'"
                                except Exception as e:
                                    # print(e)
                                    value = 'null'
                            elif key in self.boolarr:
                                value = value
                            elif type(value) is dict:
                                # print("dict -> " + str(value))
                                if 'jobDetails' in value:
                                    if 'href' in value['jobDetails']:
                                        if key == self.seccallcols:
                                            self.shortcode = str(value['jobDetails']['href'])
                                        value = "'" + str(value['jobDetails']['href']) + "'"
                                    else:
                                        value = "'" + "'"
                                elif key == "job" or key == "location":
                                    for key1, value1 in value.items():
                                        # print(key1)
                                        # print(value1)
                                        if type(value1) is dict:
                                            for key2, value2 in value1.items():
                                                self.inscols += "`" + key + "_" + key1 + "_" + key2 + "`, "
                                                self.insvals += "'" + str(value2) + "', "
                                                self.updcolsvals += "`" + key + "_" + key1 + "_" + key2 + "` = '" + str(value2) + "', "

                                                if jobsinfeed == 0:
                                                    self.colsfromfeed = self.colsfromfeed + "`" + key + "_" + key1 + "_" + key2 + "`, "
                                        else:
                                            self.inscols += "`" + key + "_" + key1 + "`, "
                                            self.insvals += "'" + str(value1) + "', "
                                            self.updcolsvals += "`" + key + "_" + key1 + "` = '" + str(value1) + "', "

                                            if jobsinfeed == 0:
                                                self.colsfromfeed = self.colsfromfeed + "`" + key + "_" + key1 + "`, "
                                else:
                                    value = "'" + "'"
                            elif type(value) is list:
                                # print("list -> " + str(value))
                                # print(value)
                                if key == 'gallery':
                                    # print(value)
                                    gallery = value
                                    # value = "'" + "'"
                                    value = "'" + self.cfgmain.escape_data(str(value).replace('\n', '').replace("  ", " ").replace("&nbsp;", " ")) + "'"

                                    # self.inscols += "`" + key + "`, "
                                    # self.insvals += "'" + str(value) + "', "
                                    # self.updcolsvals += "`" + key + "` = '" + str(value) + "', "
                                else:
                                    value = "'" + "'"
                            else:
                                if value is None:
                                    value = 'null'
                                else:
                                    value = value

                            if key == "products_descr3" or key == "products_descr4" or key == "products_descr5":
                                souptab1 = BeautifulSoup(value, "html.parser")
                                for el1 in souptab1:
                                    if len(str(el1.text).strip().replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("\\r", " ")) > 3:
                                        # print(el1)
                                        # print(str(el1.text).strip().replace("\\r", " "))
                                        if str.isdigit(str(el1.text).strip().replace("  ", "").replace("    ", "").replace("   ", "").replace("  ", "").replace("\\r", "").replace(";", "")):
                                            # print("String is numeric " + str(el1.text).strip().replace("\\r", " ").replace(";", ""))
                                            linkedparr = str(el1.text).strip().replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("\\r", " ").split(";")
                                            for itemstd in linkedparr:
                                                text2insert = str(itemstd).replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("\\r", " ").strip()
                                                # print(text2insert)

                                                if len(text2insert) != 0:
                                                    inslinkedptable = "INSERT INTO `" + self.cfg.database + "`.`borotrade_linkedp` "
                                                    inslinkedpvals = ''
                                                    inslinkedpstatement = inslinkedptable + "(`products_id`, `products_sku`, `linkedp`) VALUES "
                                                    updlinkedpvals = ''

                                                    inslinkedpvals = inslinkedpvals + "(" + self.cfgmain.escape_data(str(productsid).replace('\n', '')) + ", '" + self.cfgmain.escape_data(str(productssku).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(text2insert)) + "')"
                                                    updlinkedpvals = updlinkedpvals + "`products_id` = " + self.cfgmain.escape_data(str(productsid).replace('\n', '')) + ", `products_sku` = '" + self.cfgmain.escape_data(str(productssku).replace('\n', '')) + "', `linkedp` = '" + self.cfgmain.escape_data(str(text2insert)) + "'"

                                                    inslinkedpstatement = inslinkedpstatement + inslinkedpvals + " ON DUPLICATE KEY UPDATE " + updlinkedpvals + ";"
                                                    # print(inslinkedpstatement)

                                                    try:
                                                        handlersconn = self.myConnectionMain.connection()
                                                        unijsondb = handlersconn.cursor()

                                                        unijsondb.execute('SET NAMES utf8mb4;')
                                                        unijsondb.execute('SET character_set_connection=utf8mb4;')

                                                        try:
                                                            unijsondb.execute(inslinkedpstatement)
                                                        except pymysql.Error as e:
                                                            print(e)
                                                            print(inslinkedpstatement)
                                                            self.cfgmain.sendErrorEmail(handler, str(e) + str(inslinkedpstatement))
                                                    finally:
                                                        handlersconn.close()  # returns the connection to the pool
                                        else:
                                            addtoshortdescr = addtoshortdescr + str(el1).replace("  ", " ").replace("  ", " ").replace("\\r", "").replace("  ", " ").strip()

                            if key == "products_descr2":
                                # print(value)
                                # print(productsid)
                                # print(productssku)

                                # if productssku == '29971110':
                                #     print("products_sku -> 29971110")
                                #     print(value)

                                souptab = BeautifulSoup(value, "html.parser")
                                itablecnt = 0
                                # foundspecinhtml = False
                                whichtabletoget = 0
                                foundotherthantable = False
                                # if productssku == '29971110':
                                #     print(souptab.select_one("table"))
                                iAttrCntPerProduct = 0

                                firsttable = souptab.select_one("table")
                                if firsttable is not None and len(str(firsttable).strip()) != 0 and (len(firsttable.find_all("tr")[0].find_all("td")) == 2 or len(firsttable.find_all("tr")[1].find_all("td")) == 2):
                                    # print(firsttable)
                                    # print(firsttable.find_all("tr"))

                                    for el1 in firsttable.find_all("tr"):
                                        if len(el1.find_all("td")) == 2:
                                            insattrtable = "INSERT INTO `" + self.cfg.database + "`.`borotrade_attr` "
                                            insattrvals = ''
                                            insattrstatement = insattrtable + "(`products_id`, `products_sku`, `icnt`, `attr`, `val`) VALUES "
                                            updattrvals = ''
                                            insattrvals = insattrvals + "(" + self.cfgmain.escape_data(
                                                str(productsid).replace('\n', '')) + ", '" + self.cfgmain.escape_data(
                                                str(productssku).replace('\n', '')) + "', " + str(iAttrCntPerProduct)
                                            updattrvals = updattrvals + "`products_id` = " + self.cfgmain.escape_data(
                                                str(productsid).replace('\n',
                                                                        '')) + ", `products_sku` = '" + self.cfgmain.escape_data(
                                                str(productssku).replace('\n', '')) + "', `icnt` = " + str(
                                                iAttrCntPerProduct)
                                            itdcnt = 0
                                            colname = ''
                                            for itemstd in el1.find_all("td"):
                                                text2insert = itemstd.text

                                                convertedtext = itemstd.text

                                                convertedtext = convertedtext.replace("\r\n", "")
                                                convertedtext = convertedtext.replace("\n", "")
                                                convertedtext = convertedtext.replace("  ", " ")
                                                convertedtext = convertedtext.strip()
                                                # convertedtext = convertedtext.encode("utf-8").decode("utf-8")
                                                # if self.cfgmain.escape_data(str(convertedtext))[0:1] == "b":
                                                #     print("starting with 'b' -> " + convertedtext)
                                                # convertedtext = self.cfgmain.escape_data(convertedtext)

                                                if self.debug and self.debuglevel >= 10:
                                                    writetofile = self.cfgmain.escape_data(
                                                        str(productsid).replace('\n', '')) + "|" + self.cfgmain.escape_data(
                                                        str(productssku).replace('\n', '')) + "|" + convertedtext + "\n"
                                                    fout.write(writetofile.encode("utf-8"))

                                                text2insert = convertedtext

                                                if itdcnt == 0:
                                                    colname = 'attr'
                                                elif itdcnt == 1:
                                                    colname = 'val'

                                                # print(text2insert)
                                                insattrvals = insattrvals + ", '" + self.cfgmain.escape_data(
                                                    str(text2insert)) + "'"
                                                updattrvals = updattrvals + ", `" + colname + "` = '" + self.cfgmain.escape_data(
                                                    str(text2insert)) + "'"
                                                itdcnt += 1
                                            insattrvals = insattrvals + ")"
                                            insattrstatement = insattrstatement + insattrvals + " ON DUPLICATE KEY UPDATE " + updattrvals + ";"

                                            try:
                                                handlersconn = self.myConnectionMain.connection()
                                                unijsondb = handlersconn.cursor()

                                                unijsondb.execute('SET NAMES utf8mb4;')
                                                unijsondb.execute('SET character_set_connection=utf8mb4;')

                                                if self.debug and self.debuglevel >= 10:
                                                    foutins.write((insattrstatement + "\n").encode("utf-8"))

                                                try:
                                                    unijsondb.execute(insattrstatement)
                                                except pymysql.Error as e:
                                                    print(e)
                                                    print(insattrstatement)
                                                    print(firsttable)
                                                    self.cfgmain.sendErrorEmail(handler, str(e) + str(insattrstatement))
                                            finally:
                                                handlersconn.close()  # returns the connection to the pool

                                            iAttrCntPerProduct = iAttrCntPerProduct + 1

                                    # if len(str(el.text).strip().replace("\\r", " ")) > 3:
                                    #     # print(el)
                                    #     itrcnt = 0
                                    #     iAttrCntPerProduct = 0
                                    #
                                    #     # if productssku == '26331040' or productssku == '12696400':
                                    #     #     print(productsid)
                                    #     #     print(productssku)
                                    #     #     print(str(el))
                                    #
                                    #     # if productssku == '29971110':
                                    #     #     print(itrcnt)
                                    #
                                    #     if "<table" not in str(value):
                                    #         # if productssku == '29971110':
                                    #         #     print("no <table found! el -> " + str(el))
                                    #         #     print(foundotherthantable)
                                    #         if ("<p" in str(el) or "<h3" in str(el)) and ("СПЕЦИФИКАЦИИ" in str(el.text).replace("\\r", " ").strip() or "СПЕЦИФИКАЦИИ:" in str(el.text).replace("\\r", " ").strip() or "Технически данни" in str(el.text).replace("\\r", " ").strip() or "Технически данни:" in str(el.text).replace("\\r", " ").strip() or "ТЕХНИЧЕСКИ ПАРАМЕТРИ" in str(el.text).replace("\\r", " ").strip() or "Технически параметри:" in str(el.text).replace("\\r", " ").strip() or "Технически характеристики:" in str(el.text).replace("\\r", " ").strip() or "Технически данни" in str(el.text).replace("\\r", " ").strip() or "Технически данни:" in str(el.text).replace("\\r", " ").strip() or "Технически параметри" in str(el.text).replace("\\r", " ").strip()):
                                    #             foundotherthantable = False
                                    #         else:
                                    #             foundotherthantable = True
                                    #             addtoshortdescr = addtoshortdescr + str(el).replace("  ", " ").replace("  ", " ").replace("\\r", "").replace("  ", " ").strip()
                                    #         # print(str(el)[0:5] + " -> " + str(el.text).replace("\\r", " ").strip())
                                    #     else:
                                    #         # if productssku == '29971110':
                                    #         #     print("table found! el -> " + str(el))
                                    #         #     print(foundotherthantable)
                                    #         #     print(itrcnt)
                                    #         #     print(foundotherthantable)
                                    #         if itrcnt == 0 and foundotherthantable == False:
                                    #         # if foundotherthantable == False:
                                    #             # try:
                                    #             #     print(el.find_all("table"))
                                    #             # except Exception as e:
                                    #             #     print(e)
                                    #             for el1 in el.find_all("tr"):
                                    #                 if len(str(el1.text).strip()) != 0 and len(el.find_all("tr")[0].find_all("td")) == 2:
                                    #                     # if productssku == '41110360':
                                    #                     #     print(el)
                                    #                     #     print(el1)
                                    #                     insattrtable = "INSERT INTO `" + self.cfg.database + "`.`borotrade_attr` "
                                    #                     insattrvals = ''
                                    #                     insattrstatement = insattrtable + "(`products_id`, `products_sku`, `icnt`, `attr`, `val`) VALUES "
                                    #                     updattrvals = ''
                                    #                     insattrvals = insattrvals + "(" + self.cfgmain.escape_data(str(productsid).replace('\n','')) + ", '" + self.cfgmain.escape_data(str(productssku).replace('\n','')) + "', " + str(iAttrCntPerProduct)
                                    #                     updattrvals = updattrvals + "`products_id` = " + self.cfgmain.escape_data(str(productsid).replace('\n','')) + ", `products_sku` = '" + self.cfgmain.escape_data(str(productssku).replace('\n','')) + "', `icnt` = " + str(iAttrCntPerProduct)
                                    #                     itdcnt = 0
                                    #                     colname = ''
                                    #                     for itemstd in el1.find_all("td"):

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#                                                             text2insert = itemstd.text
#
#                                                             # if isinstance(text2insert, str):
#                                                             #     # text2insert = text2insert
#                                                             #     # print(text2insert)
#                                                             #     if text2insert[0:1] == " ":
#                                                             #         print("starting with ' ' -> " + text2insert)
#                                                             #     if text2insert[0:1] == "\\":
#                                                             #         print("starting with '\\' -> " + text2insert)
#                                                             # else:
#                                                             #     print("not string!!!")
#                                                             #
#                                                             # if isinstance(itemstd.text, bytes):
#                                                             #     print("Bytes -> " + str(itemstd.text))
#
#                                                             convertedtext = itemstd.text
#
#                                                             convertedtext = convertedtext.replace("\r\n", "")
#                                                             convertedtext = convertedtext.replace("\n", "")
#                                                             convertedtext = convertedtext.replace("  ", " ")
#                                                             convertedtext = convertedtext.strip()
#                                                             # convertedtext = convertedtext.encode("utf-8").decode("utf-8")
#                                                             # if self.cfgmain.escape_data(str(convertedtext))[0:1] == "b":
#                                                             #     print("starting with 'b' -> " + convertedtext)
#                                                             # convertedtext = self.cfgmain.escape_data(convertedtext)
#
#                                                             if self.debug and self.debuglevel >= 10:
#                                                                 writetofile = self.cfgmain.escape_data(str(productsid).replace('\n','')) + "|" + self.cfgmain.escape_data(str(productssku).replace('\n','')) + "|" + convertedtext + "\n"
#                                                                 fout.write(writetofile.encode("utf-8"))
#
#                                                             text2insert = convertedtext
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

                                                            # removecharsarr = [u"\u0020", u"\u00A0", u"\u2000", u"\u2001", u"\u2002", u"\u2003", u"\u2004", u"\u2005", u"\u2006", u"\u2007", u"\u2008", u"\u2009", u"\u200A", u"\u202F", u"\u3000", u"\u200B", u"\u200C", u"\u200D", u"\u2060", u"\uFEFF", u"\u00AD", u"\u2028", u"\u2029"]
                                                            #
                                                            # try:
                                                            #     text2insert = itemstd.text
                                                            #     text2insert = text2insert.replace("\\r", "")
                                                            #     text2insert = text2insert.replace("  ", " ")
                                                            #     for unichr in removecharsarr:
                                                            #         text2insert = text2insert.replace(unichr, " ")
                                                            #     text2insert = text2insert.strip()
                                                            #     text2insert.encode("utf-8") #.decode("utf-8")
                                                            #
                                                            #     text2insert = re.sub(r'[^α-ωΑ-Ωа-яА-Яa-zA-Z0-9.,()µØ~=*×<>%–\-!+:;І/”″"\'²³°º\s]', '', text2insert)
                                                            #     control_chars = ''.join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))
                                                            #     control_char_re = re.compile('[%s]' % re.escape(control_chars))
                                                            #     text2insert = control_char_re.sub('', text2insert)
                                                            #     text2insert = text2insert.replace('\\r', '')
                                                            #     text2insert = text2insert.replace('\r', '')
                                                            #     text2insert = text2insert.replace("\\r", "")
                                                            #     text2insert = text2insert.replace("\r", "")
                                                            #
                                                            # except UnicodeEncodeError as e:
                                                            #     print(e)
                                                            #     print(itemstd.text)
                                                            #     print(text2insert)

                                                            # if isinstance(text2insert, str):
                                                            #     print("ordinary string -> " + str(text2insert))
                                                            # elif isinstance(text2insert, bytes):
                                                            #     print("bytes string -> " + str(text2insert))
                                                            # else:
                                                            #     print("not a string")

                                                            # if isinstance(itemstd.text, str):
                                                            #     print("ordinary string -> " + str(itemstd.text))
                                                            # elif isinstance(itemstd.text, unicode):
                                                            #     print("unicode string -> " + str(itemstd.text))
                                                            # else:
                                                            #     print("not a string")
                                                            #
                                                            # text2insert = str(itemstd.text)
                                                            # text2insert = text2insert.replace('\\r', '').replace('  ', ' ')
                                                            # # 'Широчина  на обръщане на пътеката (мм)'
                                                            #
                                                            # print("replaced -> " + str(text2insert))
                                                            # text2insert = itemstd.text.encode('utf-8', 'ignore').decode('utf-8','ignore').encode("utf-8") # .replace(u"\u00A0", u" ").replace(u"  ", u" ").replace(u"  ", u" ").replace(u"  ", u" ").replace(u"  ", u" ")
                                                            # text2insert = text2insert.replace(b"00A0", b" ")
                                                            # text2insert = text2insert.decode('utf-8', 'ignore')
                                                            # text2insert = text2insert.replace("\\r", "")
                                                            # text2insert = text2insert.replace("\r", "")
                                                            # text2insert = text2insert.decode('utf-8','ignore')
                                                            # text2insert = re.sub(r'[\x00-\x1F\x7F\u2000-\u200F\uFEFF]', '', itemstd.text)
                                                            # control_chars = ''.join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7f, 0xa0))))
                                                            # control_char_re = re.compile('[%s]' % re.escape(control_chars))
                                                            # text2insert = control_char_re.sub('', text2insert)
                                                            # text2insert = text2insert.replace("\r", "")
                                                            # text2insert = str(itemstd.text).replace("mbar/ kPa", "mbar/kPa").replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("\\r", " ").replace("\t", "").replace("&nbsp;", " ").strip()
                                                            # text2insert = text2insert.strip().replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
                                                            #
                                                            # text2insert = text2insert.strip().replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")

                                                            # text2insert = ''.join(char for char in itemstd.text if char.isprintable() or char.isspace())

                                                            # if "Вакуум" in text2insert:
                                                            #     text2insert = "Вакуум (mbar/kPa)"
                                                            #
                                                                # print(text2insert)

                                                        #     if itdcnt == 0:
                                                        #         colname = 'attr'
                                                        #     elif itdcnt == 1:
                                                        #         colname = 'val'
                                                        #
                                                        #     # print(text2insert)
                                                        #     insattrvals = insattrvals + ", '" + self.cfgmain.escape_data(str(text2insert)) + "'"
                                                        #     updattrvals = updattrvals + ", `" + colname + "` = '" + self.cfgmain.escape_data(str(text2insert)) + "'"
                                                        #     itdcnt += 1
                                                        # insattrvals = insattrvals + ")"
                                                        # insattrstatement = insattrstatement + insattrvals + " ON DUPLICATE KEY UPDATE " + updattrvals + ";"

                                                        # print(insattrstatement)

                                            #             try:
                                            #                 handlersconn = self.myConnectionMain.connection()
                                            #                 unijsondb = handlersconn.cursor()
                                            #
                                            #                 unijsondb.execute('SET NAMES utf8mb4;')
                                            #                 unijsondb.execute('SET character_set_connection=utf8mb4;')
                                            #
                                            #                 if self.debug and self.debuglevel >= 10:
                                            #                     foutins.write((insattrstatement + "\n").encode("utf-8"))
                                            #
                                            #                 try:
                                            #                     unijsondb.execute(insattrstatement)
                                            #                 except pymysql.Error as e:
                                            #                     print(e)
                                            #                     print(insattrstatement)
                                            #                     # print(str(value))
                                            #                     self.cfgmain.sendErrorEmail(handler, str(e) + str(insattrstatement))
                                            #             finally:
                                            #                 handlersconn.close()  # returns the connection to the pool
                                            #
                                            #             iCntAttr = iCntAttr + 1
                                            #             iAttrCntPerProduct = iAttrCntPerProduct + 1
                                            #         else:
                                            #             addtoshortdescr = addtoshortdescr + str(el).replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("\\r", "").replace("  ", " ").strip()
                                            #         #   add to products_descr_short!
                                            #         #     if len(str(el1.text).replace("\\r", "").strip()) != 0:
                                            #         #         print(productsid)
                                            #         #         print(productssku)
                                            #         #         print("Table 0 not with 2 cols!!!")
                                            #         #         print(el)
                                            # elif itrcnt == 0 and foundotherthantable:
                                            #     #   add to products_descr_short!
                                            #     addtoshortdescr = addtoshortdescr + str(el).replace("  ", " ").replace("    ", " ").replace("   ", " ").replace("  ", " ").replace("\\r", "").replace("  ", " ").strip()
                                            #     # continue
                                            #     # print(productsid)
                                            #     # print(productssku)
                                            #     # print(len(el.find_all("tr")[0].find_all("td")))
                                            #     # print(str(el.text).replace("\\r", "").strip())
                                            # # else:
                                            # #     print(str(el.text).replace("\\r", "").strip())
                                            #
                                            # itrcnt += 1

                            if key == "products_descr_short":
                                if "karcher-borotrade.com" in value or "kaercher-media.com" in value or "data:" in value:
                                    # print(key)
                                    # print(value)
                                    value = value.replace("&nbsp;", " ")

                                    soup = BeautifulSoup(value, "html.parser")
                                    for img in soup.find_all('img'):
                                        if self.debug and self.debuglevel >= 10:
                                            print(img.tag)
                                            print(img.text)
                                            print(img.contents)
                                            print(img.attrs)

                                        img_url = img['src'].replace('\\"', "")

                                        if img_url[0:5] == "data:":
                                            # print(productssku + " -> " + str(img_url[img_url.find(",")+1:][0:20]))
                                            # print(hashlib.sha1(str(img_url[img_url.find(",")+1:]).encode("utf-8")).hexdigest())
                                            imgreqfnameupdtran = str(hashlib.sha1(str(img_url[img_url.find(",")+1:]).encode("utf-8")).hexdigest()) + ".png"
                                            imgreqfnameupdnewweb = self.cfgmain.websitedesc + self.cfgmain.imgpathdbdesc + imgreqfnameupdtran
                                            imgreqfnameupdpath = self.cfgmain.imgpathdbdesc + imgreqfnameupdtran

                                            imgreqcontent = base64.decodebytes(str(img_url[img_url.find(",")+1:]).encode("utf-8"))
                                            imgreqcontentlen = len(base64.decodebytes(str(img_url[img_url.find(",")+1:]).encode("utf-8")))

                                            if os.path.exists(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran):
                                                if int(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size) != int(imgreqcontentlen):
                                                    print("file already exists with DIFFERENT size!!! " + str(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran) + " web -> " + str(int(imgreqcontentlen)) + " local -> " + str(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size))
                                                    os.remove(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran)

                                                    fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran, "wb")
                                                    fimg.write(imgreqcontent)
                                                    fimg.close()
                                            else:
                                                fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran, "wb")
                                                fimg.write(imgreqcontent)
                                                fimg.close()

                                        else:
                                            try:
                                                adomain = urllib.parse.urlparse(img_url)  # noqa: F821
                                            except Exception as e:
                                                adomain = urlparse(img_url)
                                                if self.debug and self.debuglevel >= 10:
                                                    print(e)

                                            try:
                                                imgreqfilename = adomain.path.split('/')[len(adomain.path.split('/'))-1]
                                                imgreqfilenameupd = adomain.path[4:].replace("/", "_")
                                                imgreqfnameupdtran = slugify.slugify(imgreqfilenameupd, separator='_', regex_pattern=r'[^-a-z0-9._]+')
                                                imgreqfnameupdnewweb = self.cfgmain.websitedesc + self.cfgmain.imgpathdbdesc + imgreqfnameupdtran
                                                imgreqfnameupdpath = self.cfgmain.imgpathdbdesc + imgreqfnameupdtran
                                            except Exception as e:
                                                print(e)
                                                print(img_url)
                                                print(adomain)

                                            imgreqcontent = ""
                                            imgreqcontentlen = ""
                                            try:
                                                imgreq = requests.get(img_url, verify=False)
                                                imgreqcontent = imgreq.content
                                                if 'content-length' in imgreq.headers:
                                                    imgreqcontentlen = imgreq.headers['content-length']
                                                else:
                                                    imgreqcontentlen = len(imgreqcontent)
                                            except requests.RequestException as e:
                                                print(e)
                                                print(img_url)

                                            if isinstance(imgreqcontent, bytes):
                                                if os.path.exists(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran):
                                                    if int(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size) != int(imgreqcontentlen):
                                                        print("file already exists with DIFFERENT size!!! " + str(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran) + " web -> " + str(imgreqcontentlen) + " local -> " + str(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size))
                                                        os.remove(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran)

                                                        fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran, "wb")
                                                        fimg.write(imgreqcontent)
                                                        fimg.close()
                                                else:
                                                    fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran, "wb")
                                                    fimg.write(imgreqcontent)
                                                    fimg.close()
                                            else:
                                                # print("isinstance something else?!")
                                                # print(type(imgreqcontent))
                                                imgreqfnameupdnewweb = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"

                                            # if imgreqcontent == "":
                                            #     data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
                                            # else:
                                            #     data_uri = base64.b64encode(imgreqcontent).decode('utf-8')
                                            # img_tag = 'data:' + str(imgreq.headers['content-type']) + ';base64,{0}'.format(
                                            #     data_uri)
                                            # if img_tag == "data:text/html; charset=UTF-8;base64,":
                                            #     print("img_tag is empty for -> " + str(img_url))
                                        value = value.replace(img_url, imgreqfnameupdnewweb)
                                    # print(value)
                                    for a in soup.find_all('a'):
                                        if self.debug and self.debuglevel >= 10:
                                            print(a.tag)
                                            print(a.text)
                                            print(a.contents)
                                            print(a.attrs)

                                        a_url = a['href'].replace('\\"', "")

                                        try:
                                            adomain = urllib.parse.urlparse(a_url)  # noqa: F821
                                        except Exception as e:
                                            adomain = urlparse(a_url)
                                            if self.debug and self.debuglevel >= 10:
                                                print(e)

                                        try:
                                            areq = requests.get(a_url, verify=False)
                                            atext = a.text
                                            acontent = areq.content
                                        except requests.RequestException as e:
                                            print(e)
                                            print(a_url)

                                        if atext.strip() == "":
                                            areqfilename = domain.path.split('/')[len(domain.path.split('/')) - 1]
                                            areqfilenameupd = domain.path[4:].replace("/", "_")
                                            areqfnameupdtran = slugify.slugify(areqfilenameupd, separator='_', regex_pattern=r'[^-a-z0-9._]+')
                                            atext = areqfnameupdtran

                                        if os.path.exists(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext):
                                            if int(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext).st_size) != int(areq.headers['content-length']):
                                                print("file already exists with DIFFERENT size!!! " + str(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext) + " web -> " + str(areq.headers['content-length']) + " local -> " + str(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext).st_size))
                                                os.remove(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext)

                                                fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext, "wb")
                                                fimg.write(acontent)
                                                fimg.close()
                                        else:
                                            fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext, "wb")
                                            fimg.write(acontent)
                                            fimg.close()

                                        # data_a_uri = base64.b64encode(areq.content).decode('utf-8')
                                        # a_tag = 'data:' + str(areq.headers['content-type']) + ';base64,{0}'.format(data_a_uri)
                                        value = value.replace(a_url, self.cfgmain.websitedesc + self.cfgmain.imgpathdesc + atext)
                                        if self.debug and self.debuglevel >= 10:
                                            print(value)

                            if (key == "job" or key == "location") and (type(value) is dict or type(value) is list):
                                value = value
                            else:
                                if value == 'null':
                                    self.inscols += "`" + key + "`, "
                                    self.insvals += self.cfgmain.escape_data(str(value)) + ", "
                                    self.updcolsvals += "`" + key + "` = " + self.cfgmain.escape_data(str(value)) + ", "
                                else:
                                    self.inscols += "`" + key + "`, "
                                    self.insvals += "'" + self.cfgmain.escape_data(str(value)) + "', "
                                    self.updcolsvals += "`" + key + "` = '" + self.cfgmain.escape_data(str(value)) + "', "
                                # self.insvals += "'" + str(value) + "', "
                                # self.updcolsvals += "`" + key + "` = '" + str(value) + "', "

                            if gallery != '' and productssku != '' and productsid != 0:
                                imgupdnewwebarr = []
                                if gallery is not None and gallery != 'NULL':
                                    for gal_val in gallery:
                                        if len(gal_val) >= (len("http://karcher-borotrade.com/uf/") + 3):
                                            try:
                                                domain = urllib.parse.urlparse(gal_val)  # noqa: F821
                                            except Exception as e:
                                                domain = urlparse(gal_val)
                                                if self.debug and self.debuglevel >= 10:
                                                    print(e)

                                            imgfilename = domain.path.split('/')[len(domain.path.split('/'))-1]
                                            imgfilenameupd = domain.path[4:].replace("/", "_")
                                            imgfnameupdtran = slugify.slugify(imgfilenameupd, separator='_', regex_pattern=r'[^-a-z0-9._]+')
                                            imgfnameupdnewweb = self.cfgmain.website + self.cfgmain.imgpathdb + imgfnameupdtran
                                            imgupdnewwebarr.append(imgfnameupdnewweb)
                                            imgfnameupdpath = self.cfgmain.imgpathdb + imgfnameupdtran

                                            # if "professional_podovi_avtomati_br_30_4_c_ae_br_30_4_c_ae_1.jpg" in imgfilenameupd:
                                            #     print("Found image with _1 at the end -> ")
                                            #     print(imgfilenameupd)
                                            #     print(productssku)
                                            #     print(productsid)
                                            #
                                            if self.debug and self.debuglevel >= 0:
                                                print(domain)
                                                print(domain.scheme)
                                                print(domain.netloc)
                                                print(domain.path)
                                                print(len(domain.path.split('/')))
                                                print(domain.path.split('/'))
                                                print(imgfilename)
                                                print(imgfilenameupd)

                                            insgaltable = "INSERT INTO `" + self.cfg.database + "`.`borotrade_gallery_json` "
                                            insgalvals = ''
                                            insgallerystatement = insgaltable + "(`products_id`, `products_sku`, `gallery`, `updatedurl`, `path`, `datasize`, `dataname`, `datanameupd`, `data`) VALUES "
                                            updgalvals = ''
                                            if self.debug and self.debuglevel >= 10:
                                                print(str(productssku) + " -> " + str(gal_val))

                                            galfilecontent = ''

                                            if pull_images == 1:
                                                rrfile = requests.get(gal_val, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"})
                                                if rrfile.status_code == 200:
                                                # print(rrfile.content)
                                                # print(rrfile.headers['Content-Length'])

                                                    if os.path.exists(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran):
                                                        if int(os.stat(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran).st_size) != int(rrfile.headers['content-length']):
                                                            print("file already exists with DIFFERENT size!!! " + str(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran) + " web -> " + str(rrfile.headers['content-length']) + " local -> " + str(os.stat(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran).st_size))
                                                            os.remove(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran)

                                                            fimg = open(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran, "wb")
                                                            fimg.write(rrfile.content)
                                                            fimg.close()
                                                    else:
                                                        fimg = open(self.cfgmain.websitepath + self.cfgmain.imgpath + imgfnameupdtran, "wb")
                                                        fimg.write(rrfile.content)
                                                        fimg.close()

                                                    galfilecontent = rrfile.content
                                                else:
                                                    print(str(rrfile.status_code) + " response for url -> " + str(gal_val))

                                                insgalvals = insgalvals + "(" + self.cfgmain.escape_data(str(productsid).replace('\n', '')) + ", '" + self.cfgmain.escape_data(str(productssku).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(gal_val).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(imgfnameupdnewweb).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(imgfnameupdpath).replace('\n', '')) + "', " + str(rrfile.headers['Content-Length']) + ", '" + self.cfgmain.escape_data(str(imgfilename).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(imgfilenameupd).replace('\n', '')) + "', :gdatavalue)"
                                                updgalvals = updgalvals + "`products_id` = " + self.cfgmain.escape_data(str(productsid).replace('\n', '')) + ", `products_sku` = '" + self.cfgmain.escape_data(str(productssku).replace('\n', '')) + "', `gallery` = '" + self.cfgmain.escape_data(str(gal_val).replace('\n', '')) + "', `updatedurl` = '" + self.cfgmain.escape_data(str(imgfnameupdnewweb).replace('\n', '')) + "', `path` = '" + self.cfgmain.escape_data(str(imgfnameupdpath).replace('\n', '')) + "', `datasize` = " + str(rrfile.headers['Content-Length']) + ", `dataname` = '" + self.cfgmain.escape_data(str(imgfilename).replace('\n', '')) + "', `datanameupd` = '" + self.cfgmain.escape_data(str(imgfilenameupd).replace('\n', '')) + "', `data` = :gdatavalue1"

                                            else:

                                                insgalvals = insgalvals + "(" + self.cfgmain.escape_data(str(productsid).replace('\n', '')) + ", '" + self.cfgmain.escape_data(str(productssku).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(gal_val).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(imgfnameupdnewweb).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(imgfnameupdpath).replace('\n', '')) + "', null, null, null, :gdatavalue)"
                                                updgalvals = updgalvals + "`products_id` = " + self.cfgmain.escape_data(str(productsid).replace('\n','')) + ", `products_sku` = '" + self.cfgmain.escape_data(str(productssku).replace('\n','')) + "', `gallery` = '" + self.cfgmain.escape_data(str(gal_val).replace('\n','')) + "', `updatedurl` = '" + self.cfgmain.escape_data(str(imgfnameupdnewweb).replace('\n', '')) + "', `path` = '" + self.cfgmain.escape_data(str(imgfnameupdpath).replace('\n', '')) + "', `datasize` = null, `dataname` = null, `datanameupd` = null, `data` = :gdatavalue1"

                                            # insgalvals = insgalvals[:-2] + ";"

                                            insgallerystatement = insgallerystatement + insgalvals + " ON DUPLICATE KEY UPDATE " + updgalvals + ";"

                                            # if productssku == '17830500':
                                            #     print(insgallerystatement)

                                            if self.debug and self.debuglevel >= 0:
                                                print(insgallerystatement)

                                            try:
                                                # print(self.cfg.sqlalchemyconnstr)
                                                istmt = sqlalchemy.text(insgallerystatement)
                                                istmt = istmt.bindparams(gdatavalue=galfilecontent, gdatavalue1=galfilecontent)
                                                with engine.connect() as conn:
                                                    result = conn.execute(istmt)
                                                    conn.commit()
                                                    last_post = result.lastrowid
                                                    if self.debug and self.debuglevel >= 10:
                                                        if last_post % 100 == 0:
                                                            print(last_post)
                                            except pymysql.Error as e:
                                                print(e)
                                                print(insgallerystatement)
                                                # print(str(e)[24:str(e).find("'", 24)])
                                                # if '1054' in str(e) and str(e)[24:str(e).find("'", 24)] not in missingcols:
                                                #     missingcols += str(e)[24:str(e).find("'", 24)] + ", "
                                                #     print(missingcols)
                                                # self.cfgmain.sendErrorEmail(handler, str(e) + str(instmnt))
                                        else:
                                            print("productssku -> " + str(productssku) + " gal_val -> " + str(gal_val))

                                if len(imgupdnewwebarr) != 0:
                                    if self.debug and self.debuglevel >= 10:
                                        print(imgupdnewwebarr)
                                    self.inscols += "`" + 'galleryupd' + "`, "
                                    self.insvals += "'" + self.cfgmain.escape_data(str(imgupdnewwebarr)) + "', "
                                    self.updcolsvals += "`" + 'galleryupd' + "` = '" + self.cfgmain.escape_data(str(imgupdnewwebarr)) + "', "

                            if jobsinfeed == 0:
                                self.colsfromfeed = self.colsfromfeed + "`" + key + "`, "

                        if len(addtoshortdescr) > 29:
                            # print(productsid)
                            # print(productssku)
                            # print(addtoshortdescr)
                            addtoshortdescr = addtoshortdescr + '</div>'

                            if "karcher-borotrade.com" in addtoshortdescr or "kaercher-media.com" in addtoshortdescr or "data:" in value:
                                # print(key)
                                # print(value)
                                addtoshortdescr = addtoshortdescr.replace("&nbsp;", " ")

                                soup = BeautifulSoup(addtoshortdescr, "html.parser")
                                for img in soup.find_all('img'):
                                    if self.debug and self.debuglevel >= 10:
                                        print(img.tag)
                                        print(img.text)
                                        print(img.contents)
                                        print(img.attrs)

                                    img_url = img['src'].replace('\\"', "")

                                    if img_url[0:5] == "data:":
                                        # print(productssku + " -> " + str(img_url[img_url.find(",")+1:][0:20]))
                                        # print(hashlib.sha1(str(img_url[img_url.find(",")+1:]).encode("utf-8")).hexdigest())
                                        imgreqfnameupdtran = str(hashlib.sha1(
                                            str(img_url[img_url.find(",") + 1:]).encode("utf-8")).hexdigest()) + ".png"
                                        imgreqfnameupdnewweb = self.cfgmain.websitedesc + self.cfgmain.imgpathdbdesc + imgreqfnameupdtran
                                        imgreqfnameupdpath = self.cfgmain.imgpathdbdesc + imgreqfnameupdtran

                                        imgreqcontent = base64.decodebytes(
                                            str(img_url[img_url.find(",") + 1:]).encode("utf-8"))
                                        imgreqcontentlen = len(
                                            base64.decodebytes(str(img_url[img_url.find(",") + 1:]).encode("utf-8")))

                                        if os.path.exists(
                                                self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran):
                                            if int(os.stat(
                                                    self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size) != int(
                                                    imgreqcontentlen):
                                                print("file already exists with DIFFERENT size!!! " + str(
                                                    self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran) + " web -> " + str(
                                                    int(imgreqcontentlen)) + " local -> " + str(os.stat(
                                                    self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size))
                                                os.remove(
                                                    self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran)

                                                fimg = open(
                                                    self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran,
                                                    "wb")
                                                fimg.write(imgreqcontent)
                                                fimg.close()
                                        else:
                                            fimg = open(
                                                self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran,
                                                "wb")
                                            fimg.write(imgreqcontent)
                                            fimg.close()

                                    else:
                                        try:
                                            adomain = urllib.parse.urlparse(img_url)  # noqa: F821
                                        except Exception as e:
                                            adomain = urlparse(img_url)
                                            if self.debug and self.debuglevel >= 10:
                                                print(e)

                                        imgreqfilename = adomain.path.split('/')[len(adomain.path.split('/'))-1]
                                        imgreqfilenameupd = adomain.path[4:].replace("/", "_")
                                        imgreqfnameupdtran = slugify.slugify(imgreqfilenameupd, separator='_', regex_pattern=r'[^-a-z0-9._]+')
                                        imgreqfnameupdnewweb = self.cfgmain.websitedesc + self.cfgmain.imgpathdbdesc + imgreqfnameupdtran
                                        imgreqfnameupdpath = self.cfgmain.imgpathdbdesc + imgreqfnameupdtran

                                        imgreqcontent = ""
                                        imgreqcontentlen = ""
                                        try:
                                            imgreq = requests.get(img_url, verify=False)
                                            imgreqcontent = imgreq.content
                                            if 'content-length' in imgreq.headers:
                                                imgreqcontentlen = imgreq.headers['content-length']
                                            else:
                                                imgreqcontentlen = len(imgreqcontent)
                                        except requests.RequestException as e:
                                            print(e)
                                            print(img_url)

                                        if os.path.exists(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran):
                                            if int(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size) != int(imgreqcontentlen):
                                                print("file already exists with DIFFERENT size!!! " + str(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran) + " web -> " + str(imgreqcontentlen) + " local -> " + str(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran).st_size))
                                                os.remove(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran)

                                                fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran, "wb")
                                                fimg.write(imgreqcontent)
                                                fimg.close()
                                        else:
                                            fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + imgreqfnameupdtran, "wb")
                                            fimg.write(imgreqcontent)
                                            fimg.close()

                                    # if imgreqcontent == "":
                                    #     data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4//8/AAX+Av4N70a4AAAAAElFTkSuQmCC"
                                    # else:
                                    #     data_uri = base64.b64encode(imgreqcontent).decode('utf-8')
                                    # img_tag = 'data:' + str(imgreq.headers['content-type']) + ';base64,{0}'.format(data_uri)
                                    # if img_tag == "data:text/html; charset=UTF-8;base64,":
                                    #     print("img_tag is empty for -> " + str(img_url))
                                    addtoshortdescr = addtoshortdescr.replace(img_url, imgreqfnameupdnewweb)
                                # print(value)

                                for a in soup.find_all('a'):
                                    if self.debug and self.debuglevel >= 10:
                                        print(a.tag)
                                        print(a.text)
                                        print(a.contents)
                                        print(a.attrs)

                                    a_url = a['href'].replace('\\"', "")

                                    try:
                                        adomain = urllib.parse.urlparse(a_url)  # noqa: F821
                                    except Exception as e:
                                        adomain = urlparse(a_url)
                                        if self.debug and self.debuglevel >= 10:
                                            print(e)

                                    try:
                                        areq = requests.get(a_url, verify=False)
                                        atext = a.text
                                        acontent = areq.content
                                    except requests.RequestException as e:
                                        print(e)
                                        print(a_url)


                                    if atext.strip() == "":
                                        areqfilename = domain.path.split('/')[len(domain.path.split('/')) - 1]
                                        areqfilenameupd = domain.path[4:].replace("/", "_")
                                        areqfnameupdtran = slugify.slugify(areqfilenameupd, separator='_', regex_pattern=r'[^-a-z0-9._]+')
                                        atext = areqfnameupdtran

                                    if os.path.exists(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext):
                                        if int(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext).st_size) != int(areq.headers['content-length']):
                                            print("file already exists with DIFFERENT size!!! " + str(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext) + " web -> " + str(areq.headers['content-length']) + " local -> " + str(os.stat(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext).st_size))
                                            os.remove(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext)

                                            fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext, "wb")
                                            fimg.write(acontent)
                                            fimg.close()
                                    else:
                                        fimg = open(self.cfgmain.websitepathdesc + self.cfgmain.imgpathdesc + atext, "wb")
                                        fimg.write(acontent)
                                        fimg.close()

                                    addtoshortdescr = addtoshortdescr.replace(a_url, self.cfgmain.websitedesc + self.cfgmain.imgpathdesc + atext)
                                    if self.debug and self.debuglevel >= 10:
                                        print(addtoshortdescr)

                            self.inscols += "`" + 'products_descr_short_upd' + "`, "
                            self.insvals += "'" + self.cfgmain.escape_data(str(addtoshortdescr)) + "', "
                            self.updcolsvals += "`" + 'products_descr_short_upd' + "` = '" + self.cfgmain.escape_data(str(addtoshortdescr)) + "', "

                        if self.shortcode != '':
                            # print(self.shortcode)

                            if self.debug and self.debuglevel >= 0:
                                print(self.mainurl + self.shortcode)
                            rsec = requests.get(self.mainurl + self.shortcode, headers=self.requestHeader)
                            pagesec = rsec.content.decode("utf-8")
                            if self.debug and self.debuglevel >= 0:
                                print(pagesec)

                            try:
                                rootsec = json.loads(pagesec)
                            except json.JSONDecodeError as e:
                                print(e)
                                self.cfgmain.sendErrorEmail(handler, e)
                                return jobsinfeed

                            if self.jobfeedid == '00141_TMOPAC_JSON_FEED':
                                rootsec = rootsec['data']['jobDetails']

                            for keysec, valuesec in rootsec.items():
                                if self.debug and self.debuglevel >= 0:
                                    print(keysec)
                                    print(valuesec)

                                if keysec != 'meta':
                                    if keysec in self.dtarr:
                                        try:
                                            valuesec = "'" + str(datetime.strptime(valuesec, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")) + "'"
                                        except Exception as e:
                                            # print(e)
                                            valuesec = 'null'
                                    elif keysec in self.boolarr:
                                        valuesec = valuesec
                                    else:
                                        if valuesec is None:
                                            valuesec = 'null'
                                        else:
                                            valuesec = "'" + self.cfgmain.escape_data(str(valuesec).replace('\n', '')) + "'"

                                    self.inscols += "`" + "job_" + keysec + "`, "
                                    self.insvals += str(valuesec) + ", "
                                    self.updcolsvals += "`" + "job_" + keysec + "` = " + str(valuesec) + ", "

                                    if jobsinfeed == 0:
                                        self.colsfromfeed = self.colsfromfeed + "`" + "job_" + keysec + "`, "

                        self.inscols = self.inscols[:-2]
                        self.insvals = self.insvals[:-2]
                        self.updcolsvals = self.updcolsvals[:-2]

                        if self.debug and self.debuglevel >= 10:
                            print(self.inscols)
                            print(self.insvals)
                            print(self.updcolsvals)

                        self.inscols += ", `" + "existinfeed" + "`"
                        self.insvals += ", '" + "1" + "'"
                        self.updcolsvals += ", `existinfeed` = '" + "2" + "'"

                        self.inscols += ", `" + "job_feed_id" + "`"
                        self.insvals += ", '" + self.jobfeedid + "'"
                        self.updcolsvals += ", `job_feed_id` = '" + self.jobfeedid + "'"

                        insstatement = "INSERT INTO `" + self.cfg.database + "`.`" + self.tablename + "` (" \
                                       + self.inscols + ")"
                        insstatement += " VALUES(" + self.insvals + ")"
                        insstatement += " ON DUPLICATE KEY UPDATE " + self.updcolsvals + ";"

                        if self.debug and self.debuglevel >= 10:
                            print(insstatement)

                        try:
                            handlersconn = self.myConnectionMain.connection()
                            unijsondb = handlersconn.cursor()

                            unijsondb.execute('SET NAMES utf8mb4;')
                            unijsondb.execute('SET character_set_connection=utf8mb4;')

                            try:
                                unijsondb.execute(insstatement)
                                self.database_check = '<span style=\"color:green;\">Successfull</span>'
                            except pymysql.Error as e:
                                print(e)
                                # print(insstatement)
                                self.cfgmain.sendErrorEmail(handler, str(e) + str(insstatement))
                                self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                                return jobsinfeed

                            if self.debug and self.debuglevel >= 9:
                                print(jobsinfeed)
                                print(unijsondb.rowcount)
                        finally:
                            handlersconn.close()  # returns the connection to the pool

                        self.inscols = ''
                        self.insvals = ''
                        self.updcolsvals = ''

                        jobsinfeed = jobsinfeed + 1

            print(iCntAttr)
            if self.debug and self.debuglevel >= 10:
                fout.close()
                foutins.close()
        else:
            if self.jobtagfromfeed is not None and len(self.jobtagfromfeed) != 0:
                # print(self.jobtagfromfeed)
                root = root[self.jobtagfromfeed]
            for i in range(len(root)):
                self.shortcode = ''
                productsid = 0
                productssku = ''
                gallery = ''
                try:
                    job = root[i]
                except Exception as e:
                    print(e)
                    job = root

                if self.ats == 'unijsonsku':
                    job = job["0"]

                if self.debug and self.debuglevel >= 10:
                    print(job)
                for key, value in job.items():
                    if self.debug and self.debuglevel >= 10:
                        print(key)
                        print(value)

                    if key == 'products_sku':
                        productssku = value

                    if key == 'products_id':
                        productsid = value

                    if self.ats == 'unijsonsku':
                        productssku = self.port
                        if key == 'translations':
                            for key1, value1 in value.items():
                                if self.debug and self.debuglevel >= 10:
                                    print(key1)
                                    print(value1)

                                self.inscols += "`" + key + "_" + key1 + "`, "
                                self.insvals += "'" + str(value1) + "', "
                                self.updcolsvals += "`" + key + "_" + key1 + "` = '" + str(value1) + "', "

                                if jobsinfeed == 0:
                                    self.colsfromfeed = self.colsfromfeed + "`" + key + "_" + key1 + "`, "
                        elif key == 'suggestions' and len(value) != 0:
                            if self.debug and self.debuglevel >= 10:
                                print(key)
                                print(value[0])

                            self.inscols += "`" + key + "`, "
                            self.insvals += "'" + str(value[0]) + "', "
                            self.updcolsvals += "`" + key + "` = '" + str(value[0]) + "', "

                            if jobsinfeed == 0:
                                self.colsfromfeed = self.colsfromfeed + "`" + key + "`, "
                        elif key == 'resultGroups' and len(value) != 0:
                            for key2, valuetemp in value.items():
                                if self.debug and self.debuglevel >= 10:
                                    print(key2)
                                    print(valuetemp)

                                for keytemp1, valuetemp1 in valuetemp.items():
                                    if self.debug and self.debuglevel >= 10:
                                        print(keytemp1)
                                        print(valuetemp1)

                                    for key1, value1 in valuetemp1[0].items():
                                        if self.debug and self.debuglevel >= 10:
                                            print(key1)
                                            print(value1)

                                        if key1 != 'rating' and key1 != 'icons':
                                            self.inscols += "`" + key + "_" + key2 + "_" + key1 + "`, "
                                            self.insvals += "'" + str(value1) + "', "
                                            self.updcolsvals += "`" + key + "_" + key2 + "_" + key1 + "` = '" + str(value1) + "', "

                                            if jobsinfeed == 0:
                                                self.colsfromfeed = self.colsfromfeed + "`" + key + "_" + key2 + "_" + key1 + "`, "

                                            if key2 == 'products' and key1 == 'url':
                                                # print(self.mainurladd)
                                                # print(value1)
                                                # rr = requests.get(self.mainurladd + value1)
                                                # print(rr.status_code)
                                                service = Service()
                                                driver = webdriver.Chrome(service=service, options=self.getChromeOptions('desktop'))
                                                # driver = webdriver.Chrome()

                                                driver.get(self.mainurladd + value1)
                                                driver.implicitly_wait(5)

                                                timeout = 5  # seconds
                                                returnpagefailed = True
                                                countreturnpagefailed = 0
                                                while returnpagefailed == True:
                                                    try:
                                                        element_present = EC.presence_of_element_located((By.XPATH, "//div[@class='fc-pagination']"))
                                                        WebDriverWait(driver, timeout).until(element_present)
                                                        print("Page is ready!")
                                                        returnpagefailed = False
                                                        countreturnpagefailed = 0
                                                    except TimeoutException:
                                                        print("Loading took too much time!")
                                                        returnpagefailed = True
                                                        countreturnpagefailed = countreturnpagefailed + 1
                                                    if countreturnpagefailed > 3:
                                                        print("Open page failed too many times!!!")
                                                        # self.cfgmain.sendErrorEmail(handler, "Open page failed too many times!!!")
                                                        return

                                                try:
                                                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                                                    sleep(random.choice(list(range(3, 7))))
                                                except TimeoutException as te:
                                                    print(te)

                                                print("Starting " + self.mainurladd + value1 + " scrape...")
                                                # print(rr.content.decode(rr.encoding))

                                                try:
                                                    # pagedetails = rr.content.decode(rr.encoding)
                                                    pagedetails = driver.page_source.encode("utf-8")

                                                    soup = BeautifulSoup(pagedetails, "html.parser")

                                                    insertintogaltable = "INSERT INTO `" + self.cfg.database + "`.`borotrade_karcher_gallery_json` (`products_id`, `products_sku`, `gallery`) VALUES"

                                                    imagesarr = soup.find("div", class_="fc-pagination").find_all("li")
                                                    for img in imagesarr:
                                                        imgr = img.find("a", class_="fc-page fc-page-image")
                                                        # print(imgr)
                                                        if 'href' in str(imgr):
                                                            if imgr['href'][0:6] == "https:":
                                                                myimage = imgr['href']
                                                                # print(myimage)
                                                                insertintogaltable = insertintogaltable + "('" + str(productsid) + "', '" + productssku + "', '" + myimage + "'), "
                                                            else:
                                                                print("ERROR -> " + str(imgr))

                                                    insertintogaltable = insertintogaltable[:-2] + " ON DUPLICATE KEY UPDATE data = null" + ";"

                                                    if self.debug and self.debuglevel >= 10:
                                                        print(insertintogaltable)

                                                    try:
                                                        handlersconn = self.myConnectionMain.connection()
                                                        unijsondb = handlersconn.cursor()

                                                        unijsondb.execute('SET NAMES utf8mb4;')
                                                        unijsondb.execute('SET character_set_connection=utf8mb4;')

                                                        try:
                                                            unijsondb.execute(insertintogaltable)
                                                            self.database_check = '<span style=\"color:green;\">Successfull</span>'
                                                        except pymysql.Error as e:
                                                            print(e)
                                                            # print(insertintogaltable)
                                                            self.cfgmain.sendErrorEmail(handler, str(e) + str(insertintogaltable))
                                                            self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                                                            return jobsinfeed

                                                        if self.debug and self.debuglevel >= 9:
                                                            print(jobsinfeed)
                                                            print(unijsondb.rowcount)
                                                    finally:
                                                        handlersconn.close()  # returns the connection to the pool

                                                    itemtitle = soup.find("div", class_="col-sm-12 col-lg-9").find("h1").text.strip()

                                                    description = soup.find("div", class_="fg-products-details-page").find_all("section", class_="container")[2]
                                                    description = "<h2>ХАРАКТЕРИСТИКИ И ПРЕДИМСТВА НА " + str(itemtitle) + "</h2>\n" + str(description)
                                                    description = description.replace("Обхват на доставката", "Стандартна окомплектовка")
                                                    description = description.replace("<h3><p>Стандартна окомплектовка</p></h3>", "<h2><p>Стандартна окомплектовка</p></h2>")
                                                    if self.debug and self.debuglevel >= 9:
                                                        print(description)

                                                    self.inscols += "`description`, "
                                                    self.insvals += "'" + self.cfgmain.escape_data(str(description)) + "', "
                                                    self.updcolsvals += "`description` = '" + self.cfgmain.escape_data(str(description)) + "', "

                                                    if jobsinfeed == 0:
                                                        self.colsfromfeed = self.colsfromfeed + "`description`, "

                                                    sections = soup.find_all("section", class_="container")
                                                    # print(sections)

                                                    for section in sections:
                                                        # print(section.prettify())

                                                        # get product description
                                                        # if "p property=\"description\"" in str(section):
                                                        #     description = section.find("p", {"property":"description"}).text.strip()
                                                        #
                                                        #     self.inscols += "`description`, "
                                                        #     self.insvals += "'" + str(description) + "', "
                                                        #     self.updcolsvals += "`description` = '" + str(description) + "', "
                                                        #
                                                        #     if jobsinfeed == 0:
                                                        #         self.colsfromfeed = self.colsfromfeed + "`description`, "

                                                        # get the 3 additional images / texts for the item description
                                                        # headlinebottom
                                                        # row fc-featurebenefits-row
                                                        if "h6 class=\"headlinebottom\"" in str(section):
                                                            # print(str(section))
                                                            # print(section.find("div", {"id":"featurebenefits"}))

                                                            # heading change to h2
                                                            # leave as part of the description
                                                            # <h2>ХАРАКТЕРИСТИКИ И ПРЕДИМСТВА НА (Името на продукта)</h2> -> description
                                                            # <h2>Обхват на доставката -> Стандартна окомплектовка</h2>
                                                            # СЪВМЕСТИМИ УРЕДИ -> descriptiom и в таблицата със свързаните products_sku

                                                            insertintogaltable = "INSERT INTO `" + self.cfg.database + "`.`borotrade_karcher_gallery_json` (`products_id`, `products_sku`, `gallery`) VALUES"

                                                            sectchar = section.find("div", {"id":"featurebenefits"})
                                                            characteristics1 = sectchar.find_all("div", class_="col-sm-4 image-fit")
                                                            for char1 in characteristics1:
                                                                # print(char1)
                                                                if '<img' in str(char1):
                                                                    myimage = char1.find("img")['data-src']
                                                                    # print(myimage)
                                                                    insertintogaltable = insertintogaltable + "('" + str(productsid) + "', '" + productssku + "', '" + myimage + "'), "
                                                                # if '<h6 class="headlinebottom"' in str(char1):
                                                                #     print(char1.find("h6", class_="headlinebottom").text.strip())
                                                                #     print(char1.find("h6", class_="headlinebottom").next_sibling.text.strip())
                                                                    # print(char1.find(text=True, recursive=False))
                                                                    # print(char1.xpath('text()'))

                                                            insertintogaltable = insertintogaltable[:-2] + " ON DUPLICATE KEY UPDATE data = null" + ";"

                                                            if self.debug and self.debuglevel >= 10:
                                                                print(insertintogaltable)

                                                            try:
                                                                handlersconn = self.myConnectionMain.connection()
                                                                unijsondb = handlersconn.cursor()

                                                                unijsondb.execute('SET NAMES utf8mb4;')
                                                                unijsondb.execute('SET character_set_connection=utf8mb4;')

                                                                try:
                                                                    unijsondb.execute(insertintogaltable)
                                                                    self.database_check = '<span style=\"color:green;\">Successfull</span>'
                                                                except pymysql.Error as e:
                                                                    print(e)
                                                                    # print(insertintogaltable)
                                                                    self.cfgmain.sendErrorEmail(handler, str(e) + str(insertintogaltable))
                                                                    self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                                                                    return jobsinfeed

                                                                if self.debug and self.debuglevel >= 9:
                                                                    print(jobsinfeed)
                                                                    print(unijsondb.rowcount)
                                                            finally:
                                                                handlersconn.close()  # returns the connection to the pool

                                                            characteristics2 = sectchar.find_all("div", class_="row fc-featurebenefits-row")
                                                            # for char2 in characteristics2:
                                                            #     print(char2)
                                                            #     if '<h6>' in str(char2):
                                                            #         print(char2.find("h6").text.strip())
                                                            #     if '<li' in str(char2):
                                                            #         liarr = char2.find_all("li")
                                                            #         for li in liarr:
                                                            #             print(li.text.strip())
                                                        # if "Спецификации" in str(section):
                                                            # print(section)



                                                except Exception as e:
                                                    print(e)

                                                # //*[@id="main"]/main/div[2]/section[2]
                        else:
                            if self.debug and self.debuglevel >= 10:
                                print(key)
                                print(value)

                            if key != 'suggestions' and key != 'resultGroups':
                                self.inscols += "`" + key + "`, "
                                self.insvals += "'" + str(value) + "', "
                                self.updcolsvals += "`" + key + "` = '" + str(value) + "', "

                                if jobsinfeed == 0:
                                    self.colsfromfeed = self.colsfromfeed + "`" + key + "`, "
                    else:
                        if key in self.dtarr:
                            try:
                                value = "'" + str(datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")) + "'"
                            except Exception as e:
                                # print(e)
                                value = 'null'
                        elif key in self.boolarr:
                            value = value
                        elif type(value) is dict:
                            # print("dict -> " + str(value))
                            if 'jobDetails' in value:
                                if 'href' in value['jobDetails']:
                                    if key == self.seccallcols:
                                        self.shortcode = str(value['jobDetails']['href'])
                                    value = "'" + str(value['jobDetails']['href']) + "'"
                                else:
                                    value = "'" + "'"
                            elif key == "job" or key == "location":
                                for key1, value1 in value.items():
                                    # print(key1)
                                    # print(value1)
                                    if type(value1) is dict:
                                        for key2, value2 in value1.items():
                                            self.inscols += "`" + key + "_" + key1 + "_" + key2 + "`, "
                                            self.insvals += "'" + str(value2) + "', "
                                            self.updcolsvals += "`" + key + "_" + key1 + "_" + key2 + "` = '" + str(value2) + "', "

                                            if jobsinfeed == 0:
                                                self.colsfromfeed = self.colsfromfeed + "`" + key + "_" + key1 + "_" + key2 + "`, "
                                    else:
                                        self.inscols += "`" + key + "_" + key1 + "`, "
                                        self.insvals += "'" + str(value1) + "', "
                                        self.updcolsvals += "`" + key + "_" + key1 + "` = '" + str(value1) + "', "

                                        if jobsinfeed == 0:
                                            self.colsfromfeed = self.colsfromfeed + "`" + key + "_" + key1 + "`, "
                            else:
                                value = "'" + "'"
                        elif type(value) is list:
                            # print("list -> " + str(value))
                            # print(value)
                            if key == 'gallery':
                                # print(value)
                                gallery = value
                                # value = "'" + "'"
                                # value = "'" + self.cfgmain.escape_data(str(value).replace('\n', '')) + "'"
                                value = self.cfgmain.escape_data(str(value).replace('\n', ''))

                                # self.inscols += "`" + key + "`, "
                                # self.insvals += "'" + str(value) + "', "
                                # self.updcolsvals += "`" + key + "` = '" + str(value) + "', "
                            else:
                                value = "'" + "'"

                        elif key == 'formattedAddress':
                            addrsplit = str(value).split("\r\n")
                            # print(addrsplit)
                            if len(addrsplit) == 4:
                                self.inscols += "`" + 'formattedAddress_street' + "`, "
                                self.insvals += "'" + str(addrsplit[0]) + "', "
                                self.updcolsvals += "`" + 'formattedAddress_street' + "` = '" + str(addrsplit[0]) + "', "

                                self.inscols += "`" + 'formattedAddress_town' + "`, "
                                self.insvals += "'" + str(addrsplit[1]) + "', "
                                self.updcolsvals += "`" + 'formattedAddress_town' + "` = '" + str(addrsplit[1]) + "', "

                                self.inscols += "`" + 'formattedAddress_postcode' + "`, "
                                self.insvals += "'" + str(addrsplit[2]) + "', "
                                self.updcolsvals += "`" + 'formattedAddress_postcode' + "` = '" + str(addrsplit[2]) + "', "

                                self.inscols += "`" + 'formattedAddress_country' + "`, "
                                self.insvals += "'" + str(addrsplit[3]) + "', "
                                self.updcolsvals += "`" + 'formattedAddress_country' + "` = '" + str(addrsplit[3]) + "', "
                            value = "'" + value + "'"
                        else:
                            if value is None:
                                value = 'null'
                            else:
                                value = self.cfgmain.escape_data(str(value).replace('\n', ''))
                                # value = "'" + self.cfgmain.escape_data(str(value).replace('\n', '')) + "'"

                        if (key == "job" or key == "location") and type(value) is dict:
                            value = value
                        else:
                            self.inscols += "`" + key + "`, "
                            self.insvals += str(value) + ", "
                            self.updcolsvals += "`" + key + "` = " + str(value) + ", "

                        if gallery != '' and productssku != '' and productsid != 0:
                            if gallery is not None and gallery != 'NULL':
                                for gal_val in gallery:
                                    try:
                                        domain = urllib.parse.urlparse(gal_val)  # noqa: F821
                                    except Exception as e:
                                        domain = urlparse(gal_val)
                                        if self.debug and self.debuglevel >= 10:
                                            print(e)

                                    imgfilename = domain.path.split('/')[len(domain.path.split('/'))-1]
                                    imgfilenameupd = domain.path[4:].replace("/", "_")

                                    if self.debug and self.debuglevel >= 10:
                                        print(domain)
                                        print(domain.scheme)
                                        print(domain.netloc)
                                        print(domain.path)
                                        print(len(domain.path.split('/')))
                                        print(domain.path.split('/'))
                                        print(imgfilename)
                                        print(imgfilenameupd)

                                    if pull_images == 1:
                                        insgalvals = ''
                                        insgallerystatement = "INSERT INTO `" + self.cfg.database + "`.`borotrade_gallery_json` (`products_id`, `products_sku`, `gallery`, `datasize`, `dataname`, `datanameupd`, `data`) VALUES "
                                        if self.debug and self.debuglevel >= 10:
                                            print(str(productssku) + " -> " + str(gal_val))
                                        rrfile = requests.get(gal_val, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0"})
                                        if rrfile.status_code == 200:
                                        # print(rrfile.content)
                                        # print(rrfile.headers['Content-Length'])

                                            insgalvals = insgalvals + "(" + self.cfgmain.escape_data(str(productsid).replace('\n', '')) + ", '" + self.cfgmain.escape_data(str(productssku).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(gal_val).replace('\n', '')) + "', " + str(rrfile.headers['Content-Length']) + ", '" + self.cfgmain.escape_data(str(imgfilename).replace('\n', '')) + "', '" + self.cfgmain.escape_data(str(imgfilenameupd).replace('\n', '')) + "', :gdatavalue);"

                                            # insgalvals = insgalvals[:-2] + ";"

                                            insgallerystatement = insgallerystatement + insgalvals

                                            # if productssku == '17830500':
                                            #     print(insgallerystatement)

                                            if self.debug and self.debuglevel >= 0:
                                                print(insgallerystatement)

                                            try:
                                                # print(self.cfg.sqlalchemyconnstr)
                                                engine = sqlalchemy.create_engine(self.cfg.sqlalchemyconnstr)
                                                istmt = sqlalchemy.text(insgallerystatement)
                                                istmt = istmt.bindparams(gdatavalue=rrfile.content)
                                                with engine.connect() as conn:
                                                    result = conn.execute(istmt)
                                                    conn.commit()
                                                    last_post = result.lastrowid
                                                    print(last_post)
                                                # gmaildb.execute(instmnt)
                                                # cfg.myConnectionMain.commit()
                                                # print(gmaildb.lastrowid)
                                                # print(last_post)
                                                # if len(filename) > 0 and filename is not None:
                                                #     for f in filename:
                                                #         # instfmnt = "INSERT INTO `gmail`.`gmailatchmnts` (`gid`, `filename`, `filecontent`) VALUES (" + str(gmaildb.lastrowid) + ", '" + str(filename[f]) + "', %s);"
                                                #         instfmnt = """INSERT INTO `""" + self.database + """`.`""" + self.mailattachmentstable + """` (`gid`, `filename`, `filecontent`) VALUES (:gidvalue, :gfnamevalue, :gfcontentvalue);"""
                                                #         stmt = sqlalchemy.text(instfmnt)
                                                #         stmt = stmt.bindparams(gidvalue=str(last_post), gfnamevalue=str(filename[f]),
                                                #                                gfcontentvalue=filecontent[filename[f]])
                                                #         # gmaildb.execute(instfmnt, (filecontent[filename[f]],))
                                                #         # cfg.myConnectionMain.commit()
                                                #         # engine = sqlalchemy.create_engine('mysql+pymysql://root:Password@localhost/gmail')
                                                #         with engine.connect() as conn:
                                                #             conn.execute(stmt)
                                                #             conn.commit()
                                            except pymysql.Error as e:
                                                print(e)
                                                print(insgallerystatement)
                                                # print(str(e)[24:str(e).find("'", 24)])
                                                # if '1054' in str(e) and str(e)[24:str(e).find("'", 24)] not in missingcols:
                                                #     missingcols += str(e)[24:str(e).find("'", 24)] + ", "
                                                #     print(missingcols)
                                                # self.cfgmain.sendErrorEmail(handler, str(e) + str(instmnt))

                                        else:
                                            print(rrfile.status_code)

                                # try:
                                #     unijsondb.execute(insgallerystatement)
                                # except pymysql.Error as e:
                                #     print(e)
                                #     # self.cfgmain.sendErrorEmail(handler, str(e) + str(insgallerystatement))
                                #     # return jobsinfeed

                        if jobsinfeed == 0:
                            self.colsfromfeed = self.colsfromfeed + "`" + key + "`, "

                    if self.shortcode != '':
                        # print(self.shortcode)

                        if self.debug and self.debuglevel >= 0:
                            print(self.mainurl + self.shortcode)
                        rsec = requests.get(self.mainurl + self.shortcode, headers=self.requestHeader)
                        pagesec = rsec.content.decode("utf-8")
                        if self.debug and self.debuglevel >= 0:
                            print(pagesec)

                        try:
                            rootsec = json.loads(pagesec)
                        except json.JSONDecodeError as e:
                            print(e)
                            self.cfgmain.sendErrorEmail(handler, e)
                            return jobsinfeed

                        if self.jobfeedid == '00141_TMOPAC_JSON_FEED':
                            rootsec = rootsec['data']['jobDetails']

                        for keysec, valuesec in rootsec.items():
                            if self.debug and self.debuglevel >= 0:
                                print(keysec)
                                print(valuesec)

                            if keysec != 'meta':
                                if keysec in self.dtarr:
                                    try:
                                        valuesec = "'" + str(datetime.strptime(valuesec, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M:%S")) + "'"
                                    except Exception as e:
                                        # print(e)
                                        valuesec = 'null'
                                elif keysec in self.boolarr:
                                    valuesec = valuesec
                                else:
                                    if valuesec is None:
                                        valuesec = 'null'
                                    else:
                                        valuesec = "'" + self.cfgmain.escape_data(str(valuesec).replace('\n', '')) + "'"

                                self.inscols += "`" + "job_" + keysec + "`, "
                                self.insvals += str(valuesec) + ", "
                                self.updcolsvals += "`" + "job_" + keysec + "` = " + str(valuesec) + ", "

                                if jobsinfeed == 0:
                                    self.colsfromfeed = self.colsfromfeed + "`" + "job_" + keysec + "`, "

                self.inscols = self.inscols[:-2]
                self.insvals = self.insvals[:-2]
                self.updcolsvals = self.updcolsvals[:-2]

                if self.debug and self.debuglevel >= 10:
                    print(self.inscols)
                    print(self.insvals)
                    print(self.updcolsvals)

                if self.ats == 'unijsonsku':
                    self.inscols += ", `" + "products_sku" + "`"
                    self.insvals += ", '" + self.port + "'"
                    self.updcolsvals += ", `products_sku` = '" + self.port + "'"

                self.inscols += ", `" + "existinfeed" + "`"
                self.insvals += ", '" + "1" + "'"
                self.updcolsvals += ", `existinfeed` = '" + "2" + "'"

                self.inscols += ", `" + "job_feed_id" + "`"
                self.insvals += ", '" + self.jobfeedid + "'"
                self.updcolsvals += ", `job_feed_id` = '" + self.jobfeedid + "'"

                insstatement = "INSERT INTO `" + self.cfg.database + "`.`" + self.tablename + "` (" \
                               + self.inscols + ")"
                insstatement += " VALUES(" + self.insvals + ")"
                insstatement += " ON DUPLICATE KEY UPDATE " + self.updcolsvals + ";"

                if self.debug and self.debuglevel >= 10:
                    print(insstatement)

                try:
                    handlersconn = self.myConnectionMain.connection()
                    unijsondb = handlersconn.cursor()

                    unijsondb.execute('SET NAMES utf8mb4;')
                    unijsondb.execute('SET character_set_connection=utf8mb4;')

                    try:
                        unijsondb.execute(insstatement)
                        self.database_check = '<span style=\"color:green;\">Successfull</span>'
                    except pymysql.Error as e:
                        print(e)
                        print(insstatement)
                        self.cfgmain.sendErrorEmail(handler, str(e) + str(insstatement))
                        self.database_check = '<span style="color:red;">' + str(e) + '</span>'
                        return jobsinfeed

                    if self.debug and self.debuglevel >= 9:
                        print(jobsinfeed)
                        print(unijsondb.rowcount)
                finally:
                    handlersconn.close()  # returns the connection to the pool

                self.inscols = ''
                self.insvals = ''
                self.updcolsvals = ''

                jobsinfeed = jobsinfeed + 1

        return jobsinfeed

    def getDetailsFromDB(self, sku, domain):
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            stmnt = "SELECT `title`, `url`, `retailprice`, `curprice`, `bestprice` FROM `" + self.cfg.database + "`.`" + self.tablename + "` WHERE job_feed_id = '" + self.jobfeedid + "' and sku = '" + sku + "' and domain = '" + domain + "';"

            try:
                if self.debug and self.debuglevel >= 0:
                    print(stmnt)
                dbhandler.execute(stmnt)
                self.skudetails.clear()
                self.skudetails = {'sku': sku}
                self.skudetails['sku'] = {'title':'', 'url':'', 'retailprice':'', 'curprice':'', 'bestprice':''}
                for item in dbhandler.fetchall():
                    self.skudetails['sku'] = item
                if self.debug and self.debuglevel >= 0:
                    print(self.skudetails)
            except pymysql.Error as e:
                print(e)
                print(stmnt)
                self.cfgmain.sendErrorEmail({'jobfeed_id':''}, str(e) + str(stmnt))
                return
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def getMappingFromDB(self, domain, key=''):
        if key == '':
            result = {}
        else:
            result = ''
        try:
            handlersconn = self.myConnectionMain.connection()
            dbhandler = handlersconn.cursor()

            dbhandler.execute('SET NAMES utf8mb4;')
            dbhandler.execute('SET character_set_connection=utf8mb4;')

            if key == '':
                stmnt = "SELECT `key`, `val` FROM `" + self.cfg.database + "`.`" + self.tablenamekarchermapping + "` WHERE job_feed_id = '" + self.jobfeedid + "' and domain = '" + domain + "' and `type` <> 's';"
            else:
                stmnt = "SELECT `val` FROM `" + self.cfg.database + "`.`" + self.tablenamekarchermapping + "` WHERE job_feed_id = '" + self.jobfeedid + "' and domain = '" + domain + "' and `key` = '" + key + "';"

            try:
                if self.debug and self.debuglevel >= 0:
                    print(stmnt)
                dbhandler.execute(stmnt)
                if key == '':
                    for item in dbhandler.fetchall():
                        result.update({item['key']: item['val']})
                else:
                    for item in dbhandler.fetchall():
                        result = item['val']
                if self.debug and self.debuglevel >= 0:
                    print(result)
            except pymysql.Error as e:
                print(e)
                print(stmnt)
                self.cfgmain.sendErrorEmail({'jobfeed_id':''}, str(e) + str(stmnt))
                return result
        finally:
            handlersconn.close()                                # returns the connection to the pool
        return result

    def prWebScraping(self, handler):
        # self.debug = True
        # self.debuglevel = 0

        start = datetime.now()
        print(start)

        self.resetFeedVars()
        self.loadFeedVars(handler)

        if self.feedlocks == 1:
            errormsg = self.jobfeedid + ' Handler locked!!!'
            print(errormsg)
            self.cfgmain.sendErrorEmail(handler, errormsg)
            return

        print('Processing: ' + self.jobfeedid)

        self.updJobsTable(handler)

        self.getTableColsTypes(handler)

        self.getJobsInDB(handler)
        jobsindb = self.jobsindb

        url = urlparse(self.url)

        self.mainurl = url[0] + "://" + url[1]

        if self.server is not None and self.server != '' and self.server not in ("delete", "donotdelete"):
            self.mainurl = self.server

        if self.server is None or self.server == '':
            self.server = "donotdelete"

        page = ""
        urlsarr = {}

        try:
            print("Starting...")

            if self.feedtype == 'sku':
                service = Service()
                driver = webdriver.Chrome(service=service, options=self.getChromeOptions('desktop'))
                # driver.implicitly_wait(10)

                # sku from stck -> Desso give select - products_sku
                # SELECT * FROM stck s LEFT JOIN stck_l l ON s.id=l.id_stck WHERE s.suser>0 AND s.sactx=0 AND l.wid<>0
                sku = "11952500"

                driver.get(self.url + sku + "%20цена")

                timeout = 5  # seconds
                try:
                    element_present = EC.presence_of_element_located((By.XPATH, "//div[@classs='gsc-resultsbox-visible']"))
                    WebDriverWait(driver, timeout).until(element_present)
                    print("Page is ready!")
                except TimeoutException:
                    print("Loading took too much time!")

                if self.debug and self.debuglevel >= 9:
                    print(driver.page_source.encode("utf-8"))

                page = driver.page_source.encode("utf-8")

                parser = lxmlET.HTMLParser(recover=True, encoding='utf-8')
                root = lh.fromstring(page, parser=parser)

                self.rss_check = '<span style="color:green;">Successful run for handler ' + self.jobfeedid + '</span>'

                # affectedrows = 0
                self.jobsinfeed = 0

                for item in root.xpath("//div[@class='gsc-webResult gsc-result']"):
                    # print(lxml.html.tostring(item))

                    # добави пореден номер в търсенето

                    title = item.xpath(".//a[@class='gs-title']")[0].text.strip()
                    print(title)
                    url2call = item.xpath(".//a[@class='gs-title']")[0].get('href')
                    print(url2call)
                    domain2call = item.xpath(".//div[@class='gs-bidi-start-align gs-visibleUrl gs-visibleUrl-breadcrumb']/span")[0].text.strip()
                    print(domain2call)
                    if self.cfg.validate_domain_name(domain2call):
                        domain2call = domain2call
                    else:
                        try:
                            domainfromurl2call = urllib.parse.urlparse(url2call)  # noqa: F821
                        except Exception as e:
                            domainfromurl2call = urlparse(url2call)
                            if self.debug and self.debuglevel >= 10:
                                print(e)
                        domain2call = domainfromurl2call[1]
                    print(domain2call)
                    # print(item.xpath(".//a[@class='gs-title']")[1].text)
                    # print(item.xpath(".//a[@class='gs-title']")[1].get('href'))

                    self.inscols += "`" + "sku" + "`, "
                    self.insvals += "'" + self.cfgmain.escape_data(str(sku)) + "', "
                    self.updcolsvals += "`" + "sku" + "` = '" + self.cfgmain.escape_data(str(sku)) + "', "

                    if self.jobsinfeed == 0:
                        self.colsfromfeed = self.colsfromfeed + "`" + "sku" + "`, "

                    self.inscols += "`" + "title" + "`, "
                    self.insvals += "'" + self.cfgmain.escape_data(str(title)) + "', "
                    self.updcolsvals += "`" + "title" + "` = '" + self.cfgmain.escape_data(str(title)) + "', "

                    if self.jobsinfeed == 0:
                        self.colsfromfeed = self.colsfromfeed + "`" + "title" + "`, "

                    self.inscols += "`" + "url" + "`, "
                    self.insvals += "'" + self.cfgmain.escape_data(str(url2call)) + "', "
                    self.updcolsvals += "`" + "url" + "` = '" + self.cfgmain.escape_data(str(url2call)) + "', "

                    if self.jobsinfeed == 0:
                        self.colsfromfeed = self.colsfromfeed + "`" + "url" + "`, "

                    self.inscols += "`" + "domain" + "`, "
                    self.insvals += "'" + self.cfgmain.escape_data(str(domain2call)) + "', "
                    self.updcolsvals += "`" + "domain" + "` = '" + self.cfgmain.escape_data(str(domain2call)) + "', "

                    if self.jobsinfeed == 0:
                        self.colsfromfeed = self.colsfromfeed + "`" + "domain" + "`, "

                    self.getDetailsFromDB(sku, domain2call)

                    if url2call != self.skudetails['sku']['url']:
                        print("URL different!!! db url -> " + str(self.skudetails['sku']['url'] + " feed url -> " + str(url2call)))

                    driver.get(url2call)

                    timeout = 5  # seconds

                    loadfromdomain = self.getMappingFromDB(domain2call, 'load')

                    if loadfromdomain != '' and loadfromdomain is not None:
                        try:
                            element_present = EC.presence_of_element_located((By.XPATH, loadfromdomain))
                            WebDriverWait(driver, timeout).until(element_present)
                            print("Page is ready!")
                        except TimeoutException:
                            print("Loading took too much time!")
                    else:
                        sleep(random.choice(list(range(3, 7))))
                        print("Page is ready with timeout!")

                    if self.debug and self.debuglevel >= 9:
                        print(driver.page_source.encode("utf-8"))

                    pagedetails = driver.page_source.encode("utf-8")

                    parser = lxmlET.HTMLParser(recover=True, encoding='utf-8')
                    rootdetails = lh.fromstring(pagedetails, parser=parser)

                    maparr = self.getMappingFromDB(domain2call)
                    for maparritem in maparr:
                        tag = maparritem
                        text = maparr[maparritem]

                        print(tag)
                        print(text)

                        self.inscols += "`" + tag + "`, "
                        self.insvals += "'" + self.cfgmain.escape_data(str(text)) + "', "
                        self.updcolsvals += "`" + tag + "` = '" + self.cfgmain.escape_data(str(text)) + "', "

                        if self.jobsinfeed == 0:
                            self.colsfromfeed = self.colsfromfeed + "`" + tag + "`, "

                    # description = ''
                    # retailprice = ''
                    # curprice = ''
                    # bestprice = ''
                    #
                    # try:
                    #     descrfromdomain = self.getMappingFromDB(domain2call, 'description')
                    #     if descrfromdomain != '' and descrfromdomain is not None:
                    #         description = rootdetails.xpath(descrfromdomain)[0].text.strip()
                    #     rpfromdomain = self.getMappingFromDB(domain2call, 'retailprice')
                    #     if rpfromdomain != '' and rpfromdomain is not None:
                    #         retailprice = rootdetails.xpath(rpfromdomain)[0].text.strip()
                    #     cpfromdomain = self.getMappingFromDB(domain2call, 'curprice')
                    #     if cpfromdomain != '' and cpfromdomain is not None:
                    #         curprice = rootdetails.xpath(cpfromdomain)[0].text.strip()
                    #     bpfromdomain = self.getMappingFromDB(domain2call, 'bestprice')
                    #     if bpfromdomain != '' and bpfromdomain is not None:
                    #         bestprice = rootdetails.xpath(bpfromdomain)[0].text.strip()
                    # except Exception as e:
                    #     print(e)
                    #
                    # self.inscols += "`" + "description" + "`, "
                    # self.insvals += "'" + self.cfgmain.escape_data(str(description)) + "', "
                    # self.updcolsvals += "`" + "description" + "` = '" + self.cfgmain.escape_data(str(description)) + "', "
                    #
                    # self.inscols += "`" + "retailprice" + "`, "
                    # self.insvals += "'" + self.cfgmain.escape_data(str(retailprice)) + "', "
                    # self.updcolsvals += "`" + "retailprice" + "` = '" + self.cfgmain.escape_data(str(retailprice)) + "', "
                    #
                    # self.inscols += "`" + "curprice" + "`, "
                    # self.insvals += "'" + self.cfgmain.escape_data(str(curprice)) + "', "
                    # self.updcolsvals += "`" + "curprice" + "` = '" + self.cfgmain.escape_data(str(curprice)) + "', "
                    #
                    # self.inscols += "`" + "bestprice" + "`, "
                    # self.insvals += "'" + self.cfgmain.escape_data(str(bestprice)) + "', "
                    # self.updcolsvals += "`" + "bestprice" + "` = '" + self.cfgmain.escape_data(str(bestprice)) + "', "
                    #
                    # if self.jobsinfeed == 0:
                    #     self.colsfromfeed = self.colsfromfeed + "`" + "description" + "`, "
                    #     self.colsfromfeed = self.colsfromfeed + "`" + "retailprice" + "`, "
                    #     self.colsfromfeed = self.colsfromfeed + "`" + "curprice" + "`, "
                    #     self.colsfromfeed = self.colsfromfeed + "`" + "bestprice" + "`, "

                    self.inscols += "`" + "existinfeed" + "`"
                    self.insvals += "'" + "1" + "'"
                    self.updcolsvals += "`existinfeed` = '" + "2" + "'"

                    self.inscols += ", `" + "job_feed_id" + "`"
                    self.insvals += ", '" + self.jobfeedid + "'"
                    self.updcolsvals += ", `job_feed_id` = '" + self.jobfeedid + "'"

                    insstatement = "INSERT INTO " + self.tablename + " (" \
                                   + self.inscols + ")"
                    insstatement += " VALUES(" + self.insvals + ")"
                    insstatement += " ON DUPLICATE KEY UPDATE " + self.updcolsvals + ";"

                    if self.debug and self.debuglevel >= 0:
                        print(self.inscols)
                        print(self.insvals)
                        print(self.updcolsvals)
                        print(self.colsfromfeed)
                        print(insstatement)

                    self.insItemsStatement(handler, insstatement)

                    self.jobsinfeed += 1

                    self.inscols = ''
                    self.insvals = ''
                    self.updcolsvals = ''

                    # soups = BeautifulSoup(lxml.html.tostring(item), "html.parser")

                    # print(soups.prettify())

                    # print(soups.find("a", class_="gs-title")['href'])
                    # print(soups.find("a", class_="gs-title").text)

                    # /div[@class='gsc-thumbnail-inside']
                    # print(item[0][0][0][0].text)

                # for item in root.xpath("//tr[@class='jobResultItem']/td/div/a[@class='jobTitle']"):
                # for item in root.xpath("//div[@class='gsc-webResult gsc-result']"):
                #     print(item.prettify())

        except Exception as e:
            print(e)

        print("Jobs in feed -> " + str(self.jobsinfeed))

        self.colsfromfeed = self.colsfromfeed[:-2]

        if self.debug and self.debuglevel >= 9:
            print(self.colsfromfeed)
            print(self.inscols)
            print(self.insvals)
            print(self.updcolsvals)

        currenttime = datetime.now()
        print(currenttime)

        time1 = currenttime - start

        self.getJobsFiguresFromTables(handler)

        self.processDBJobsTables(handler, self.colsfromfeed, delete = 'donotdelete')

        self.getJobsInDB(handler)
        jobsindbafter = self.jobsindb

        currenttime = datetime.now()
        print(currenttime)

        # time2 = currenttime - start

        self.updHandlersTable(handler)

        currenttime = datetime.now()
        print(currenttime)

        time = currenttime - start

        print(currenttime - start)

        if self.debug and self.debuglevel >= 9:
            print("updated " + str(self.updatedjobs))
            print("inserted " + str(self.insertedjobs))
            print("deleted " + str(self.deletedjobs))
            print("after " + str(jobsindbafter))

        self.emailvars['rss_check'] = self.rss_check
        self.emailvars['database_check'] = self.database_check
        self.emailvars['jobsindbinit'] = jobsindb
        self.emailvars['jobsinfeed'] = self.jobsinfeed
        self.emailvars['jobsupdated'] = self.updatedjobs
        self.emailvars['jobsinserted'] = self.insertedjobs
        self.emailvars['jobsdeleted'] = self.deletedjobs
        self.emailvars['jobsindb'] = jobsindbafter
        self.emailvars['time1step'] = time1
        self.emailvars['time2step'] = time
        self.emailvars['time3end'] = time

        self.cfg.sendEmail(handler, self.emailvars)
