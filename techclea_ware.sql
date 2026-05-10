-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 29, 2025 at 01:10 AM
-- Server version: 10.11.13-MariaDB
-- PHP Version: 8.3.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `techclea_ware`
--

DELIMITER $$
--
-- Procedures
--
CREATE OR REPLACE PROCEDURE `boroimport` (OUT `result` TEXT CHARSET utf8mb4)
MODIFIES SQL DATA
BEGIN
    DECLARE feedcount INT DEFAULT 0;
    DECLARE updates INT DEFAULT 0;
    DECLARE updatesl INT DEFAULT 0;
    DECLARE endresult INT DEFAULT 0;
    DECLARE endresultsl INT DEFAULT 0;
    DECLARE attrcount INT DEFAULT 0;
    DECLARE attrcounta INT DEFAULT 0;
    DECLARE attrcountal INT DEFAULT 0;
    DECLARE termcount INT DEFAULT 0;
    DECLARE termcounta INT DEFAULT 0;
    DECLARE termcountal INT DEFAULT 0;
    DECLARE stckacount INT DEFAULT 0;
    DECLARE stckacounta INT DEFAULT 0;
    DECLARE stckrcount INT DEFAULT 0;
    DECLARE stckrcounta INT DEFAULT 0;
    DECLARE stckgcount INT DEFAULT 0;
    DECLARE stckgcounta INT DEFAULT 0;

	SET result = '';
    
	SELECT count(*) INTO feedcount FROM `techclea_ware`.`borotrade_json`;
    
    SET result = CONCAT(result, 'Initial feed count -> ', CAST(feedcount as CHAR), '\n');

	-- check for updated records

	-- STEP 2

    SELECT count(*) into updates from (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, 1 as xtype, 2 as xunit FROM `techclea_ware`.`borotrade_json` bj left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a left join (SELECT * FROM `techclea_ware`.stck) b on a.products_sku = b.sku and a.products_id = b.isbn where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.xtype <> b.xtype or a.xunit <> b.xunit;

    SET result = CONCAT(result, 'Updates found -> ', CAST(updates as CHAR), '\n');

	-- INSERT INTO stcka THE UPDATED RECORDS when stck.isbn is updated with products_id!!!

	-- STEP 3

	INSERT INTO `techclea_ware`.`stcka`
	(`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`)
	select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid` from 
	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, 1 as xtype, 2 as xunit FROM `techclea_ware`.`borotrade_json` bj left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
	left join
	(SELECT * FROM `techclea_ware`.stck) b
	on a.products_sku = b.sku and a.products_id = b.isbn
	where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or a.galleryupd  <> b.image or a.xtype <> b.xtype or a.xunit <> b.xunit;

    SET result = CONCAT(result, 'Inserts into archive table stcka -> ', CAST(ROW_COUNT() as CHAR), '\n');
    
	-- UPDATE stck ALL FIELDS WHERE ANY CHANGES!!!

	-- STEP 4

    update `techclea_ware`.stck bb left join
	(select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, a.* from 
	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, 1 as axtype, 2 as axunit FROM `techclea_ware`.`borotrade_json` bj left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
	left join
	(SELECT * FROM `techclea_ware`.stck) b
	on a.products_sku = b.sku and a.products_id = b.isbn
	where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.axtype <> b.xtype or a.axunit <> b.xunit) aa on bb.id = aa.id
	set bb.id_catg = aa.catgw, bb.id_inet = aa.catgi, bb.name = aa.products_name, bb.oprice = aa.products_sale_price, bb.ocurrency = aa.products_sale_price_curr, bb.dprice = aa.products_crrsale_price, bb.iprice = products_sale_price, bb.image = aa.galleryupd, bb.xtype = aa.axtype, bb.xunit = aa.axunit where aa.id is not null;

    SET result = CONCAT(result, 'Update stck where changes found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- INSERT ALL NEW PRODUCTS MISSING IN stck

	-- STEP 5

	insert into `techclea_ware`.stck (`id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `iprice`, `ocurrency`, `dprice`, `dcurrency`, `xtype`, `punit`, `xunit`, `sunit`, `id_vatx`, `image`)
	select a.catgw as id_catg, a.catgi as id_inet, a.products_sku as sku, a.products_id as isbn, a.products_name as name, a.products_sale_price as oprice, a.products_sale_price as iprice, a.products_sale_price_curr as ocurrency, a.products_crrsale_price as dprice, a.products_sale_price_curr as dcurrency, 1 as xtype, 2 as punit, 1 as xunit, 2 as sunit, 1 as id_vatx, a.galleryupd as image from 
	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd FROM `techclea_ware`.`borotrade_json` bj left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
	left join
	(SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image` FROM `techclea_ware`.stck where sactx <> 1) b
	on a.products_sku = b.sku and a.products_id = b.isbn
	where b.id is null;

    SET result = CONCAT(result, 'Insert into stck where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- UPDATE stck.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

	-- STEP 6

	update `techclea_ware`.stck b left join 
	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd FROM `techclea_ware`.`borotrade_json` bj left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `techclea_ware`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
	on a.products_sku = b.sku and a.products_id = b.isbn
	set b.sactx = 1
	where a.products_sku is null;

    SET result = CONCAT(result, 'Update stck to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- UPDATE borotrade_json.stck_id with stck.id

	-- STEP 7

	update `techclea_ware`.`borotrade_json` a left join
	(SELECT * FROM `techclea_ware`.stck where sactx <> 1) b
	on a.products_sku = b.sku and a.products_id = b.isbn
	set a.stck_id = b.id;

    SET result = CONCAT(result, 'Update stck stck_id into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');
    
	-- check active products count in stck

	-- STEP 8

    select count(*) INTO endresult from `techclea_ware`.stck where sactx <> 1;

    SET result = CONCAT(result, 'Updated destination table active items after import -> ', CAST(endresult as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- UPDATE stck_l

	-- STEP 2

	SELECT count(*) INTO updatesl FROM
	`techclea_ware`.`borotrade_json` bj left join `techclea_ware`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `techclea_ware`.stck_l sl on s.id = sl.id_stck
	where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

    SET result = CONCAT(result, 'Updates stck_l found -> ', CAST(updatesl as CHAR), '\n');

	-- STEP 3

	-- INSERT INTO stck_la THE UPDATED RECORDS

	INSERT INTO `techclea_ware`.`stck_la`
	SELECT sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
	`techclea_ware`.`borotrade_json` bj left join `techclea_ware`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `techclea_ware`.stck_l sl on s.id = sl.id_stck
	where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

    SET result = CONCAT(result, 'Inserts into archive table stck_la -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- STEP 4

	-- UPDATE stck_l ALL FIELDS WHERE ANY CHANGES!!!

	UPDATE `techclea_ware`.`stck_l` sl
	left join `techclea_ware`.stck s on s.id = sl.id_stck left join `techclea_ware`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
	SET sl.title = bj.products_name, sl.description = CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, ''))
	where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

    SET result = CONCAT(result, 'Update stck_l where changes found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- STEP 5

	-- INSERT ALL NEW PRODUCTS MISSING IN stck_l

	INSERT INTO `techclea_ware`.`stck_l` (`id_stck`, `id_lang`, `title`, `description`)
	SELECT s.`id`, 1, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) FROM
	`techclea_ware`.`borotrade_json` bj left join `techclea_ware`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `techclea_ware`.stck_l sl on s.id = sl.id_stck
	where sl.id is null;

    SET result = CONCAT(result, 'Insert into stck_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- STEP 6

	-- UPDATE stck_l.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

	UPDATE `techclea_ware`.stck_l sl left join `techclea_ware`.stck s on sl.id_stck = s.id
	left join `techclea_ware`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
	set sl.sactx = 1
	where bj.products_sku is null;

    SET result = CONCAT(result, 'Update stck_l to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- check active products count in stck_l

	-- STEP 7

    select count(*) INTO endresultsl from `techclea_ware`.stck_l where sactx <> 1;

    SET result = CONCAT(result, 'Updated destination table active items after import -> ', CAST(endresultsl as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- UPDATE attr

	-- update sactx with 1 for all non existant attr

	update `techclea_ware`.attr a right join
	(select attr, name, id from
	(select attr, name, id from
	(SELECT DISTINCT attr FROM `techclea_ware`.borotrade_attr group by attr) src_a
	left join
	(select id, name from `techclea_ware`.attr) dst_a
	on src_a.attr = dst_a.name
	UNION
	select attr, name, id from
	(SELECT DISTINCT attr FROM `techclea_ware`.borotrade_attr group by attr) src_a
	right join
	(select id, name from `techclea_ware`.attr) dst_a
	on src_a.attr = dst_a.name) a
	where a.attr is null) src on src.id = a.id
	set a.sactx = 1;

    SET result = CONCAT(result, 'Update attr to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert all new rows into attr

	insert into `techclea_ware`.attr (name)
	select attr from
	(select attr, name, id from
	(SELECT DISTINCT attr FROM `techclea_ware`.borotrade_attr group by attr) src_a
	left join
	(select id, name from `techclea_ware`.attr) dst_a
	on src_a.attr = dst_a.name
	UNION
	select attr, name, id from
	(SELECT DISTINCT attr FROM `techclea_ware`.borotrade_attr group by attr) src_a
	right join
	(select id, name from `techclea_ware`.attr) dst_a
	on src_a.attr = dst_a.name) a
	where a.name is null;

    SET result = CONCAT(result, 'Insert into attr where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update attr_id into src table -> borotrade_attr

	update `techclea_ware`.borotrade_attr src_a left join 
	(select id, name from `techclea_ware`.attr where sactx <> 1) dst_a
	on src_a.attr = dst_a.name
	set src_a.attr_id = dst_a.id;

    SET result = CONCAT(result, 'Update attr_id into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update sactx with 1 for all non existant attr_l

	update `techclea_ware`.attr_l al left join `techclea_ware`.attr a on al.id_attr = a.id set al.sactx = a.sactx;

    SET result = CONCAT(result, 'Update attr_l to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert new values into attr_l

	INSERT INTO `techclea_ware`.`attr_l` (`id_attr`, `id_lang`, `title`)
	select a.id, 1, a.name from `techclea_ware`.`attr` a left join `techclea_ware`.`attr_l` al on a.id = al.id_attr where al.id_attr is null;

    SET result = CONCAT(result, 'Insert into attr_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- check both tables are ok

	select count(*) into attrcount from (SELECT attr FROM `techclea_ware`.`borotrade_attr`group by attr) a;
    SET result = CONCAT(result, 'Feed table attr active items -> ', CAST(attrcount as CHAR), '\n');

	select count(*) into attrcounta from `techclea_ware`.`attr` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table attr active items after impot -> ', CAST(attrcounta as CHAR), '\n');

	select count(*) into attrcountal from `techclea_ware`.`attr_l` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table attr_l active items after impot -> ', CAST(attrcountal as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_id in borotrade_attr from borotrade_json

	update `techclea_ware`.borotrade_attr a left join `techclea_ware`.borotrade_json j on a.products_sku = j.products_sku and a.products_id = j.products_id set a.stck_id = j.stck_id;

    SET result = CONCAT(result, 'Updated feed table attr_l -> ', CAST(attrcountal as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update sactx in term where not found in borotrade_attr

	update `techclea_ware`.term t left join 
	(SELECT attr_id, val FROM `techclea_ware`.borotrade_attr group by attr_id, val) a
	on t.name = a.val and t.id_attr = a.attr_id and t.sactx <> 1
	set t.sactx = 1
	where a.val is null;

	-- insert into term the new vals

	INSERT INTO `techclea_ware`.`term` (`id_attr`, `name`)
	select a.attr_id, a.val from 
	(SELECT attr_id, val FROM `techclea_ware`.borotrade_attr group by attr_id, val) a
	left join
	`techclea_ware`.term t
	on a.val = t.name and t.id_attr = a.attr_id and t.sactx <> 1
	where t.id is null;

    SET result = CONCAT(result, 'Insert into term where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update term_id into src table -> borotrade_attr

	update `techclea_ware`.borotrade_attr src_a left join 
	(select id, id_attr, name from `techclea_ware`.term where sactx <> 1) dst_a
	on src_a.val = dst_a.name and src_a.attr_id = dst_a.id_attr
	set src_a.term_id = dst_a.id;

    SET result = CONCAT(result, 'Update term_id into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update sactx with 1 for all non existant term_l

	update `techclea_ware`.term_l tl left join `techclea_ware`.term t on tl.id_term = t.id set tl.sactx = t.sactx;

    SET result = CONCAT(result, 'Update term to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert new values into term_l

	INSERT INTO `techclea_ware`.`term_l` (`id_term`, `id_lang`, `title`)
	select t.id, 1, t.name from `techclea_ware`.`term` t left join `techclea_ware`.`term_l` tl on t.id = tl.id_term where tl.id_term is null;

    SET result = CONCAT(result, 'Insert into term_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- check both tables are ok

	select count(*) into termcount from (select attr_id, val from `techclea_ware`.borotrade_attr group by attr_id, val) a;
    SET result = CONCAT(result, 'Feed table term active items -> ', CAST(termcount as CHAR), '\n');

	select count(*) into termcounta from `techclea_ware`.`term` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table term active items after impot -> ', CAST(termcounta as CHAR), '\n');

	select count(*) into termcountal from `techclea_ware`.`term_l` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table term_l active items after impot -> ', CAST(termcountal as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_a where not found in borotrade_attr
	update techclea_ware.stck_a s left join techclea_ware.borotrade_attr a on s.id_attr = a.attr_id and s.id_term = a.term_id and s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

    SET result = CONCAT(result, 'Update term to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert into stck_a where new found in borotrade_attr
	INSERT INTO `techclea_ware`.`stck_a` (`id_stck`, `id_attr`, `id_term`)
	SELECT a.stck_id, a.attr_id, a.term_id FROM `techclea_ware`.borotrade_attr a left join `techclea_ware`.stck_a s on a.attr_id = s.id_attr and a.term_id = s.id_term and a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;

    SET result = CONCAT(result, 'Insert into term_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');


	select count(*) into stckacount from `techclea_ware`.borotrade_attr;
    SET result = CONCAT(result, 'Feed table stck_a active items -> ', CAST(stckacount as CHAR), '\n');
    
	select count(*) into stckacounta from `techclea_ware`.stck_a where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table stck_a active items after impot -> ', CAST(stckacounta as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	-- update stck_id in borotrade_linkedp from borotrade_json

	update `techclea_ware`.borotrade_linkedp p left join `techclea_ware`.borotrade_json j on p.products_sku = j.products_sku and p.products_id = j.products_id set p.stck_id = j.stck_id;


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update into stck_r not found

	update `techclea_ware`.borotrade_linkedp p left join `techclea_ware`.stck_r r on p.stck_id = r.id_stck and r.sactx <> 1 set r.sactx = 1 where p.stck_id is null;

    SET result = CONCAT(result, 'Update stck_r to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert into stck_r the new found rows

	INSERT INTO `techclea_ware`.`stck_r` (`id_stck`, `text`)
	select p.stck_id, p.linkedp from `techclea_ware`.borotrade_linkedp p left join `techclea_ware`.stck_r r on p.stck_id = r.id_stck and r.sactx <> 1 where r.id_stck is null;

    SET result = CONCAT(result, 'Insert into stck_r where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	select count(*) into stckrcount from `techclea_ware`.borotrade_linkedp;
    SET result = CONCAT(result, 'Feed table stck_r active items -> ', CAST(stckrcount as CHAR), '\n');
    
	select count(*) into stckrcounta from `techclea_ware`.stck_r where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table stck_r active items after impot -> ', CAST(stckrcounta as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_id in borotrade_lgallery_json from borotrade_json

	update `techclea_ware`.borotrade_gallery_json g left join `techclea_ware`.borotrade_json j on g.products_sku = j.products_sku and g.products_id = j.products_id set g.stck_id = j.stck_id;

    SET result = CONCAT(result, 'Update borotrade_gallery_json id_stck -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_g where not found in borotrade_gallery_json
	update `techclea_ware`.stck_g s left join `techclea_ware`.borotrade_gallery_json a on s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

    SET result = CONCAT(result, 'Update stck_g to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert into stck_g where new found in borotrade_gallery_json
	INSERT INTO `techclea_ware`.`stck_g` (`id_stck`, `urlx`, `path`)
	SELECT a.stck_id, a.gallery, a.path FROM `techclea_ware`.borotrade_gallery_json a left join `techclea_ware`.stck_g s on a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;

    SET result = CONCAT(result, 'Insert into stck_g where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	select count(*) into stckgcount from `techclea_ware`.borotrade_gallery_json;
    SET result = CONCAT(result, 'Feed table gallery_json active items -> ', CAST(stckgcount as CHAR), '\n');

	select count(*) into stckgcounta from `techclea_ware`.stck_g where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table stck_g active items after impot -> ', CAST(stckgcounta as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	-- update final (added by Desso
	UPDATE `techclea_ware`.stck JOIN (SELECT id_stck, MIN(id) as id_gall FROM `techclea_ware`.stck_g GROUP BY id_stck) AS subquery ON stck.id = subquery.id_stck SET stck.id_gall = subquery.id_gall;


    SELECT 1, result;
END;

$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



