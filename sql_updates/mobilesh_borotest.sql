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
-- Database: `mobilesh_borotest`
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
    
	SELECT count(*) INTO feedcount FROM `mobilesh_borotest`.`borotrade_json`;
    
    SET result = CONCAT(result, 'Initial feed count -> ', CAST(feedcount as CHAR), '\n');

	-- check for updated records

	-- STEP 2

--     SELECT count(*) into updates from (SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description, 1 as xtype, 2 as xunit FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a left join (SELECT * FROM `mobilesh_borotest`.stck) b on a.products_sku = b.sku and a.products_id = b.isbn where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description or a.xtype <> b.xtype or a.xunit <> b.xunit;

select count(*) into updates from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stcku AS ( SELECT `stck`.`id`, `stck`.`id_catg`, `stck`.`id_inet`, `stck`.`id_stck`, `stck`.`id_manf`, `stck`.`id_supl`, `stck`.`xtype`, `stck`.`sku`, `stck`.`skux`, `stck`.`ean`, `stck`.`isbn`, `stck`.`upc`, `stck`.`name`, `stck`.`weight`, `stck`.`punit`, `stck`.`sunit`, `stck`.`xunit`, `stck`.`qunit`, `stck`.`plus`, `stck`.`minus`, `stck`.`allqty`, `stck`.`minqty`, `stck`.`iprice`, `stck`.`icurrency`, `stck`.`oprice`, `stck`.`ocurrency`, `stck`.`dperc`, `stck`.`dprice`, `stck`.`dcurrency`, `stck`.`id_vatx`, `stck`.`minpr`, `stck`.`maxpr`, `stck`.`avgpr`, `stck`.`image_uri`, `stck`.`image`, `stck`.`suser`, `stck`.`stime`, `stck`.`sactx`, `stck`.`wid`, `stck`.`lot`, `stck`.`description` FROM mobilesh_borotest.`stck`
    UNION
    SELECT	`stcka`.`id`, `stcka`.`id_catg`, `stcka`.`id_inet`, `stcka`.`id_stck`, `stcka`.`id_manf`, `stcka`.`id_supl`, `stcka`.`xtype`, `stcka`.`sku`, `stcka`.`skux`, `stcka`.`ean`, `stcka`.`isbn`, `stcka`.`upc`, `stcka`.`name`, `stcka`.`weight`, `stcka`.`punit`, `stcka`.`sunit`, `stcka`.`xunit`, `stcka`.`qunit`, `stcka`.`plus`, `stcka`.`minus`, `stcka`.`allqty`, `stcka`.`minqty`, `stcka`.`iprice`, `stcka`.`icurrency`, `stcka`.`oprice`, `stcka`.`ocurrency`, `stcka`.`dperc`, `stcka`.`dprice`, `stcka`.`dcurrency`, `stcka`.`id_vatx`, `stcka`.`minpr`, `stcka`.`maxpr`, `stcka`.`avgpr`, `stcka`.`image_uri`, `stcka`.`image`, `stcka`.`suser`, `stcka`.`stime`, `stcka`.`sactx`, `stcka`.`wid`, `stcka`.`lot`, `stcka`.`description` FROM mobilesh_borotest.`stcka`
)
SELECT DISTINCT b.* FROM
(SELECT 
abs(id) AS id, MAX(stime) AS stime
FROM stcku
GROUP BY abs(id)) a
LEFT JOIN stcku b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description;

    SET result = CONCAT(result, 'Updates found -> ', CAST(updates as CHAR), '\n');

	-- INSERT INTO stcka THE UPDATED RECORDS when stck.isbn is updated with products_id!!!

	-- STEP 3

-- 	INSERT INTO `mobilesh_borotest`.`stcka`
-- 	(`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`, `lot`, `description`)
-- 	select -b.`id`, a.catgw, a.catgi, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, a.products_name, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, a.products_sale_price, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, a.galleryupd, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, a.description from 
-- 	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description, 1 as xtype, 2 as xunit FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- 	left join
-- 	(WITH stcku AS (SELECT * FROM `mobilesh_borotest`.`stck` UNION SELECT * FROM `mobilesh_borotest`.`stcka`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stcku GROUP BY abs(id)) a LEFT JOIN stcku b ON a.id=abs(b.id) AND a.stime=b.stime) b 
-- 	on a.products_sku = b.sku and a.products_id = b.isbn
-- 	where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description or a.xtype <> b.xtype or a.xunit <> b.xunit;

INSERT INTO `mobilesh_borotest`.`stcka`
(`id`, `id_catg`, `id_inet`, `id_stck`, `id_manf`, `id_supl`, `xtype`, `sku`, `skux`, `ean`, `isbn`, `upc`, `name`, `weight`, `punit`, `sunit`, `xunit`, `qunit`, `plus`, `minus`, `allqty`, `minqty`, `iprice`, `icurrency`, `oprice`, `ocurrency`, `dperc`, `dprice`, `dcurrency`, `id_vatx`, `minpr`, `maxpr`, `avgpr`, `image_uri`, `image`, `suser`, `stime`, `sactx`, `wid`, `lot`, `description`)
-- select -b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` from 
select -b.`id`, a.catgw, a.catgi, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, a.products_name, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, a.products_sale_price, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, a.galleryupd, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, a.description from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stcku AS (
    SELECT `stck`.`id`, `stck`.`id_catg`, `stck`.`id_inet`, `stck`.`id_stck`, `stck`.`id_manf`, `stck`.`id_supl`, `stck`.`xtype`, `stck`.`sku`, `stck`.`skux`, `stck`.`ean`, `stck`.`isbn`, `stck`.`upc`, `stck`.`name`, `stck`.`weight`, `stck`.`punit`, `stck`.`sunit`, `stck`.`xunit`, `stck`.`qunit`, `stck`.`plus`, `stck`.`minus`, `stck`.`allqty`, `stck`.`minqty`, `stck`.`iprice`, `stck`.`icurrency`, `stck`.`oprice`, `stck`.`ocurrency`, `stck`.`dperc`, `stck`.`dprice`, `stck`.`dcurrency`, `stck`.`id_vatx`, `stck`.`minpr`, `stck`.`maxpr`, `stck`.`avgpr`, `stck`.`image_uri`, `stck`.`image`, `stck`.`suser`, `stck`.`stime`, `stck`.`sactx`, `stck`.`wid`, `stck`.`lot`, `stck`.`description` FROM mobilesh_borotest.`stck`
    UNION
    SELECT 	`stcka`.`id`, `stcka`.`id_catg`, `stcka`.`id_inet`, `stcka`.`id_stck`, `stcka`.`id_manf`, `stcka`.`id_supl`, `stcka`.`xtype`, `stcka`.`sku`, `stcka`.`skux`, `stcka`.`ean`, `stcka`.`isbn`, `stcka`.`upc`, `stcka`.`name`, `stcka`.`weight`, `stcka`.`punit`, `stcka`.`sunit`, `stcka`.`xunit`, `stcka`.`qunit`, `stcka`.`plus`, `stcka`.`minus`, `stcka`.`allqty`, `stcka`.`minqty`, `stcka`.`iprice`, `stcka`.`icurrency`, `stcka`.`oprice`, `stcka`.`ocurrency`, `stcka`.`dperc`, `stcka`.`dprice`, `stcka`.`dcurrency`, `stcka`.`id_vatx`, `stcka`.`minpr`, `stcka`.`maxpr`, `stcka`.`avgpr`, `stcka`.`image_uri`, `stcka`.`image`, `stcka`.`suser`, `stcka`.`stime`, `stcka`.`sactx`, `stcka`.`wid`, `stcka`.`lot`, `stcka`.`description` FROM mobilesh_borotest.`stcka`
)
SELECT DISTINCT b.* FROM
(SELECT 
abs(id) AS id, MAX(stime) AS stime
FROM stcku
GROUP BY abs(id)) a
LEFT JOIN stcku b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.products_sku = b.sku and a.products_id = b.isbn
where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or a.galleryupd  <> b.image or a.description <>  b.description;

    SET result = CONCAT(result, 'Inserts into archive table stcka -> ', CAST(ROW_COUNT() as CHAR), '\n');
    
	-- UPDATE stck ALL FIELDS WHERE ANY CHANGES!!!

	-- STEP 4

--     update `mobilesh_borotest`.stck bb left join
-- 	(select b.`id`, b.`id_catg`, b.`id_inet`, b.`id_stck`, b.`id_manf`, b.`id_supl`, b.`xtype`, b.`sku`, b.`skux`, b.`ean`, b.`isbn`, b.`upc`, b.`name`, b.`weight`, b.`punit`, b.`sunit`, b.`xunit`, b.`qunit`, b.`plus`, b.`minus`, b.`allqty`, b.`minqty`, b.`iprice`, b.`icurrency`, b.`oprice`, b.`ocurrency`, b.`dperc`, b.`dprice`, b.`dcurrency`, b.`id_vatx`, b.`minpr`, b.`maxpr`, b.`avgpr`, b.`image_uri`, b.`image`, b.`suser`, b.`stime`, b.`sactx`, b.`wid`, b.`lot`, b.`description` as bdescription, a.* from 
-- 	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description, 1 as axtype, 2 as axunit FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- 	left join
-- 	(SELECT * FROM `mobilesh_borotest`.stck) b
-- 	on a.products_sku = b.sku and a.products_id = b.isbn
-- 	where a.catgw <> b.id_catg or a.catgi <> b.id_inet or a.products_name <> b.name or cast(a.products_sale_price as decimal) <> cast(b.oprice as decimal) or a.products_sale_price_curr  <> b.ocurrency or cast(a.products_crrsale_price as decimal) <> cast(b.dprice as decimal) or cast(a.products_sale_price as decimal) <> cast(b.iprice as decimal) or a.galleryupd  <> b.image or a.description <>  b.description or a.axtype <> b.xtype or a.axunit <> b.xunit) aa on bb.id = aa.id
-- 	set bb.id_catg = aa.catgw, bb.id_inet = aa.catgi, bb.name = aa.products_name, bb.oprice = aa.products_sale_price, bb.ocurrency = aa.products_sale_price_curr, bb.dprice = aa.products_crrsale_price, bb.iprice = products_sale_price, bb.image = aa.galleryupd, bb.description = aa.description, bb.xtype = aa.axtype, bb.xunit = aa.axunit where aa.id is not null;

--     SET result = CONCAT(result, 'Update stck where changes found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- INSERT ALL NEW PRODUCTS MISSING IN stck

	-- STEP 5

-- 	insert into `mobilesh_borotest`.stck (`id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `iprice`, `ocurrency`, `dprice`, `dcurrency`, `xtype`, `punit`, `xunit`, `sunit`, `id_vatx`, `image`, `description`)
-- 	select a.catgw as id_catg, a.catgi as id_inet, a.products_sku as sku, a.products_id as isbn, a.products_name as name, a.products_sale_price as oprice, a.products_sale_price as iprice, a.products_sale_price_curr as ocurrency, a.products_crrsale_price as dprice, a.products_sale_price_curr as dcurrency, 1 as xtype, 2 as punit, 1 as xunit, 2 as sunit, 1 as id_vatx, a.galleryupd as image, a.description from 
-- 	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- 	left join
-- 	(SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM `mobilesh_borotest`.stck where sactx <> 1) b
-- 	on a.products_sku = b.sku and a.products_id = b.isbn
-- 	where b.id is null;

insert into `mobilesh_borotest`.stck (`id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `iprice`, `ocurrency`, `dprice`, `dcurrency`, `xtype`, `punit`, `xunit`, `sunit`, `id_vatx`, `image`, `description`)
select a.catgw as id_catg, a.catgi as id_inet, a.products_sku as sku, a.products_id as isbn, a.products_name as name, a.products_sale_price as oprice, a.products_sale_price as iprice, a.products_sale_price_curr as ocurrency, a.products_crrsale_price as dprice, a.products_sale_price_curr as dcurrency, 1 as xtype, 2 as punit, 1 as xunit, 2 as sunit, 1 as id_vatx, a.galleryupd as image, a.description from 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(SELECT `id`, `id_catg`, `id_inet`, `sku`, `isbn`, `name`, `oprice`, `ocurrency`, `dprice`, `dcurrency`, `id_vatx`, `image`, `description` FROM `mobilesh_borotest`.stck where sactx <> 1) b
on a.products_sku = b.sku and a.products_id = b.isbn
where b.id is null;

    SET result = CONCAT(result, 'Insert into stck where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- UPDATE stck.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

	-- STEP 6

-- 	update `mobilesh_borotest`.stck b left join 
-- 	(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as bdescription FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- 	on a.products_sku = b.sku and a.products_id = b.isbn
-- 	set b.sactx = 1
-- 	where a.products_sku is null;

update `mobilesh_borotest`.stck b left join 
(SELECT c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as bdescription FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
on a.products_sku = b.sku and a.products_id = b.isbn
set b.sactx = 1
where a.products_sku is null;

    SET result = CONCAT(result, 'Update stck to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- UPDATE borotrade_json.stck_id with stck.id

	-- STEP 7

-- 	update `mobilesh_borotest`.`borotrade_json` a left join
-- 	(SELECT * FROM `mobilesh_borotest`.stck where sactx <> 1) b
-- 	on a.products_sku = b.sku and a.products_id = b.isbn
-- 	set a.stck_id = b.id;

update `mobilesh_borotest`.`borotrade_json` a left join
(SELECT * FROM `mobilesh_borotest`.stck where sactx <> 1) b
on a.products_sku = b.sku and a.products_id = b.isbn
set a.stck_id = b.id;

    SET result = CONCAT(result, 'Update stck stck_id into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');
    
	-- check active products count in stck

	-- STEP 8

--     select count(*) INTO endresult from `mobilesh_borotest`.stck where sactx <> 1;

select count(*) INTO endresult from `mobilesh_borotest`.stck where sactx <> 1;

    SET result = CONCAT(result, 'Updated destination table active items after import -> ', CAST(endresult as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

-- 	-- insert stck_pa where difference in prices

-- 	INSERT INTO `mobilesh_borotest`.`stck_pa`
-- 	(`id_stck`, `xtype`, `price`, `currency`, `suser`, `sactx`)
-- 	select -b.`id` as id_stck, 'o' as xtype, a.products_sale_price as price, 1 as currency, -1 as suser, 0 as sactx from 
-- 	(SELECT stck_id, c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- 	left join
-- 	(WITH stck_pu AS (SELECT * FROM `mobilesh_borotest`.`stck_p` UNION SELECT * FROM `mobilesh_borotest`.`stck_pa`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_pu GROUP BY abs(id)) a LEFT JOIN stck_pu b ON a.id=abs(b.id) AND a.stime=b.stime) b
-- 	on a.stck_id = b.id_stck
-- 	where cast(a.products_sale_price as decimal) <> cast(b.price as decimal);

-- 	-- insert in stck_p where id_stck price doesn't exist

-- 	insert into `mobilesh_borotest`.stck_p
-- 	(`id_stck`, `xtype`, `price`, `currency`, `suser`, `sactx`)
-- 	select a.stck_id, '0' as xtype, a.products_sale_price as price, a.products_sale_price_curr as currency, -1 as suser, 0 as sactx from 
-- 	(SELECT stck_id, c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
-- 	left join
-- 	(WITH stck_pu AS (SELECT * FROM `mobilesh_borotest`.`stck_p` UNION SELECT * FROM `mobilesh_borotest`.`stck_pa`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_pu GROUP BY abs(id)) a LEFT JOIN stck_pu b ON a.id=abs(b.id) AND a.stime=b.stime) b
-- 	on a.stck_id = b.id_stck
-- 	where b.id is null;

-- insert stck_pa where difference in prices

INSERT INTO `mobilesh_borotest`.`stck_pa`
(`id_stck`, `xtype`, `price`, `currency`, `suser`, `sactx`)
select -b.`id` as id_stck, 'o' as xtype, a.products_sale_price as price, 1 as currency, -1 as suser, 0 as sactx from 
(SELECT stck_id, c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stck_pu AS (SELECT * FROM mobilesh_borotest.`stck_p` UNION SELECT * FROM mobilesh_borotest.`stck_pa`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_pu GROUP BY abs(id)) a LEFT JOIN stck_pu b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.stck_id = b.id_stck
where cast(a.products_sale_price as decimal) <> cast(b.price as decimal);

    SET result = CONCAT(result, 'Insert into stck_pa into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');

-- insert in stck_p where id_stck price doesn't exist

insert into `mobilesh_borotest`.stck_p
(`id_stck`, `xtype`, `price`, `currency`, `suser`, `sactx`)
select a.stck_id, '0' as xtype, a.products_sale_price as price, a.products_sale_price_curr as currency, -1 as suser, 0 as sactx from 
(SELECT stck_id, c1.id as catgw, c2.id as catgi, products_sku, products_id, products_name, products_sale_price, products_sale_price_curr, products_crrsale_price, 1 as curr, galleryupd, CONCAT(ifnull(products_descr_short, ''), ifnull(products_descr_short_upd, '')) as description FROM `mobilesh_borotest`.`borotrade_json` bj left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 1) c1 on bj.category_id = c1.fid left join (SELECT * FROM `mobilesh_borotest`.catg WHERE xtype = 2) c2 on bj.category_id = c2.fid) a
left join
(WITH stck_pu AS (SELECT * FROM mobilesh_borotest.`stck_p` UNION SELECT * FROM mobilesh_borotest.`stck_pa`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_pu GROUP BY abs(id)) a LEFT JOIN stck_pu b ON a.id=abs(b.id) AND a.stime=b.stime) b
on a.stck_id = b.id_stck
where b.id is null;

    SET result = CONCAT(result, 'Insert into stck_p into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- UPDATE stck_l

	-- STEP 2

-- 	SELECT count(*) INTO updatesl FROM
-- 	`mobilesh_borotest`.`borotrade_json` bj left join `mobilesh_borotest`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join
-- --     `mobilesh_borotest`.stck_l
-- 	(WITH stck_lu AS (SELECT * FROM `mobilesh_borotest`.`stck_l` UNION SELECT * FROM `mobilesh_borotest`.`stck_la`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_lu GROUP BY abs(id)) a LEFT JOIN stck_lu b ON a.id=abs(b.id) AND a.stime=b.stime)
-- 	sl on s.id = sl.id_stck
-- 	where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

SELECT count(*) INTO updatesl FROM
`mobilesh_borotest`.`borotrade_json` bj left join mobilesh_borotest.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join
-- brortrade_crm.stck_l
(WITH stck_lu AS (SELECT * FROM mobilesh_borotest.`stck_l` UNION SELECT * FROM mobilesh_borotest.`stck_la`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_lu GROUP BY abs(id)) a LEFT JOIN stck_lu b ON a.id=abs(b.id) AND a.stime=b.stime)
 sl on s.id = sl.id_stck
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

    SET result = CONCAT(result, 'Updates stck_l found -> ', CAST(updatesl as CHAR), '\n');

	-- STEP 3

	-- INSERT INTO stck_la THE UPDATED RECORDS

-- 	INSERT INTO `mobilesh_borotest`.`stck_la`
-- 	SELECT -sl.`id`, sl.`id_stck`, sl.`id_lang`, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')), sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
-- -- 	SELECT sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
-- 	`mobilesh_borotest`.`borotrade_json` bj left join `mobilesh_borotest`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join
-- --     `mobilesh_borotest`.stck_l
-- 	(WITH stck_lu AS (SELECT * FROM `mobilesh_borotest`.`stck_l` UNION SELECT * FROM `mobilesh_borotest`.`stck_la`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_lu GROUP BY abs(id)) a LEFT JOIN stck_lu b ON a.id=abs(b.id) AND a.stime=b.stime)
--     sl on s.id = sl.id_stck
-- 	where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

INSERT INTO `mobilesh_borotest`.`stck_la`
-- SELECT -sl.`id`, sl.`id_stck`, sl.`id_lang`, sl.`title`, sl.`description`, sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
SELECT sl.`id`, -sl.`id_stck`, sl.`id_lang`, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')), sl.`suser`, sl.`stime`, sl.`sactx`, sl.`wid` FROM
`mobilesh_borotest`.`borotrade_json` bj left join mobilesh_borotest.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join
-- borotrade_crm.stck_l
(WITH stck_lu AS (SELECT * FROM mobilesh_borotest.`stck_l` UNION SELECT * FROM mobilesh_borotest.`stck_la`) SELECT DISTINCT b.* FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM stck_lu GROUP BY abs(id)) a LEFT JOIN stck_lu b ON a.id=abs(b.id) AND a.stime=b.stime)
sl on s.id = sl.id_stck
where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

    SET result = CONCAT(result, 'Inserts into archive table stck_la -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- STEP 4

	-- UPDATE stck_l ALL FIELDS WHERE ANY CHANGES!!!

-- 	UPDATE `mobilesh_borotest`.`stck_l` sl
-- 	left join `mobilesh_borotest`.stck s on s.id = sl.id_stck left join `mobilesh_borotest`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
-- 	SET sl.title = bj.products_name, sl.description = CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, ''))
-- 	where bj.products_name <> sl.title or CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) <> sl.description;

--     SET result = CONCAT(result, 'Update stck_l where changes found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- STEP 5

	-- INSERT ALL NEW PRODUCTS MISSING IN stck_l

-- 	INSERT INTO `mobilesh_borotest`.`stck_l` (`id_stck`, `id_lang`, `title`, `description`)
-- 	SELECT s.`id`, 1, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) FROM
-- 	`mobilesh_borotest`.`borotrade_json` bj left join `mobilesh_borotest`.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join `mobilesh_borotest`.stck_l sl on s.id = sl.id_stck
-- 	where sl.id is null;

INSERT INTO `mobilesh_borotest`.`stck_l` (`id_stck`, `id_lang`, `title`, `description`)
SELECT s.`id`, 1, bj.products_name, CONCAT(ifnull(bj.products_descr_short, ''), ifnull(bj.products_descr_short_upd, '')) FROM
`mobilesh_borotest`.`borotrade_json` bj left join mobilesh_borotest.stck s on bj.products_sku = s.sku and bj.products_id = s.isbn left join mobilesh_borotest.stck_l sl on s.id = sl.id_stck
where sl.id is null;

    SET result = CONCAT(result, 'Insert into stck_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- STEP 6

	-- UPDATE stck_l.sactx with 1 to "delete" all mising in borotrade_json PRODUCTS!!!

-- 	UPDATE `mobilesh_borotest`.stck_l sl left join `mobilesh_borotest`.stck s on sl.id_stck = s.id
-- 	left join `mobilesh_borotest`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
-- 	set sl.sactx = 1
-- 	where bj.products_sku is null;

UPDATE mobilesh_borotest.stck_l sl left join mobilesh_borotest.stck s on sl.id_stck = s.id
left join `mobilesh_borotest`.`borotrade_json` bj on bj.products_sku = s.sku and bj.products_id = s.isbn
set sl.sactx = 1
where bj.products_sku is null;

    SET result = CONCAT(result, 'Update stck_l to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- check active products count in stck_l

	-- STEP 7

    select count(*) INTO endresultsl from `mobilesh_borotest`.stck_l where sactx <> 1;

    SET result = CONCAT(result, 'Updated destination table active items after import -> ', CAST(endresultsl as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- UPDATE attr

	-- update sactx with 1 for all non existant attr

	update `mobilesh_borotest`.attr a right join
	(select attr, name, id from
	(select attr, name, id from
	(SELECT DISTINCT attr FROM `mobilesh_borotest`.borotrade_attr group by attr) src_a
	left join
-- 	(select id, name from `mobilesh_borotest`.attr) dst_a
	(WITH attru AS (SELECT * FROM `mobilesh_borotest`.`attr` UNION SELECT * FROM `mobilesh_borotest`.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
	on src_a.attr = dst_a.name
	UNION
	select attr, name, id from
	(SELECT DISTINCT attr FROM `mobilesh_borotest`.borotrade_attr group by attr) src_a
	right join
-- 	(select id, name from `mobilesh_borotest`.attr) dst_a
	(WITH attru AS (SELECT * FROM `mobilesh_borotest`.`attr` UNION SELECT * FROM `mobilesh_borotest`.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
	on src_a.attr = dst_a.name) a
	where a.attr is null) src on src.id = a.id
	set a.sactx = 1;

    SET result = CONCAT(result, 'Update attr to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert all new rows into attr

	insert into `mobilesh_borotest`.attr (name)
	select attr from
	(select attr, name, id from
	(SELECT DISTINCT attr FROM `mobilesh_borotest`.borotrade_attr group by attr) src_a
	left join
-- 	(select id, name from `mobilesh_borotest`.attr) dst_a
	(WITH attru AS (SELECT * FROM `mobilesh_borotest`.`attr` UNION SELECT * FROM `mobilesh_borotest`.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
	on src_a.attr = dst_a.name
	UNION
	select attr, name, id from
	(SELECT DISTINCT attr FROM `mobilesh_borotest`.borotrade_attr group by attr) src_a
	right join
-- 	(select id, name from `mobilesh_borotest`.attr) dst_a
	(WITH attru AS (SELECT * FROM `mobilesh_borotest`.`attr` UNION SELECT * FROM `mobilesh_borotest`.`attra`) SELECT DISTINCT b.id, b.name FROM (SELECT abs(id) AS id, MAX(stime) AS stime FROM attru GROUP BY abs(id)) a LEFT JOIN attru b ON a.id=abs(b.id) AND a.stime=b.stime) dst_a
	on src_a.attr = dst_a.name) a
	where a.name is null;

    SET result = CONCAT(result, 'Insert into attr where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update attr_id into src table -> borotrade_attr

	update `mobilesh_borotest`.borotrade_attr src_a left join 
	(select id, name from `mobilesh_borotest`.attr where sactx <> 1) dst_a
	on src_a.attr = dst_a.name
	set src_a.attr_id = dst_a.id;

    SET result = CONCAT(result, 'Update attr_id into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update sactx with 1 for all non existant attr_l

	update `mobilesh_borotest`.attr_l al left join `mobilesh_borotest`.attr a on al.id_attr = a.id set al.sactx = a.sactx;

    SET result = CONCAT(result, 'Update attr_l to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert new values into attr_l

	INSERT INTO `mobilesh_borotest`.`attr_l` (`id_attr`, `id_lang`, `title`)
	select a.id, 1, a.name from `mobilesh_borotest`.`attr` a left join `mobilesh_borotest`.`attr_l` al on a.id = al.id_attr where al.id_attr is null;

    SET result = CONCAT(result, 'Insert into attr_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- check both tables are ok

	select count(*) into attrcount from (SELECT attr FROM `mobilesh_borotest`.`borotrade_attr`group by attr) a;
    SET result = CONCAT(result, 'Feed table attr active items -> ', CAST(attrcount as CHAR), '\n');

	select count(*) into attrcounta from `mobilesh_borotest`.`attr` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table attr active items after impot -> ', CAST(attrcounta as CHAR), '\n');

	select count(*) into attrcountal from `mobilesh_borotest`.`attr_l` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table attr_l active items after impot -> ', CAST(attrcountal as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_id in borotrade_attr from borotrade_json

	update `mobilesh_borotest`.borotrade_attr a left join `mobilesh_borotest`.borotrade_json j on a.products_sku = j.products_sku and a.products_id = j.products_id set a.stck_id = j.stck_id;

    SET result = CONCAT(result, 'Updated feed table attr_l -> ', CAST(attrcountal as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update sactx in term where not found in borotrade_attr

	update `mobilesh_borotest`.term t left join 
	(SELECT attr_id, val FROM `mobilesh_borotest`.borotrade_attr group by attr_id, val) a
	on t.name = a.val and t.id_attr = a.attr_id and t.sactx <> 1
	set t.sactx = 1
	where a.val is null;

	-- insert into term the new vals

	INSERT INTO `mobilesh_borotest`.`term` (`id_attr`, `name`)
	select a.attr_id, a.val from 
	(SELECT attr_id, val FROM `mobilesh_borotest`.borotrade_attr group by attr_id, val) a
	left join
	`mobilesh_borotest`.term t
	on a.val = t.name and t.id_attr = a.attr_id and t.sactx <> 1
	where t.id is null;

    SET result = CONCAT(result, 'Insert into term where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update term_id into src table -> borotrade_attr

	update `mobilesh_borotest`.borotrade_attr src_a left join 
	(select id, id_attr, name from `mobilesh_borotest`.term where sactx <> 1) dst_a
	on src_a.val = dst_a.name and src_a.attr_id = dst_a.id_attr
	set src_a.term_id = dst_a.id;

    SET result = CONCAT(result, 'Update term_id into feed table -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- update sactx with 1 for all non existant term_l

	update `mobilesh_borotest`.term_l tl left join `mobilesh_borotest`.term t on tl.id_term = t.id set tl.sactx = t.sactx;

    SET result = CONCAT(result, 'Update term to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert new values into term_l

	INSERT INTO `mobilesh_borotest`.`term_l` (`id_term`, `id_lang`, `title`)
	select t.id, 1, t.name from `mobilesh_borotest`.`term` t left join `mobilesh_borotest`.`term_l` tl on t.id = tl.id_term where tl.id_term is null;

    SET result = CONCAT(result, 'Insert into term_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- check both tables are ok

	select count(*) into termcount from (select attr_id, val from `mobilesh_borotest`.borotrade_attr group by attr_id, val) a;
    SET result = CONCAT(result, 'Feed table term active items -> ', CAST(termcount as CHAR), '\n');

	select count(*) into termcounta from `mobilesh_borotest`.`term` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table term active items after impot -> ', CAST(termcounta as CHAR), '\n');

	select count(*) into termcountal from `mobilesh_borotest`.`term_l` where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table term_l active items after impot -> ', CAST(termcountal as CHAR), '\n');


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_a where not found in borotrade_attr
	update mobilesh_borotest.stck_a s left join mobilesh_borotest.borotrade_attr a on s.id_attr = a.attr_id and s.id_term = a.term_id and s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

    SET result = CONCAT(result, 'Update term to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert into stck_a where new found in borotrade_attr
	INSERT INTO `mobilesh_borotest`.`stck_a` (`id_stck`, `id_attr`, `id_term`)
	SELECT a.stck_id, a.attr_id, a.term_id FROM `mobilesh_borotest`.borotrade_attr a left join `mobilesh_borotest`.stck_a s on a.attr_id = s.id_attr and a.term_id = s.id_term and a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;

    SET result = CONCAT(result, 'Insert into term_l where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');


	select count(*) into stckacount from `mobilesh_borotest`.borotrade_attr;
    SET result = CONCAT(result, 'Feed table stck_a active items -> ', CAST(stckacount as CHAR), '\n');
    
	select count(*) into stckacounta from `mobilesh_borotest`.stck_a where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table stck_a active items after impot -> ', CAST(stckacounta as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	-- update stck_id in borotrade_linkedp from borotrade_json

	update `mobilesh_borotest`.borotrade_linkedp p left join `mobilesh_borotest`.borotrade_json j on p.products_sku = j.products_sku and p.products_id = j.products_id set p.stck_id = j.stck_id;


	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update into stck_r not found

	update `mobilesh_borotest`.borotrade_linkedp p left join `mobilesh_borotest`.stck_r r on p.stck_id = r.id_stck and r.sactx <> 1 set r.sactx = 1 where p.stck_id is null;

    SET result = CONCAT(result, 'Update stck_r to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert into stck_r the new found rows

	INSERT INTO `mobilesh_borotest`.`stck_r` (`id_stck`, `text`)
	select p.stck_id, p.linkedp from `mobilesh_borotest`.borotrade_linkedp p left join `mobilesh_borotest`.stck_r r on p.stck_id = r.id_stck and r.sactx <> 1 where r.id_stck is null;

    SET result = CONCAT(result, 'Insert into stck_r where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	select count(*) into stckrcount from `mobilesh_borotest`.borotrade_linkedp;
    SET result = CONCAT(result, 'Feed table stck_r active items -> ', CAST(stckrcount as CHAR), '\n');
    
	select count(*) into stckrcounta from `mobilesh_borotest`.stck_r where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table stck_r active items after impot -> ', CAST(stckrcounta as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_id in borotrade_lgallery_json from borotrade_json

	update `mobilesh_borotest`.borotrade_gallery_json g left join `mobilesh_borotest`.borotrade_json j on g.products_sku = j.products_sku and g.products_id = j.products_id set g.stck_id = j.stck_id;

    SET result = CONCAT(result, 'Update borotrade_gallery_json id_stck -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	-- update stck_g where not found in borotrade_gallery_json
	update `mobilesh_borotest`.stck_g s left join `mobilesh_borotest`.borotrade_gallery_json a on s.id_stck = a.stck_id and s.sactx <> 1 set s.sactx = 1 where a.id is null;

    SET result = CONCAT(result, 'Update stck_g to mark as delete where feed items not found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	-- insert into stck_g where new found in borotrade_gallery_json
	INSERT INTO `mobilesh_borotest`.`stck_g` (`id_stck`, `urlx`, `path`)
	SELECT a.stck_id, a.gallery, a.path FROM `mobilesh_borotest`.borotrade_gallery_json a left join `mobilesh_borotest`.stck_g s on a.stck_id = s.id_stck and s.sactx <> 1 where s.id is null;

    SET result = CONCAT(result, 'Insert into stck_g where new rows found -> ', CAST(ROW_COUNT() as CHAR), '\n');

	select count(*) into stckgcount from `mobilesh_borotest`.borotrade_gallery_json;
    SET result = CONCAT(result, 'Feed table gallery_json active items -> ', CAST(stckgcount as CHAR), '\n');

	select count(*) into stckgcounta from `mobilesh_borotest`.stck_g where sactx <> 1;
    SET result = CONCAT(result, 'Updated destination table stck_g active items after impot -> ', CAST(stckgcounta as CHAR), '\n');

	-- ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
	-- update final (added by Desso
	UPDATE `mobilesh_borotest`.stck JOIN (SELECT id_stck, MIN(id) as id_gall FROM `mobilesh_borotest`.stck_g GROUP BY id_stck) AS subquery ON stck.id = subquery.id_stck SET stck.id_gall = subquery.id_gall;


    SELECT 1, result;
END;

$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;



