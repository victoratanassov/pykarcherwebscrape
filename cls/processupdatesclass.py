# -*- coding: utf-8 -*-
import os
import sys
import pymysql.cursors
from datetime import datetime, timedelta
import gc

import pymysql.cursors

from cfg.config import Config  # noqa: E402


class ClassProcessUpdates:
    debug = False
    debuglevel = 0
    cfg = Config(debug=debug)
    myConnectionMain = ''
    emailvars = {}
    suser = -1

    def __init__(self, debug=False, debuglevel=0):
        self.debug = debug
        self.debuglevel = debuglevel
        print("Processing handlers:")
        print("Debug        -> " + str(self.debug))
        print("Debug level  -> " + str(self.debuglevel))
        self.myConnectionMain = self.cfg.myConnectionMain
        # self.myConnection = pymysql.connect(
        #     host=self.cfg.hostname,
        #     user=self.cfg.username,
        #     password=self.cfg.password,
        #     db=self.cfg.database,
        #     charset='utf8mb4',
        #     cursorclass=pymysql.cursors.DictCursor
        # )

    def __del__(self):
        self.closeMySqlPool()
        try:
            gc.collect()
        except Exception as e:
            print(e)
            return

    def closeMySqlPool(self):
        self.myConnectionMain.close()

    def processCategoriesUpdate(self, xtype):
        start = datetime.now()
        print(start)

        srctable = "borotrade_json"

        print("Starting Categories update for xtype = " + str(xtype) + "...")

        catgarrfromfeed = {}

        getcatgfromfeed = "SELECT category_id, category_name, count(*) FROM " + self.cfg.database + "." + srctable + " GROUP BY category_id, category_name;"

        try:
            handlersconn = self.myConnectionMain.connection()
            proccatupddb = handlersconn.cursor()

            try:
                proccatupddb.execute(getcatgfromfeed)
            except pymysql.Error as e:
                print(e)
                print(getcatgfromfeed)

            for rowret in proccatupddb.fetchall():
                if self.debug and self.debuglevel >= 0:
                    print(rowret)
                if rowret['category_id'] is not None:
                    catgarrfromfeed[rowret['category_id']] = rowret['category_name']
        except pymysql.Error as e:
            print(e)
            print(getcatgfromfeed)
            self.cfg.sendErrorEmail(errorMessage=str(e) + " " + str(getcatgfromfeed))
            return
        finally:
            handlersconn.close()                                # returns the connection to the pool

        if self.debug and self.debuglevel >= 0:
            print(catgarrfromfeed)

        catgfromdb = "SELECT * FROM " + self.cfg.warehousedb + ".catg WHERE xtype = " + str(xtype) + ";"
        try:
            handlersconn = self.myConnectionMain.connection()
            proccatupddb = handlersconn.cursor()

            try:
                proccatupddb.execute(catgfromdb)
            except pymysql.Error as e:
                print(e)
                print(catgfromdb)

            for rowret1 in proccatupddb.fetchall():
                if self.debug and self.debuglevel >= 0:
                    print(rowret1)
                if rowret1['fid'] in catgarrfromfeed.keys():
                    # Какво да update-не в таблицата? - каквото се update-не да се добави в catga
                    if self.debug and self.debuglevel >= 0:
                        print(rowret1['fid'])
                        print(catgarrfromfeed[rowret1['fid']])
                    del catgarrfromfeed[rowret1['fid']]
        except pymysql.Error as e:
            print(e)
            print(getcatgfromfeed)
            self.cfg.sendErrorEmail(errorMessage=str(e) + " " + str(getcatgfromfeed))
            return
        finally:
            handlersconn.close()                                # returns the connection to the pool

        newcategories = ''

        # добавя новите категории, които са останали в dict catgarrfromfeed - добавя ли се в catga?
        if len(catgarrfromfeed) > 0:
            if self.debug and self.debuglevel >= 0:
                print(catgarrfromfeed)
            for key in catgarrfromfeed:
                newcategories = newcategories + str(key) + " => " + catgarrfromfeed[key] + "<br>\n"
                insstmnt = "INSERT INTO `" + self.cfg.warehousedb + "`.`catg` (`id_catg`, `name`, `xtype`, `path`, `suser`, `fid`) VALUES (0, '" + str(catgarrfromfeed[key]) + "', " + str(xtype) + ", 'AAA', " + str(self.suser) + ", " + str(key) + ");"
                if self.debug and self.debuglevel >= 0:
                    print(insstmnt)
                try:
                    handlersconn = self.myConnectionMain.connection()
                    proccatupddb = handlersconn.cursor()

                    try:
                        proccatupddb.execute(insstmnt)
                    except pymysql.Error as e:
                        print(e)
                        print(catgfromdb)
                except pymysql.Error as e:
                    print(e)
                    print(getcatgfromfeed)
                    self.cfg.sendErrorEmail(errorMessage=str(e) + " " + str(getcatgfromfeed))
                    return
                finally:
                    handlersconn.close()                                # returns the connection to the pool

        # изпрати на мейл новите категории, които са добавени в таблицата
        addednewcatg = ""
        if len(newcategories) > 0:
            addednewcatg = "Added new categories for xtype = " + str(xtype) + ":<br>\n" + str(newcategories)
            print(addednewcatg)

        self.emailvars['handlerid'] = ""
        self.emailvars['rss_check'] = ""
        self.emailvars['database_check'] = ""
        self.emailvars['jobsindbinit'] = ""
        self.emailvars['jobsinfeed'] = ""
        self.emailvars['jobsupdated'] = ""
        self.emailvars['jobsinserted'] = ""
        self.emailvars['jobsdeleted'] = ""
        self.emailvars['jobsindb'] = ""
        self.emailvars['time1step'] = 0.00
        self.emailvars['time2step'] = 0.00
        self.emailvars['time3end'] = 0.00

        if len(addednewcatg) > 0:
            self.cfg.sendErrorEmail(handler={'jobfeed_id':'Categories ADDED!!!'}, errorMessage=str(addednewcatg))
        # self.cfg.sendEmail({'jobfeed_id':"", "emailsto":self.cfg.defaulttoemail, "emailssubject":"Categories added!", "emailsbody":str(addednewcatg), "sendemails":"1"}, self.emailvars)


        # как се добавя в catg_l и catg_la? ако има само бг то направо се update-ва директно при update-та не catg и catga?

    def processItemsUpdate(self):
        self.debug = True
        self.debuglevel = 0

        start = datetime.now()
        print(start)

        print("Starting Items update...")

        # procstckupddb = self.myConnectionMain.cursor()

        # # зарежда категориите в масив с ключ id на категорията от фийда в отделни масиви за интернет и склад
        # catgwarrfromdb = {}
        #
        # catgwfromdb = "SELECT * FROM borotrade_crm.catg WHERE xtype = 1;"
        # try:
        #     procstckupddb.execute(catgwfromdb)
        # except pymysql.Error as e:
        #     print(e)
        #     print(catgwfromdb)
        #
        # for rowret in procstckupddb.fetchall():
        #     if self.debug and self.debuglevel >= 0:
        #         print(rowret)
        #     if rowret['fid'] is not None:
        #         catgwarrfromdb[rowret['fid']] = rowret['id']
        #
        # if self.debug and self.debuglevel >= 0:
        #     print(catgwarrfromdb)
        #
        # # зарежда категориите в масив с ключ id на категорията от фийда в отделни масиви за интернет и склад - сега за интернет
        # catgiarrfromdb = {}
        #
        # catgifromdb = "SELECT * FROM borotrade_crm.catg WHERE xtype = 2;"
        # try:
        #     procstckupddb.execute(catgifromdb)
        # except pymysql.Error as e:
        #     print(e)
        #     print(catgifromdb)
        #
        # for rowret1 in procstckupddb.fetchall():
        #     if self.debug and self.debuglevel >= 0:
        #         print(rowret1)
        #     if rowret1['fid'] is not None:
        #         catgiarrfromdb[rowret1['fid']] = rowret1['id']
        #
        # if self.debug and self.debuglevel >= 0:
        #     print(catgiarrfromdb)

        # stck - стоките
        # взема от stck sku и го слага в масив - рповерява дали има такова sku във фийда и прави update
        skuarrfromdb = {}
        itemdatafromdb = {}

        getskufromdb = "SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM borotrade_crm.stck;"
        try:
            handlersconn = self.myConnectionMain.connection()
            procstckupddb = handlersconn.cursor()

            procstckupddb.execute('SET NAMES utf8mb4;')
            procstckupddb.execute('SET character_set_connection=utf8mb4;')

            try:
                procstckupddb.execute(getskufromdb)
            except pymysql.Error as e:
                print(e)
                print(getskufromdb)

            for rowret2 in procstckupddb.fetchall():
                if self.debug and self.debuglevel >= 0:
                    print(rowret2)
                if rowret2['sku'] is not None:
                    skuarrfromdb[rowret2['sku']] = rowret2['id']
                    itemdatafromdb[rowret2['id']] = {}
                    itemdatafromdb[rowret2['id']]['name'] = rowret2['name']
                    itemdatafromdb[rowret2['id']]['dprice'] = rowret2['dprice']
                    # да се добави в последствие и количеството - няма количества във файла...
        finally:
            handlersconn.close()  # returns the connection to the pool

        if self.debug and self.debuglevel >= 0:
            print(skuarrfromdb)

        getdatafromfeed = "SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid;"
        # getdatafromfeed = "SELECT * FROM vpws_main.borotrade_json;"
        try:
            handlersconn = self.myConnectionMain.connection()
            procstckupddb = handlersconn.cursor()

            procstckupddb.execute('SET NAMES utf8mb4;')
            procstckupddb.execute('SET character_set_connection=utf8mb4;')

            try:
                procstckupddb.execute(getdatafromfeed)
            except pymysql.Error as e:
                print(e)
                print(getdatafromfeed)

            for rowret3 in procstckupddb.fetchall():
                if self.debug and self.debuglevel >= 0:
                    print(rowret3)
                if rowret3['products_sku'] in skuarrfromdb:
                    if self.debug and self.debuglevel >= 0:
                        print(skuarrfromdb[rowret3['products_sku']])
                    if rowret3['products_name'] != itemdatafromdb[skuarrfromdb[rowret3['products_sku']]]['name']:
                        if self.debug and self.debuglevel >= 0:
                            print("name in DB different from name in feed! DB => " + str(itemdatafromdb[skuarrfromdb[rowret3['products_sku']]]['name']) + " Feed => " + str(rowret3['products_name']))
                    if rowret3['products_crrsale_price'] != itemdatafromdb[skuarrfromdb[rowret3['products_sku']]]['dprice']:
                        if self.debug and self.debuglevel >= 0:
                            print("price in DB different from price in feed! DB => " + str(itemdatafromdb[skuarrfromdb[rowret3['products_sku']]]['dprice']) + " Feed => " + str(rowret3['products_crrsale_price']))
                    # update name and prices - description, attributes, etc. add a row in archive file for each update where there is update
                    # изпрати мейл с промените в цените и имената на стоките
                else:
                    if self.debug and self.debuglevel >= 0:
                        print("new sku => " + str(rowret3['products_sku']) + " for item => " + str(rowret3['products_name']))
                    # insert в базата новите стоки - категориите са в отделни масиви
                    # insert в базата на атрибутите от поле products_descr2
        finally:
            handlersconn.close()  # returns the connection to the pool

# check if any updates!
# select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from
# (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
# left join
# (SELECT * FROM borotrade_crm.stck) b
# on a.products_sku = b.sku and a.products_id = b.isbn
# where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;


# insert into stcka the relevatn changes!

# INSERT INTO `borotrade_crm`.`stcka`
# (`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`, `lot`, `description`)
# select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from
# (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
# left join
# (SELECT * FROM borotrade_crm.stck) b
# on a.products_sku = b.sku and a.products_id = b.isbn
# where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description;


# update stck with the updated values from the export

# update borotrade_crm.stck bb left join
# (select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` as bdescription, a.* from
# (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
# left join
# (SELECT * FROM borotrade_crm.stck) b
# on a.products_sku = b.sku and a.products_id = b.isbn
# where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description) aa on bb.id = aa.id
# set bb.id_catg = aa.catgw, bb.id_inet = aa.catgi, bb.name = aa.products_name, bb.oprice = aa.products_sale_price, bb.ocurrency = aa.products_sale_price_curr, bb.dprice = aa.products_crrsale_price, bb.image = aa.galleryupd, bb.description = aa.description where aa.id is not null;

# insert the new items in stck

# insert into borotrade_crm.stck (`id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `iprice`, `xtype`, `punit`, `xunit`, `sunit`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description`)
# select a.catgw as id_catg, a.catgi as id_inet, a.products_sku as sku, a.products_id as isbn, a.products_name as name, a.products_sale_price as oprice, a.products_sale_price as iprice, 1 as xtype, 2 as punit, 1 as xunit, 2 as sunit, a.products_sale_price_curr as ocurrency, a.products_crrsale_price as dprice, a.products_sale_price_curr as dcurrency, 1 as id_vatx, a.galleryupd as image, a.description from
# (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
# left join
# (SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM borotrade_crm.stck) b
# on a.products_sku = b.sku and a.products_id = b.isbn
# where b.id is null;


# delete all items (update sactx with 1) that are not in parent feed

# update borotrade_crm.stck bb left join
# (
# select * from
# (SELECT * FROM borotrade_crm.stck) b
# left join
# (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as bdescription FROM `vpws_main`.`borotrade_json` bj left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM borotrade_crm.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
# on a.products_sku = b.sku and a.products_id = b.isbn
# where a.products_sku is null
# ) a on bb.id = a.id
# set bb.sactx = 1 where a.id is not null;


# check if the job count is the same as in the parent feed!
# select count(*) as cnt from borotrade_crm.stck where sactx <> 1;


# update id into the parent feed -> borotrade_json

# update `vpws_main`.`borotrade_json` aa left join
# (select * from
# (SELECT * FROM `vpws_main`.`borotrade_json`) a
# left join
# (SELECT * FROM borotrade_crm.stck) b
# on a.products_sku = b.sku and a.products_id = b.isbn and b.sactx <> 1) bb on aa.products_sku = bb.sku and aa.products_id = bb.isbn
# set aa.stck_id = bb.id;



        # attr - имена на атрибутите
        # term - стойности на атрибутите


