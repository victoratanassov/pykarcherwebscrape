# -*- coding: utf-8 -*-

import datetime
import sys

NEW_PATH = './cfg'
if NEW_PATH not in sys.path:
    sys.path.append(NEW_PATH)

from cfg.config import Config  # noqa: E402

NEW_PATH = './cls'
if NEW_PATH not in sys.path:
    sys.path.append(NEW_PATH)

from cls.processhandlersclass import ClassProcessHandlers  # noqa: E402
# from processfeedsclass import ClassProcessFeeds  # noqa: E402
# from processcronjobclass import ClassProcessCronjob  # noqa: E402
# from maintenance import ClassMaintenance # noqa: E402

class MainProcess:
    def __init__(self):
        print("Starting...")

    def callMainProcess(self, sysargv):
        start = datetime.datetime.now()
        print(start)

        DEBUG = False
        DEBUGLEVEL = 0
        PARAMS = ''
        ACTIVE = 4
        ACTION = ''

        SYSARGV1 = ''
        SYSARGV2 = ''
        SYSARGV3 = ''

        MAINTENANCE = 0
        ANALYZETABLES = 0
        UNLOCK = 0

        if len(sysargv) >= 2:
            if len(sysargv) >= 2:
                if sysargv[1] is not None:
                    SYSARGV1 = sysargv[1]

            if len(sysargv) >= 3:
                if sysargv[2] is not None:
                    SYSARGV2 = sysargv[2]
            if len(sysargv) >= 4:
                if sysargv[3] is not None:
                    SYSARGV3 = sysargv[3]

            if SYSARGV1 in ('checkNew', 'checknew'):
                ACTION = "chk"
                ACTIVE = 5

            if SYSARGV1 in ('updateLast', 'updatelast'):
                ACTION = "upl"
                ACTIVE = 5

            if SYSARGV1 in ('updateAll', 'updateall'):
                ACTION = "upa"
                ACTIVE = 5

            if 'debug' in (SYSARGV1, SYSARGV2, SYSARGV3):
                DEBUG = True
                DEBUGLEVEL = (int(SYSARGV2) if SYSARGV2.isdigit() else 0)
                if DEBUGLEVEL == 0:
                    DEBUGLEVEL = (int(SYSARGV3) if SYSARGV3.isdigit() else 0)

            if 'maintenance' in (SYSARGV1, SYSARGV2, SYSARGV3):
                MAINTENANCE = 1

            if 'analyzetables' in (SYSARGV1, SYSARGV2, SYSARGV3):
                ANALYZETABLES = 1

            if 'unlock' in (SYSARGV1, SYSARGV2, SYSARGV3):
                UNLOCK = 1

            if 'getstatement' in (SYSARGV1, SYSARGV2, SYSARGV3):
                PARAMS = 'getstatement'

            if 'help' in (SYSARGV1, SYSARGV2, SYSARGV3):
                print("Usage -> main param debug debuglevel\n"
                      "      - param - on of checkNew / checknew, updateLast / updatelast, updateAll / updateall\n"
                      "      - debug\n"
                      "      - debuglevel - between 0 and 9 - always used as param after debug\n"
                      "      - maintenance - locks the execution and archives to tar the tables above XXX MBs\n"
                      "      - analyzetables - locks the execution and runs analyze tables on all tables\n"
                      "      - unlock - unlocks the execution\n"
                      "      - getstatement - sets getstatement variable\n" # to be checked if it is used somewhere?
                      "      - help - view this help\n")
                exit(0)

        RUNNINGHANDLERS = 0
        RUNNINGFEEDS = 0
        RUNNINGCRON = 0

        cfgmain = Config(debug=DEBUG)

        if MAINTENANCE == 1:
            cfgmain.setvpwsconfig('global', 'lock', '1')
            # mntnc = ClassMaintenance(DEBUG, DEBUGLEVEL, RUNNINGHANDLERS, RUNNINGFEEDS, RUNNINGCRON)
            mntnc.checkTables()
            cfgmain.setvpwsconfig('global', 'lock', '0')
            exit(0)

        if ANALYZETABLES == 1:
            cfgmain.setvpwsconfig('global', 'lock', '1')
            # mntnc = ClassMaintenance(DEBUG, DEBUGLEVEL, RUNNINGHANDLERS, RUNNINGFEEDS, RUNNINGCRON)
            mntnc.analyzeTables()
            cfgmain.setvpwsconfig('global', 'lock', '0')
            exit(0)

        if UNLOCK == 1:
            print("Are you sure you want to unlock the execution? Please confirm with Y!")
            confirm = input()
            if confirm != 'Y':
                print("Still Locked!")
                exit(0)
            else:
                cfgmain.setvpwsconfig('global', 'lock', '0')
                print("Unlocked!")

        LOCKS = cfgmain.getvpwsconfig('global', 'lock')

        if LOCKS == '1' and MAINTENANCE != 1:
            cfgmain.sendErrorEmail({}, "LOCKS activated!!! Please check if something is not running!!!")
            exit(0)

        RUNNINGHANDLERS = 1
        RUNNINGFEEDS = 0
        RUNNINGCRON = 0

        processAllHandlers = ClassProcessHandlers(ACTIVE, DEBUG, DEBUGLEVEL, RUNNINGHANDLERS, RUNNINGFEEDS, RUNNINGCRON)
        processAllHandlers.params = PARAMS
        processAllHandlers.processdatetime = start
        processAllHandlers.processAllFeeds()

        RUNNINGHANDLERS = 0

        RUNNINGFEEDS = 1

        # processAllFeeds = ClassProcessFeeds(ACTIVE, DEBUG, DEBUGLEVEL, RUNNINGHANDLERS, RUNNINGFEEDS, RUNNINGCRON)
        # processAllFeeds.params = PARAMS
        # processAllFeeds.processdatetime = start
        # processAllFeeds.processAllFeeds()

        RUNNINGFEEDS = 0

        RUNNINGCRON = 1

        # processAllCronjobs = ClassProcessCronjob('*', DEBUG, DEBUGLEVEL, RUNNINGHANDLERS, RUNNINGFEEDS, RUNNINGCRON)
        # processAllCronjobs.processAllCronjob()

        RUNNINGCRON = 0

        end = datetime.datetime.now()
        print(end)

        print(end - start)
