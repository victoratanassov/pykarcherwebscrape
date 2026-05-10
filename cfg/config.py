# -*- coding: utf-8 -*-

import gc
import html
import os
import re
# from w3lib.html import replace_entities

# pip install cryptography==35.0 - compatible with Python 3.6.0 !!!!!!!!!!!!!!!!

from cryptography.fernet import Fernet
import pymysql.cursors

# pip install secure-smtplib -> You do not have to install it. You can import it and use it without really trying to install it. If it is essential to install the module, then use the command
import smtplib
from email.mime.text import MIMEText

import sys
import subprocess
from urllib.parse import quote_plus

import zipfile
from io import BytesIO

from dbutils.pooled_db import PooledDB

if sys.version_info[0] == 2:
    reload(sys)  # noqa: F821
    sys.setdefaultencoding('UTF8')


class Config():
    debug = False
    debuglevel = 0
    hostname = ''
    username = ''
    password = ''
    database = ''
    warehousedb = ''
    dbname = 'vpws_main'
    sqlalchemyconnstr = ''
    key = ''
    variables = {}
    emailparams = {}
    handlerparams = {}
    outtags = ''
    outconditions = {}
    postcodetags = {}
    postcodecount = 0
    emailhost = ''
    encryptedemailpass = ''

    email1 = 'noreply@mobileship.eu'
    email2 = 'techsupport@vacancygroup.com'

    defaultfromemail = 'noreply@mobileship.eu'
    defaultFromName = 'NoReply'
    defaulttoemail = 'victor.atanassov@gmail.com'
    defaultrewriteurl = 'http://vprs.co.uk'
    defaultservertype = ''

    apppath = ''

    imgpath = ''
    imgpathdb = ''
    website = ''
    websitepath = ''

    imgpathdesc = ''
    imgpathdbdesc = ''
    websitedesc = ''
    websitepathdesc = ''

    myConnection = ''
    myConnectionMain = ''

    def __init__(self, dbname='vpws_main', debug=False, debuglevel=0):
        self.debug = debug
        self.debuglevel = debuglevel
        self.dbname = dbname
        encryptedpwd = ''

        pathtokeyfiles = ''
        techcleaenv = ''

        if os.path.isfile('/home/mobilesh/msh_airlines/key.bin'):
            pathtokeyfiles = '/home/mobilesh/msh_airlines/'

        if os.path.isfile('/home/techclea/pythont/key.bin') and os.path.abspath(os.getcwd()) == "/home/techclea/pythont":
            pathtokeyfiles = '/home/techclea/pythont/'
            techcleaenv = 'test'

        if os.path.isfile('/home/techclea/python/key.bin') and os.path.abspath(os.getcwd()) == "/home/techclea/python":
            pathtokeyfiles = '/home/techclea/python/'
            techcleaenv = 'prod'

        # if os.path.isfile('key.bin'):
        #     pathtokeyfiles = ''

        if self.debug and self.debuglevel >= 0:
            print(os.path.isfile(pathtokeyfiles + 'key.bin'))
            print(os.path.isfile('key.bin'))
            print(os.path.dirname(os.path.abspath(__file__)))
            print(os.path.abspath(os.getcwd()))
            print(os.path.dirname(os.path.realpath(__file__)))
            print("pathtokeyfiles -> " + str(pathtokeyfiles))
            print("techcleaenv -> " + str(techcleaenv))

        if os.path.isfile(pathtokeyfiles + 'key.bin'):
            with open(pathtokeyfiles + 'key.bin', 'rb') as file_object:
                for line in file_object:
                    self.key = line

        if self.debug and self.debuglevel >= 0:
            print(self.key)

        cipher_suite = Fernet(self.key)
        if os.path.isfile(pathtokeyfiles + 'mypvstore.bin'):
            with open(pathtokeyfiles + 'mypvstore.bin', 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line

        if self.debug and self.debuglevel >= 0:
            print(encryptedpwd)

        if encryptedpwd != '':
            uncipher_text = (cipher_suite.decrypt(encryptedpwd))
            # convert to string
            mysqlpass = bytes(uncipher_text).decode("utf-8")

        if self.debug and self.debuglevel >= 0:
            print(encryptedpwd)

        if os.path.isfile(pathtokeyfiles + 'prodpvstore.bin'):
            with open(pathtokeyfiles + 'prodpvstore.bin', 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line

        if self.debug and self.debuglevel >= 0:
            print(encryptedpwd)

        if encryptedpwd != '':
            uncipher_text = (cipher_suite.decrypt(encryptedpwd))
            # convert to string
            mysqlpassprod = bytes(uncipher_text).decode("utf-8")

        if os.path.isfile(pathtokeyfiles + 'prodpvstorevpws.bin'):
            with open(pathtokeyfiles + 'prodpvstorevpws.bin', 'rb') as file_object:
                for line in file_object:
                    encryptedpwd = line

        if self.debug and self.debuglevel >= 0:
            print(encryptedpwd)

        if encryptedpwd != '':
            uncipher_text = (cipher_suite.decrypt(encryptedpwd))
            # convert to string
            mysqlpassprodvpws = bytes(uncipher_text).decode("utf-8")

        if os.path.isfile(pathtokeyfiles + 'myepvstore.bin'):
            with open(pathtokeyfiles + 'myepvstore.bin', 'rb') as file_object:
                for line in file_object:
                    self.encryptedemailpass = line

        if self.encryptedemailpass != '':
            uncipher_text = (cipher_suite.decrypt(self.encryptedemailpass))
            # convert to string
            self.encryptedemailpass = bytes(uncipher_text).decode("utf-8")
            # print(self.encryptedemailpass)

        # print(mysqlpass)
        # if sys.version_info[0] == 2:
        #     self.hostname = 'localhost'
        #     self.username = 'root'
        #     self.password = mysqlpassprod
        #     self.database = dbname
        # else:

        print(os.uname()[1])
        if os.uname()[1] == 'ip-10-20-14-173.eu-west-2.compute.internal':
            self.hostname = 'djgrs01-db.cfwm468agx4u.eu-west-2.rds.amazonaws.com'
            self.username = 'dbadmin'
            self.password = mysqlpassprod
            self.database = dbname
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database
        elif os.uname()[1] == 'ip-10-10-13-170.eu-west-2.compute.internal':
            # self.hostname = 'localhost'
            # self.username = 'root'
            self.hostname = 'vpws01-db.cssii6vgokfc.eu-west-2.rds.amazonaws.com'
            self.username = 'dbadmin'
            self.password = mysqlpassprodvpws
            self.database = dbname
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database
        elif os.uname()[1] == 'pilot.superhosting.bg' or os.uname()[1] == 'rodina.ns1.bg':
            self.hostname = 'localhost'
            self.username = 'mobilesh_airlines'
            self.password = mysqlpassprod
            self.database = 'mobilesh_borotest'
            self.warehousedb = 'mobilesh_borotest'
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database
        elif os.uname()[1] == 'asparuh.ns1.bg' and techcleaenv == 'test':
            self.hostname = 'localhost'
            self.username = 'techclea_waret'
            self.password = mysqlpassprod
            self.database = 'techclea_feedt'
            self.warehousedb = 'techclea_waret'
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database
        elif os.uname()[1] == 'asparuh.ns1.bg' and techcleaenv == 'prod':
            self.hostname = 'localhost'
            self.username = 'techclea_ware'
            self.password = mysqlpassprod
            self.database = 'techclea_feed'
            self.warehousedb = 'techclea_ware'
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database
        elif os.uname()[1] == 'mail.bg':
            self.hostname = 'localhost'
            self.username = 'root'
            self.password = mysqlpassprod
            self.database = 'db_main'
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database
        else:
            self.hostname = 'localhost'
            self.username = 'root'
            self.password = mysqlpass
            self.database = dbname
            self.sqlalchemyconnstr = 'mysql+pymysql://' + self.username + ':' + quote_plus(self.password) + '@' + self.hostname + '/' + self.database

        if self.debug and self.debuglevel >= 0:
            print(self.hostname)
            print(self.username)
            print(self.password)
            print(self.database)
            print(self.sqlalchemyconnstr)

        try:
            self.myConnectionMain = PooledDB(
                creator=pymysql,                                # the module that creates the underlying connections
                host=self.hostname,
                user=self.username,
                password=self.password,
                database=self.database,
                autocommit=True,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                maxconnections = 10,                            # maximum number of connections in the pool
                mincached = 2,                                  # minimum number of idle connections in the pool
                maxcached = 5,                                  # maximum number of idle connections in the pool
                maxusage = 100,                                 # maximum number of reuses for a connection
                blocking = True,                                # block and wait if no connections are available
                ping = 1                                        # ping MySQL server to check if connection is alive
            )
        except Exception as e:
            self.defaultservertype = str(os.uname()[1])
            self.sendErrorEmail({'jobfeed_id': 'MYSQL Connection failed!'}, e)
            exit(1)

        try:
            self.myConnection = pymysql.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                db=self.database,
                charset='utf8mb4',
                autocommit=True,
                cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            self.defaultservertype = str(os.uname()[1])
            self.sendErrorEmail({'jobfeed_id': 'MYSQL Connection failed!'}, e)
            exit(1)

        self.loadConfigParameters('global')
        self.defaultfromemail = self.variables['global']['emailfrom']
        self.defaulttoemail = self.variables['global']['emailto']
        self.defaultrewriteurl = self.variables['global']['rewriteurl']
        self.defaultservertype = self.variables['global']['servertype']
        self.emailhost = self.variables['global']['emailhost']
        self.imgpath = self.variables['global']['imgpath']
        self.imgpathdb = self.variables['global']['imgpathdb']
        self.website = self.variables['global']['website']
        self.websitepath = self.variables['global']['websitepath']
        self.imgpathdesc = self.variables['global']['imgpathdesc']
        self.imgpathdbdesc = self.variables['global']['imgpathdbdesc']
        self.websitedesc = self.variables['global']['websitedesc']
        self.websitepathdesc = self.variables['global']['websitepathdesc']
        self.apppath = self.variables['global']['apppath']

    def __del__(self):
        gc.collect()
        if self.myConnection.open:
            self.myConnection.close()
        self.closeMySqlPool()

    def closeMySqlPool(self):
        self.myConnectionMain.close()

    def loadConfigParameters(self, idxsection):
        try:
            handlersconn = self.myConnectionMain.connection()
            handlers = handlersconn.cursor()
            handlerstmnt = 'SELECT idxkey, idxvalue FROM vpwsconfig WHERE idxsection = \'' + idxsection + '\';'
            handlers.execute(handlerstmnt)

            self.variables[idxsection] = {}

            for handler in handlers.fetchall():
                self.variables[idxsection][handler['idxkey']] = handler['idxvalue']
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def getvpwsconfig(self, idxsection, idxkey):
        if self.debug:
            print(self.variables[idxsection][idxkey])
        return self.variables[idxsection][idxkey]

    def setvpwsconfig(self, idxsection, idxkey, idxvalue):
        self.variables[idxsection][idxkey] = idxvalue
        self.updatevpwsconfig(idxsection, idxkey)

    def updatevpwsconfig(self, idxsection, idxkey):
        if self.debug:
            print(self.variables[idxsection][idxkey])
        try:
            handlersconn = self.myConnectionMain.connection()
            handlers = handlersconn.cursor()
            handlerstmnt = 'UPDATE vpwsconfig SET idxvalue = \'' \
                           + str(self.variables[idxsection][idxkey]) \
                           + '\' WHERE idxsection = \'' \
                           + idxsection + '\' and idxkey = \'' \
                           + idxkey + '\';'
            handlers.execute(handlerstmnt)
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def loadHandlerParameters(self, handler):
        try:
            handlersconn = self.myConnectionMain.connection()
            handlers = handlersconn.cursor()
            handlerstmnt = 'SELECT active, jobfeedurl, tablename, sendemails, ' \
                           'emailsto, emailssubject, emailsbody FROM ' \
                           'handlers WHERE jobfeed_id = \'' + handler + '\';'
            handlers.execute(handlerstmnt)

            self.emailparams['handlerid'] = handler

            for handler in handlers.fetchall():
                self.handlerparams['active'] = handler['active']
                self.handlerparams['tablename'] = handler['tablename']
                self.handlerparams['sendemails'] = handler['sendemails']
                self.handlerparams['emailsto'] = handler['emailsto']
                self.handlerparams['emailssubject'] = handler['emailssubject']
                self.handlerparams['emailsbody'] = handler['emailsbody']
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def queryDB(self, sqlStatement):
        resp = False
        try:
            handlersconn = self.myConnectionMain.connection()
            handlers = handlersconn.cursor()
            resp = handlers.execute(sqlStatement)
        except pymysql.Error as e:
            print(e)
        finally:
            handlersconn.close()                                # returns the connection to the pool
            return resp

    def lockExec(self, type, action, jobfeed_id, locking, feed_id=""):
        tablename = "handlers"
        typestmnt = ""
        if type == "feed":
            tablename = "feeds"
            typestmnt = " and action = '" + action + "' and feed_id = '" + feed_id + "'"
        updstmnt = "UPDATE " + tablename + " SET locks = " + str(locking) + " WHERE jobfeed_id = '" + jobfeed_id + "'" + typestmnt + ";"
        # print(updstmnt)
        self.queryDB(updstmnt)

    def escape_data(self, data):
        if data is not None:
            data = self.myConnection.escape_string(data)
            return data
        else:
            return ''

    def html_unescape(self, job_feed_id = '', parameter = '', htmlval = ''):
        returnval = html.unescape(htmlval)
        if self.debug:
            print('html_unescape -> returnval -> ' + returnval)
        return returnval

    def emailReplace(self, text):
        text = text.replace("%MULTIPLE%",
                            (self.emailparams['multiple'] if
                             self.emailparams['multiple'] is
                             not None else ""))
        text = text.replace("%JOBSFEED_ID%",
                            (self.emailparams['handlerid'] if
                             self.emailparams['handlerid'] is
                             not None else ""))
        text = text.replace("%HANDLER_NAME%",
                            (self.emailparams['handlername'] if
                             self.emailparams['handlername'] is
                             not None else ""))
        text = text.replace("%ACTION%",
                            (self.emailparams['action'] if
                             self.emailparams['action'] is
                             not None else ""))
        # text = text.replace("%RSS_CHECK%", self.emailparams['rss_check'])
        # text = text.replace("%DATABASE_CHECK%",
        #                     self.emailparams['database_check'])
        # text = text.replace("%UPLOAD_STATUS%",
        #                     self.emailparams['uploadstatus'])
        text = text.replace("%JOBS_IN_DB_INIT%",
                            (self.emailparams['jobsindbinit'] if
                             self.emailparams['jobsindbinit'] is
                             not None else ""))
        text = text.replace("%JOBS_IN_FEED%",
                            (self.emailparams['jobsinfeed'] if
                             self.emailparams['jobsinfeed'] is
                             not None else ""))
        text = text.replace("%JOBS_INSERTED%",
                            (self.emailparams['jobsinserted'] if
                             self.emailparams['jobsinserted'] is
                             not None else ""))
        text = text.replace("%JOBS_UPDATED%",
                            (self.emailparams['jobsupdated'] if
                             self.emailparams['jobsupdated'] is
                             not None else ""))
        # text = text.replace("%JOBS_DELETED%",
        #                     self.emailparams['jobsdeleted'])
        # text = text.replace("%JOBS_IN_DB%",
        #                     (self.emailparams['jobsindb'] if
        #                      self.emailparams['jobsindb'] is
        #                      not None else ""))
        text = text.replace("%EXECUTION_TIME%",
                            (self.emailparams['time3end'] if
                             self.emailparams['time3end'] is
                             not None else ""))
        text = text.replace("%INSERTED_ROWS%",
                            (self.emailparams['insertedrows'] if
                             self.emailparams['insertedrows'] is
                             not None else ""))
        text = text.replace("%UPDATED_ROWS%",
                            (self.emailparams['updatedrows'] if
                             self.emailparams['updatedrows'] is
                             not None else ""))

        return text

    def sendEmail(self, handler, emailvars):
        # self.debug = True
        # self.debuglevel = 0
        #
        if self.debug and self.debuglevel >= 0:
            print(handler)
            print(emailvars)

        if self.debug and self.debuglevel >= 0:
            print(handler['emailsbody'])

        emailvars['handlerid'] = handler['jobfeed_id']
        try:
            if 'handlername' in emailvars:
                if emailvars['handlername'] == '':
                    emailvars['handlername'] = 'tribepad'
            if 'handlerfeed' in emailvars:
                if emailvars['handlerfeed'] == '' and handler['upload'] == 1:
                    emailvars['handlerfeed'] = handler['jobfeedurl']
        except Exception as e:
            print(e)
        emailvars['action'] = 'ups'
        emailvars['uploadstatus'] = ''

        emailvars['emailto'] = handler['emailsto']
        emailvars['emailsubject'] = handler['emailssubject']
        emailvars['emailbody'] = handler['emailsbody']

        if self.debug and self.debuglevel >= 0:
            print(emailvars)

        self.insertIntoHandlerStatus(emailvars)
        if handler['sendemails'] == 1:
            if self.debug and self.debuglevel >= 0:
                print(emailvars['emailbody'])

            emailvars['emailbody'] = self.emailBodyParametersReplace(emailvars, emailvars['emailbody'])
            emailvars['emailsubject'] = self.emailBodyParametersReplace(emailvars,
                                                                                emailvars['emailsubject'])
            if self.debug and self.debuglevel >= 0:
                print(emailvars)
                print(emailvars['emailbody'])

            if emailvars['emailto'] is not None:
                sendToEmail = emailvars['emailto'].split(',')
            else:
                sendToEmail = ''
            htmloutput = "MIME - Version: 1.0\r\nContent - type: text / html"
            myoutput = "Subject: " + emailvars['emailsubject'] + "\r\n\r\n" + emailvars['emailbody']

            if self.debug and self.debuglevel >= 0:
                print(sendToEmail)
                if len(sendToEmail) >= 1:
                    print(sendToEmail[0][0:(sendToEmail[0].find("@"))])

            if (sys.version_info[0] == 3):
                try:
                    print(self.emailhost)
                    if self.emailhost == 'localhost':
                        s = smtplib.SMTP(self.emailhost)
                    else:
                        s = smtplib.SMTP(self.emailhost, 587)
                        s.starttls()
                        s.ehlo()
                        s.login(self.defaultfromemail, self.encryptedemailpass)

                    if self.debug and self.debuglevel >= 0:
                        myoutput1 = "From: " + self.email1[0:(self.email1.find("@"))] + " <" + self.email1 + ">\r\n" + "To: " + self.email2[0:(self.email2.find("@"))] + " <" + self.email2 + ">\r\n" + htmloutput + "\r\n" + myoutput
                        # s.sendmail(self.email1, self.email2, myoutput1)
                        if self.debug and self.debuglevel >= 0:
                            print(myoutput1)

                        msg = MIMEText(emailvars['emailbody'], 'html')
                        msg['Subject'] = emailvars['emailsubject']
                        msg['From'] = self.email1
                        msg['To'] = self.email2

                        print(myoutput1)
                        print(msg)
                        print(self.email1)
                        print(self.email2)

                        s.sendmail(self.email1, self.email2, msg.as_string())
                    else:
                        for emlTo in sendToEmail:
                            print(emlTo)
                            myoutput1 = "From: " + self.email1[0:(self.email1.find("@"))] + " <" + self.email1 + ">\r\n" + "To: " + emlTo[0:(emlTo.find("@"))] + " <" + emlTo + ">\r\n" + htmloutput + "\r\n" + myoutput
                            # s.sendmail(self.email1, emlTo, myoutput1)
                            # s.sendmail(self.email1, self.email2, myoutput)
                            if self.debug and self.debuglevel >= 0:
                                print(myoutput1)

                            msg = MIMEText(emailvars['emailbody'], 'html')
                            msg['Subject'] = emailvars['emailsubject']
                            msg['From'] = self.email1
                            msg['To'] = emlTo

                            print(myoutput1)
                            print(msg)
                            print(self.email1)
                            print(emlTo)

                            s.sendmail(self.email1, emlTo, msg.as_string())

                    s.quit()
                except Exception as exception:
                    print('except:')
                    print(myoutput)
                    print(exception)
                # finally:
                #     print('finally:')
                #     print(myoutput)
            else:
                print(myoutput)

    def writeToLog(self):
        insHS = "INSERT INTO `handlers_status`(`handlerid`, `handlername`, " \
                "`handlerfeed`, `action`, `jobsindbinit`, `jobsinfeed`, " \
                "`jobsexist`, `jobsupdated`, `jobsinserted`, `jobsdeleted`," \
                "`jobsindb`, `time1step`, `time2step`, `time3end`) VALUES"
        insHS = insHS + "('" + self.emailparams['handlerid'] + "', '" \
            + (self.emailparams['handlername']
               if self.emailparams['handlername'] is not None
               else "") + "', '" \
            + (self.emailparams['requesturl']
               if self.emailparams['requesturl'] is not None
               else "") + "', '" \
            + (self.emailparams['action']
               if self.emailparams['action'] is not None
               else "") + "', " \
            + (self.emailparams['jobsindbinit']
               if self.emailparams['jobsindbinit'] is not None
               else "") + ", " \
            + (self.emailparams['jobsinfeed']
               if self.emailparams['jobsinfeed'] is not None
               else "") + ", " \
            + "null" + ", " \
            + (self.emailparams['jobsinserted']
               if self.emailparams['jobsinserted'] is not None
               else "") + ", " \
            + (self.emailparams['jobsupdated']
               if self.emailparams['jobsupdated'] is not None
               else "") + ", " \
            + "null" + ", " \
            + (self.emailparams['jobsinfeed']
               if self.emailparams['jobsinfeed'] is not None
               else "") + ", " \
            + self.emailparams['time1step'] + ", " \
            + self.emailparams['time2step'] + ", " \
            + self.emailparams['time3end'] + ");"

        if self.debug:
            print(insHS)

        try:
            rowcount = self.queryDB(insHS)
            if self.debug:
                print('Updates: ' + str(rowcount))
        except pymysql.Error as e:
            print(e)

    def insertIntoHandlerStatus(self, inArr, tableName = "handlers_status"):
        if 'handlername' not in inArr:
            inArr['handlername'] = ''
        if 'handlerfeed' not in inArr:
            inArr['handlerfeed'] = ''
        sqlstmnt = "INSERT INTO `" + tableName + "`(`handlerid`, `handlername`, `handlerfeed`, `action`, `jobsindbinit`, `jobsinfeed`, `jobsexist`, `jobsupdated`, `jobsinserted`, `jobsdeleted`, `jobsindb`, `time1step`, `time2step`, `time3end`) "
        sqlstmnt += " VALUES ('" + inArr['handlerid'] + "', '" + inArr['handlername'] + "', '" + inArr['handlerfeed'] + "', '" + inArr['action'] + "', " + str(inArr['jobsindbinit'] if inArr['jobsindbinit'] != 0 and inArr['jobsindbinit'] is not None else 0) + ", " + str(inArr['jobsinfeed'] if inArr['jobsinfeed'] != 0 and inArr['jobsinfeed'] is not None else 0) + ", " + str(inArr['jobsinfeed'] if inArr['jobsinfeed'] != 0 and inArr['jobsinfeed'] is not None else 0) + ", " + str(inArr['jobsupdated'] if inArr['jobsupdated'] != 0 and inArr['jobsupdated'] is not None else 0) + ", " + str(inArr['jobsinserted'] if inArr['jobsinserted'] != 0 and inArr['jobsinserted'] is not None else 0) + ", " + str(inArr['jobsdeleted'] if inArr['jobsdeleted'] != 0 and inArr['jobsdeleted'] is not None else 0) + ", " + str(inArr['jobsindb'] if inArr['jobsindb'] != 0 and inArr['jobsindb'] is not None else 0) + ", " + str(float(str(inArr['time1step']).replace(":", ""))) + ", " + str(float(str(inArr['time2step']).replace(":", ""))) + ", " + str(float(str(inArr['time3end']).replace(":", ""))) + ");"

        if self.debug:
            print(sqlstmnt)

        try:
            rowcount = self.queryDB(sqlstmnt)
            if self.debug:
                print('Inserted : ' + str(rowcount))
        except pymysql.Error as e:
            print(e)

    def emailBodyParametersReplace(self, inArr, body):
        body = body.replace("%JOBSFEED_ID%",        inArr['handlerid'])
        body = body.replace("%HANDLER_NAME%",       inArr['handlername'])
        body = body.replace("%ACTION%",             inArr['action'])
        body = body.replace("%RSS_CHECK%",          inArr['rss_check'])
        body = body.replace("%DATABASE_CHECK%",     inArr['database_check'])
        body = body.replace("%UPLOAD_STATUS%",      inArr['uploadstatus'])
        body = body.replace("%JOBS_IN_DB_INIT%",    str(inArr['jobsindbinit']))
        body = body.replace("%JOBS_IN_FEED%",       str(inArr['jobsinfeed']))
        body = body.replace("%JOBS_INSERTED%",      str(inArr['jobsinserted']))
        body = body.replace("%JOBS_UPDATED%",       str(inArr['jobsupdated']))
        body = body.replace("%JOBS_DELETED%",       str(inArr['jobsdeleted']))
        body = body.replace("%JOBS_IN_DB%",         str(inArr['jobsindb']))
        body = body.replace("%EXECUTION_TIME%",     str(inArr['time3end']))
        if 'resplist' in inArr:
            body = body.replace("%RESPLIST%", str(inArr['resplist']))
        if 'feedid' in inArr:
            body = body.replace("%FEED_ID%", inArr['feedid'])
        if 'company' in inArr:
            body = body.replace("%CVLIB_COMPANY%",  inArr['company'])
        if 'notprocessed' in inArr:
            body = body.replace("%JOBS_NOT_PROCESSED%", str(inArr['notprocessed']))
        if 'jobserrors' in inArr:
            body = body.replace("%JOBS_ERRORS%",       str(inArr['jobserrors']))

        return body

    def getJbMapping(self, jobboard, clientid, tableAlias, jbmaptable="feed_jbmap"):
        self.outtags = ''
        self.outconditions = {}
        self.postcodetags = {}
        try:
            handlersconn = self.myConnectionMain.connection()
            mysqlcon = handlersconn.cursor()

            if jobboard != "":
                jbmapmysqlst = "SELECT tagenabled, intag, outtag, outconditions, fixed FROM " + jbmaptable + " WHERE (tagenabled = 1 or tagenabled = 2) and jbid = '" + jobboard + "' and clid = '" + clientid + "' ORDER BY tagorder, id;"
            else:
                jbmapmysqlst = "SELECT tagenabled, intag, outtag, outconditions, fixed FROM " + jbmaptable + " WHERE (tagenabled = 1 or tagenabled = 2) and clid = '" + clientid + "' ORDER BY tagorder, id;"

            if self.debug:
                print(jbmapmysqlst)

            rowcount = mysqlcon.execute(jbmapmysqlst)
            if self.debug:
                print('Selected : ' + str(rowcount))

            postcodecnt = 0

            for retrow in mysqlcon.fetchall():
                intag = retrow['intag']
                outtag = retrow['outtag']
                tagenabled = retrow['tagenabled']
                fixed = retrow['fixed']
                add2intag = ''
                if outtag[0:1] == '@':
                    print('out tag found @ -> ' + outtag)
                    add2intag = "@rolesummary := "
                    outtag = outtag[1:]
                if self.debug:
                    print(retrow)
                if tagenabled == 1:
                    if intag is None:
                        if fixed is not None:
                            self.outtags += add2intag + "'" + fixed.strip() + "' as `" + outtag + "`, "
                        else:
                            self.outtags += add2intag + "null as `" + outtag + "`, "
                    else:
                        if fixed is not None:
                            self.outtags += add2intag + "'" + fixed.strip() + "' as `" + outtag + "`, "
                        else:
                            self.outtags += add2intag + ("" if "(" in intag else tableAlias + ".`") + intag + ("" if "(" in intag else "`") + " as " + "`" + outtag + "`, "
                if tagenabled == 2:
                    self.postcodetags[postcodecnt, 'intag'] = intag
                    self.postcodetags[postcodecnt, 'outtag'] = outtag
                    if self.postcodetags[postcodecnt, 'intag'] == 'town':
                        self.postcodetags[postcodecnt, 'replfld'] = 'globalcity'
                    else:
                        if self.postcodetags[postcodecnt, 'intag'] == 'county':
                            self.postcodetags[postcodecnt, 'replfld'] = 'globalregion'
                        else:
                            if self.postcodetags[postcodecnt, 'intag'] == 'country':
                                self.postcodetags[postcodecnt, 'replfld'] = 'globalcountry'
                            else:
                                self.postcodetags[postcodecnt, 'replfld'] = ''
                    postcodecnt += 1
                self.postcodecount = postcodecnt

                tag = outtag
                self.outconditions[tag] = retrow['outconditions']

            self.outtags = self.outtags[0:-2]

            if self.debug:
                print(self.outtags)
                print(self.outconditions)
                print(self.postcodetags)
        finally:
            handlersconn.close()                                # returns the connection to the pool

    def validate_domain_name(self, domain_name):
        # Check the overall length of the domain name, should not exceed 253 characters
        if len(domain_name) > 253:
            return False

        # Regular expression pattern to validate domain name:
        #   - (?!-) ensures that the label doesn't start with a hyphen
        #   - [A-Za-z0-9-]{1,63} ensures that the label contains 1 to 63 alphanumeric characters or hyphens
        #   - (?<!-) ensures that the label doesn't end with a hyphen
        #   - \. matches a dot between labels
        #   - [A-Za-z]{2,} matches a two or more character top-level domain (TLD)
        pattern = r'^((?!-)[A-Za-z0-9-]{1,63}(?<!-)\.)+[A-Za-z]{2,}$'

        # Check if the domain name matches the pattern
        if re.match(pattern, domain_name):
            return True
        else:
            return False

    def hours2text(self, job_feed_id, parameter, hours):
        # self.debug = True
        parttime = 'Part time'
        fulltime = 'Full time'
        if re.sub("[^0-9]", '', hours) != '':
            getint = int(re.sub("[^0-9]", '', hours))
        else:
            getint = 0

        try:
            handlersconn = self.myConnectionMain.connection()
            mysqlcon = handlersconn.cursor()

            if self.debug:
                print("hours -> " + str(hours))

            getparamsmysqlst = "SELECT keyid, value, auxvalue FROM handlers_feedopts WHERE paramtype = 'workinghours' and keyindex = '" + parameter + "' and job_feed_id = '" + job_feed_id + "';"

            if self.debug:
                print(getparamsmysqlst)

            try:
                rowcount = mysqlcon.execute(getparamsmysqlst)
                if self.debug:
                    print('Selected : ' + str(rowcount))
            except pymysql.Error as e:
                print(e)

            auxvalue = ""

            for retrow in mysqlcon.fetchall():
                if self.debug:
                    print(retrow)
                if retrow['keyid'] == 0:
                    fulltime = retrow['value']
                if retrow['keyid'] == 1:
                    parttime = retrow['value']
                auxvalue = retrow['auxvalue']
        finally:
            handlersconn.close()  # returns the connection to the pool

        if eval(str(getint) + " " + auxvalue):
            return parttime
        else:
            return fulltime

    def valid_xml_char_ordinal(c):
        codepoint = ord(c)
        # conditions ordered by presumed frequency
        return (
            0x20 <= codepoint <= 0xD7FF or
            codepoint in (0x9, 0xA, 0xD) or
            0xE000 <= codepoint <= 0xFFFD or
            0x10000 <= codepoint <= 0x10FFFF
            )

    def sendErrorEmail(self, handler={'jobfeed_id': ''}, errorMessage='', auxerror=''):
        if 'jobfeed_id' in handler:
            if self.debug and self.debuglevel >= 0:
                print(handler['jobfeed_id'])
        else:
            handler['jobfeed_id'] = ''
        subject = str("Subject: [" + self.defaultservertype) + "] Error with execution of " + str(handler['jobfeed_id'])
        emailbody = str(errorMessage) + "<br>\n<br>\n<br>\n" + str(auxerror)
        htmloutput = "MIME - Version: 1.0\r\nContent - type: text / html"
        myoutput = subject + "\r\n\r\n" + emailbody

        if self.debug and self.debuglevel >= 0:
            print(self.defaultfromemail)
            print(self.defaulttoemail)

        try:
            if self.emailhost == 'localhost':
                s = smtplib.SMTP(self.emailhost)
            else:
                s = smtplib.SMTP(self.emailhost, 587)
                s.starttls()
                s.ehlo()
                s.login(self.defaultfromemail, self.encryptedemailpass)

            myoutput1 = "From: " + self.defaultfromemail[
                                   0:(self.defaultfromemail.find("@"))] + " <" + self.defaultfromemail + ">\r\n" + \
                        "To: " + self.defaulttoemail[0:(
                self.defaulttoemail.find("@"))] + " <" + self.defaulttoemail + ">\r\n" + htmloutput + "\r\n" + myoutput
            #                        s.sendmail(self.email1, self.email2, myoutput1)
            if self.debug and self.debuglevel >= 0:
                print(myoutput1)

            msg = MIMEText(emailbody, 'html')
            msg['Subject'] = subject
            msg['From'] = self.defaultfromemail
            msg['To'] = self.defaulttoemail
            s.sendmail(self.defaultfromemail, self.defaulttoemail, msg.as_string())

            s.quit()
        except Exception as exception:
            print('except:')
            # print(myoutput)
            print(str(exception)[:1000])
        finally:
            print('finally:')
            # print(str(myoutput))

    def salaryBandCalc(self, job_feed_id, parameter, salary_to):
        salary = 0
        auxvalue = ""

        if isinstance(salary_to, int):
            salary = int(salary_to) * 8 * 220
        if isinstance(salary_to, float):
            salary = float(salary_to) * 8 * 220

        try:
            handlersconn = self.myConnectionMain.connection()
            mysqlcon = handlersconn.cursor()

            getparamsmysqlst = "SELECT keyid, value, auxvalue FROM handlers_feedopts WHERE paramtype = 'salaryBand' and keyindex = '" + parameter + "' and job_feed_id = '" + job_feed_id + "';"

            if self.debug:
                print(getparamsmysqlst)

            rowcount = mysqlcon.execute(getparamsmysqlst)
            if self.debug:
                print('Selected : ' + str(rowcount))

            for retrow in mysqlcon.fetchall():
                if self.debug:
                    print(retrow)

                if eval(str(salary) + " " + retrow['auxvalue']):
                    auxvalue = retrow['value']
        finally:
            handlersconn.close()  # returns the connection to the pool

        return auxvalue

    def jobtype2textNHS(self, job_feed_id = '', parameter = '', jobtype = ''):
        returnval = ''
        if job_feed_id == '00073_HCRGCAREGROUP_XML_FEED':
            if int(jobtype) == 1:
                returnval = 'permanent'
            elif int(jobtype) == 2:
                returnval = 'permanent'
            elif int(jobtype) == 3:
                returnval = 'permanent'
            elif int(jobtype) == 4:
                returnval = 'fixed-term'
            elif int(jobtype) == 5:
                returnval = 'fixed-term'
            elif int(jobtype) == 7:
                returnval = 'fixed-term'
            elif int(jobtype) == 8:
                returnval = 'fixed-term'
            elif int(jobtype) == 9:
                returnval = 'bank'
            elif int(jobtype) == 10:
                returnval = 'fixed-term'
            else:
                returnval = ''
        elif job_feed_id == '00077_RDEXTRUST_XML_FEED':
            if int(jobtype) == 1:
                returnval = 'permanent'
            elif int(jobtype) == 3:
                returnval = 'fixed-term'
            elif int(jobtype) == 4:
                returnval = 'fixed-term'
            elif int(jobtype) == 5:
                returnval = 'fixed-term'
            elif int(jobtype) == 6:
                returnval = 'bank'
            elif int(jobtype) == 7:
                returnval = 'fixed-term'
            elif int(jobtype) == 8:
                returnval = 'fixed-term'
            elif int(jobtype) == 9:
                returnval = 'fixed-term'
            elif int(jobtype) == 10:
                returnval = 'permanent'
            else:
                returnval = ''
        else:
            if int(jobtype) == 1:
                returnval = 'permanent'
            elif int(jobtype) == 2:
                returnval = 'permanent'
            elif int(jobtype) == 3:
                returnval = 'permanent'
            elif int(jobtype) == 4:
                returnval = 'fixed-term'
            elif int(jobtype) == 5:
                returnval = 'fixed-term'
            elif int(jobtype) == 6:
                returnval = 'bank'
            elif int(jobtype) == 7:
                returnval = 'fixed-term'
            elif int(jobtype) == 8:
                returnval = 'fixed-term'
            elif int(jobtype) == 9:
                returnval = 'bank'
            elif int(jobtype) == 10:
                returnval = 'fixed-term'
            else:
                returnval = ''

        if self.debug:
            print(jobtype)
            print(job_feed_id)
            print('jobtype2textNHS -> returnval -> ' + returnval)

        return returnval

    def hours2textNHS(self, job_feed_id = '', parameter = 'shift_hours', hours = ''):
        returnval = self.hours2text(job_feed_id, parameter, hours)
        if self.debug:
            print('hours2textNHS -> returnval -> ' + str(returnval))
        return returnval

    def hours2textNHSRDE(self, job_feed_id, parameter, hours):
        # self.debug = True
        if re.sub("[^0-9]", '', hours) != '':
            getint = int(re.sub("[^0-9]", '', hours))
        else:
            getint = 0

        if self.debug:
            print("hours -> " + str(hours))
            print("getint -> " + str(getint))

        return str(getint)

    def staffgrpmapping(self, job_feed_id = '', parameter = '', stgrp = ''):
        returnval = ''
        if stgrp == 'Additional Clinical Services':
            returnval = "CLINICAL_SERVICES"
        elif stgrp == 'Additional Professional, Scientific and Technical':
            returnval = "PROF_SCIENTIFIC_AND_TECHNICAL"
        elif stgrp == 'Additional Professional, Scientific &amp; Technical':
            returnval = "PROF_SCIENTIFIC_AND_TECHNICAL"
        elif stgrp == 'Administrative & Clerical':
            returnval = "ADMINISTRATIVE_AND_CLERICAL"
        elif stgrp == 'Administrative &amp; Clerical':
            returnval = "ADMINISTRATIVE_AND_CLERICAL"
        elif stgrp == 'Allied Health Professionals':
            returnval = "ALLIED_HEALTH_PROF"
        elif stgrp == 'Corporate':
            returnval = "CLINICAL_SERVICES"
        elif stgrp == 'Estates & Ancillary':
            returnval = "ESTATES_AND_ACILLARY"
        elif stgrp == 'Estates &amp Ancillary':
            returnval = "ESTATES_AND_ACILLARY"
        elif stgrp == 'Healthcare Scientists':
            returnval = "HEALTHCARE_SCIENTISTS"
        elif stgrp == 'Medical and Dental':
            returnval = "MEDICAL_AND_DENTAL"
        elif stgrp == 'Medical &amp Dental':
            returnval = "MEDICAL_AND_DENTAL"
        elif stgrp == 'Nursing and Midwifery Registered':
            returnval = "NURSING_AND_MIDWIFERY_REGD"
        elif stgrp == 'Nursing &amp Midwifery Registered':
            returnval = "NURSING_AND_MIDWIFERY_REGD"
        # Devon category_name mapping
        elif stgrp == 'Administration':
            returnval = "ADMINISTRATIVE_AND_CLERICAL"
        elif stgrp == 'Doctor jobs':
            returnval = "ALLIED_HEALTH_PROF"
        elif stgrp == 'Healthcare Assistant':
            returnval = "CLINICAL_SERVICES"
        elif stgrp == 'Human Resources':
            returnval = "ADMINISTRATIVE_AND_CLERICAL"
        elif stgrp == 'Medical':
            returnval = "MEDICAL_AND_DENTAL"
        elif stgrp == 'Midwifery':
            returnval = "NURSING_AND_MIDWIFERY_REGD"
        elif stgrp == 'Nursing':
            returnval = "NURSING_AND_MIDWIFERY_REGD"
        elif stgrp == 'Occupational Therapy':
            returnval = "CLINICAL_SERVICES"
        elif stgrp == 'Physiotherapy':
            returnval = "CLINICAL_SERVICES"
        # Everything else mapping...
        else:
            returnval = "CLINICAL_SERVICES"

        if self.debug:
            print('staffgrpmapping -> returnval -> ' + returnval)

        return returnval

    def EmploymentType2DWP(self, job_feed_id = '', parameter = '', empltype = ''):
        returnval = ''
        if empltype == 'Part Time':
            returnval = "2"
        elif empltype == 'Full Time':
            returnval = "1"
        elif empltype == 'Full & Part Time':
            returnval = "1"
        else:
            returnval = "1"

        if self.debug:
            print('empltype -> ' + empltype + '; returnval -> ' + returnval)

        return returnval

    def jobTypeTribepad2DWP(self, job_feed_id = '', parameter = '', jobtype = ''):
        # self.debug = True

        returnval = ''

#       Tesco
#       1       Permanent                     1
#       3       Part time                     3
#       4       Temporary                     3
#       5       Fixed Term                    2
#       7       Seasonal                      3
#       8       Parental Leave                3
#       9       Student Transfers             3
#       13      Apprenticeship contract       4
#       14      Graduate contract             3
#       15      Internship contract           3

# EmploymentTypeID-1    Full Time
# EmploymentTypeID-2    Part Time
# EmploymentTypeID-3    Flexi
# EmploymentTypeID-4    Home Based
# EmploymentTypeID-5    Contract

#       Compass
#       1       Full Time           EmploymentTypeID-1      Full Time
#       3       Part Time           EmploymentTypeID-2      Part Time
#       4       Temporary Casual
#       5       Fixed Term          EmploymentTypeID-5      Contract
#       7       Permanent Casual

#       Greggs
#       1       Full Time               1
#       2       Part Time               3
#       3       Students Hours          3
#       4       Temporary / Casual      3
#       5       Fixed Term              2

        if job_feed_id == '00076_TESCO_XML_FEED':
            if str(jobtype) == '1':
                returnval = '1'
            elif str(jobtype) == '3':
                returnval = '3'
            elif str(jobtype) == '4':
                returnval = '3'
            elif str(jobtype) == '5':
                returnval = '2'
            elif str(jobtype) == '7':
                returnval = '3'
            elif str(jobtype) == '8':
                returnval = '3'
            elif str(jobtype) == '9':
                returnval = '3'
            elif str(jobtype) == '13':
                returnval = '4'
            elif str(jobtype) == '14':
                returnval = '3'
            elif str(jobtype) == '15':
                returnval = '3'
        elif job_feed_id == '00084_GREGGS_XML_FEED':
            if str(jobtype) == '1':
                returnval = '1'
            if str(jobtype) == '2':
                returnval = '3'
            if str(jobtype) == '3':
                returnval = '3'
            if str(jobtype) == '4':
                returnval = '3'
            if str(jobtype) == '5':
                returnval = '2'
        elif job_feed_id == '00081_COMPASS_XML_FEED':
            if str(jobtype) == '1':
                returnval = 'EmploymentTypeID-1'
            if str(jobtype) == '3':
                returnval = 'EmploymentTypeID-2'
            if str(jobtype) == '4':
                returnval = 'EmploymentTypeID-5'
            if str(jobtype) == '5':
                returnval = 'EmploymentTypeID-5'
            if str(jobtype) == '7':
                returnval = 'EmploymentTypeID-2'
        elif job_feed_id == '00100_CARDFACTORY_XML_FEED':
            if str(jobtype) == '2':
                returnval = '1'
            if str(jobtype) == '4':
                returnval = '2'

        if self.debug:
            print('jobtype -> ' + str(jobtype) + '; returnval -> ' + str(returnval))

        return returnval

    def salaryFreqTribepad2FFJ(self, job_feed_id = '', parameter = '', salaryfreq = ''):
        returnval = ''

#       Day(3) or Month(4) or Week(6) or Year(1) or Hour(2)

        if str(salaryfreq) == '1':
            returnval = 'Year'
        elif str(salaryfreq) == '2':
            returnval = 'Hour'
        elif str(salaryfreq) == '3':
            returnval = 'Day'
        elif str(salaryfreq) == '4':
            returnval = 'Month'
        elif str(salaryfreq) == '6':
            returnval = 'Week'

        if self.debug:
            print('salaryfreq -> ' + str(salaryfreq) + '; returnval -> ' + str(returnval))

        return returnval

    def Tribepad2ArbetsCountryCode(self, job_feed_id = '', parameter = '', val = ''):
        return val

    def Tribepad2ArbetsMunicipality(self, job_feed_id = '', parameter = '', val = ''):
        return val

    def SubWay2ArbetsJobType(self, job_feed_id = '', parameter = '', val = ''):
        return val

    def SubWay2ArbetsSalaryType(self, job_feed_id = '', parameter = '', val = ''):
        return val

    def dummyone(self, job_feed_id = '', parameter = '', val = ''):
        return val

class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_zip = BytesIO()

    def append(self, filename_in_zip, file_contents):
        '''Appends a file with name filename_in_zip and contents of
        file_contents to the in-memory zip.'''
        # Get a handle to the in-memory zip in append mode
        zf = zipfile.ZipFile(self.in_memory_zip, "w", zipfile.ZIP_DEFLATED, False)

        # Write the file to the in-memory zip
        zf.writestr(filename_in_zip, file_contents)

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in zf.filelist:
            zfile.create_system = 0

        return self

    def read(self):
        '''Returns a string with the contents of the in-memory zip.'''
        self.in_memory_zip.seek(0)
        return self.in_memory_zip.read()

    def writetofile(self, filename):
        '''Writes the in-memory zip to a file.'''
        f = file(filename, "w")
        f.write(self.read())
        f.close()
